import { useState, useEffect, useRef } from 'react';
import { useWebSocket, useConversation } from '../hooks';
import type { ConversationMessage } from '../types/conversation';

interface ChatInterfaceProps {
  verseReference?: string;
}

const ChatInterface = ({ verseReference }: ChatInterfaceProps) => {
  const [input, setInput] = useState('');
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { messages, sendMessage, connected, loading, error, loadMessages } = useWebSocket();
  const {
    currentConversation,
    conversations,
    loading: conversationLoading,
    saving,
    loadConversation,
    saveMessages,
    deleteConversation,
    startNewConversation
  } = useConversation();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load messages from current conversation
  useEffect(() => {
    if (currentConversation && currentConversation.messages) {
      // Convert ConversationMessage[] to ChatMessage[]
      const chatMessages = currentConversation.messages.map(msg => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp ? new Date(msg.timestamp) : undefined
      }));
      loadMessages(chatMessages as any);
    }
  }, [currentConversation, loadMessages]);

  // Save messages to database after each exchange
  useEffect(() => {
    if (messages.length > 0 && !loading) {
      // Debounce saving to avoid excessive API calls
      const timeoutId = setTimeout(() => {
        // Convert ChatMessage[] to ConversationMessage[]
        const conversationMessages: ConversationMessage[] = messages.map(msg => ({
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp ? msg.timestamp.toISOString() : undefined
        }));
        saveMessages(conversationMessages);
      }, 1000);

      return () => clearTimeout(timeoutId);
    }
  }, [messages, loading, saveMessages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    sendMessage(input, verseReference);
    setInput('');
  };

  const handleLoadConversation = async (id: number) => {
    await loadConversation(id);
    setShowHistory(false);
  };

  const handleDeleteConversation = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Delete this conversation?')) {
      await deleteConversation(id);
    }
  };

  const handleNewConversation = () => {
    startNewConversation();
    setShowHistory(false);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 flex flex-col h-[600px] relative">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h2 className="text-xl font-semibold">AI Chat</h2>
          {saving && (
            <span className="text-xs text-gray-500 italic">Saving...</span>
          )}
          {currentConversation && (
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              {currentConversation.title || 'Untitled'}
            </span>
          )}
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleNewConversation}
            className="text-sm text-blue-600 hover:text-blue-800"
            title="New conversation"
          >
            + New
          </button>
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="text-sm text-gray-600 hover:text-gray-800"
            title="Conversation history"
          >
            {showHistory ? '✕ Close' : '📚 History'}
          </button>
          <div className="flex items-center gap-2">
            <div
              className={`w-2 h-2 rounded-full ${
                connected ? 'bg-green-500' : 'bg-red-500'
              }`}
            />
            <span className="text-xs text-gray-600">
              {connected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
      </div>

      {/* Conversation History Sidebar */}
      {showHistory && (
        <div className="absolute top-0 right-0 w-80 h-full bg-white border-l border-gray-200 shadow-lg z-10 flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold">Conversation History</h3>
              <button
                onClick={() => setShowHistory(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            {conversationLoading ? (
              <div className="text-center text-gray-500 py-8">Loading...</div>
            ) : conversations.length === 0 ? (
              <div className="text-center text-gray-500 py-8">
                No conversations yet
              </div>
            ) : (
              <div className="space-y-2">
                {conversations.map((conv) => (
                  <div
                    key={conv.id}
                    onClick={() => handleLoadConversation(conv.id)}
                    className={`p-3 border rounded-lg cursor-pointer hover:bg-gray-50 ${
                      currentConversation?.id === conv.id
                        ? 'bg-blue-50 border-blue-300'
                        : 'border-gray-200'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-sm truncate">
                          {conv.title || 'Untitled Conversation'}
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {conv.message_count} messages
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                          {new Date(conv.updated_at).toLocaleDateString()}
                        </div>
                      </div>
                      <button
                        onClick={(e) => handleDeleteConversation(conv.id, e)}
                        className="text-red-500 hover:text-red-700 text-xs"
                        title="Delete conversation"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4 border border-gray-200 rounded-md p-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <p>Ask questions about Greek words, grammar, or theology</p>
            <p className="text-sm mt-2">Example: "What does agape mean in this context?"</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>
                {msg.timestamp && (
                  <div
                    className={`text-xs mt-1 ${
                      msg.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                    }`}
                  >
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={!connected || loading}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={!connected || loading || !input.trim()}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          Send
        </button>
      </form>

      {verseReference && (
        <div className="mt-2 px-3 py-2 bg-blue-50 border border-blue-200 rounded text-xs">
          <span className="font-semibold text-blue-900">📖 Verse Context:</span>{' '}
          <span className="text-blue-700">{verseReference}</span>
        </div>
      )}
      {!verseReference && (
        <div className="mt-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded text-xs text-gray-600">
          💡 Tip: Search for a verse above to give the AI context for your questions
        </div>
      )}
    </div>
  );
};

export default ChatInterface;
