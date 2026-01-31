import type { ChatRequest } from '../types/chat';

// WebSocket URL
const WS_URL = import.meta.env.VITE_API_URL?.replace('http', 'ws') || 'ws://localhost:8000';

export const chatAPI = {
  // Create WebSocket connection for streaming chat
  connectWebSocket: (onMessage: (data: any) => void, onError?: (error: any) => void): WebSocket => {
    const ws = new WebSocket(`${WS_URL}/api/chat/stream`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      onMessage({ type: 'connected' });
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // Transform backend response format to frontend format
        if (data.chunk !== undefined) {
          if (data.done) {
            onMessage({ type: 'done' });
          } else {
            onMessage({ type: 'chunk', content: data.chunk });
          }
        } else if (data.error) {
          onMessage({ type: 'error', message: data.error });
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (onError) onError(error);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return ws;
  },

  // Send message through WebSocket
  sendMessage: (ws: WebSocket, request: ChatRequest): void => {
    if (ws.readyState === WebSocket.OPEN) {
      // Transform frontend request to backend format
      const backendRequest = {
        message: request.message,
        verse_reference: request.verse_reference,
        conversation_history: [],
        include_lexicon: true,
      };
      ws.send(JSON.stringify(backendRequest));
    } else {
      console.error('WebSocket is not open. Ready state:', ws.readyState);
    }
  },

  // Close WebSocket connection
  closeWebSocket: (ws: WebSocket): void => {
    if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
      ws.close();
    }
  },
};
