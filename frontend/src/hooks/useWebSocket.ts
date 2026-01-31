import { useState, useEffect, useCallback, useRef } from 'react';
import { chatAPI } from '../services/chatAPI';
import type { ChatMessage } from '../types/chat';

interface UseWebSocketReturn {
  messages: ChatMessage[];
  sendMessage: (message: string, verseReference?: string) => void;
  connected: boolean;
  loading: boolean;
  error: string | null;
  clearMessages: () => void;
  loadMessages: (messages: ChatMessage[]) => void;
}

export const useWebSocket = (): UseWebSocketReturn => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Connect WebSocket on mount
    const ws = chatAPI.connectWebSocket(
      (data) => {
        if (data.type === 'connected') {
          setConnected(true);
          setError(null);
        } else if (data.type === 'chunk') {
          // Append chunk to last message
          setMessages((prev) => {
            const lastMsg = prev[prev.length - 1];
            if (lastMsg && lastMsg.role === 'assistant') {
              return [
                ...prev.slice(0, -1),
                { ...lastMsg, content: lastMsg.content + data.content },
              ];
            }
            return [
              ...prev,
              { role: 'assistant', content: data.content, timestamp: new Date() },
            ];
          });
        } else if (data.type === 'done') {
          setLoading(false);
        } else if (data.type === 'error') {
          setError(data.message || 'An error occurred');
          setLoading(false);
        }
      },
      (err) => {
        setError('WebSocket connection failed');
        setConnected(false);
        console.error('WebSocket error:', err);
      }
    );

    wsRef.current = ws;

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        chatAPI.closeWebSocket(wsRef.current);
      }
    };
  }, []);

  const sendMessage = useCallback((message: string, verseReference?: string) => {
    if (!wsRef.current || !message.trim()) return;

    // Add user message to state
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);

    // Send to WebSocket
    chatAPI.sendMessage(wsRef.current, {
      message,
      verse_reference: verseReference,
    });

    setLoading(true);
    setError(null);
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const loadMessages = useCallback((newMessages: ChatMessage[]) => {
    setMessages(newMessages);
  }, []);

  return {
    messages,
    sendMessage,
    connected,
    loading,
    error,
    clearMessages,
    loadMessages,
  };
};
