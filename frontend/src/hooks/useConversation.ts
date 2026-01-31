/**
 * useConversation Hook
 * ====================
 * Custom React hook for managing conversation history.
 */

import { useState, useEffect, useCallback } from 'react';
import { conversationAPI } from '../services/conversationAPI';
import type {
  Conversation,
  ConversationListItem,
  ConversationMessage
} from '../types/conversation';

interface UseConversationResult {
  // Current conversation
  currentConversation: Conversation | null;

  // Conversation list
  conversations: ConversationListItem[];

  // Loading states
  loading: boolean;
  saving: boolean;

  // Error state
  error: string | null;

  // Actions
  loadConversations: () => Promise<void>;
  loadConversation: (id: number) => Promise<void>;
  createConversation: (messages?: ConversationMessage[]) => Promise<Conversation>;
  saveMessages: (messages: ConversationMessage[]) => Promise<void>;
  deleteConversation: (id: number) => Promise<void>;
  startNewConversation: () => void;
}

export const useConversation = (): UseConversationResult => {
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [conversations, setConversations] = useState<ConversationListItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Load user's conversation list
   */
  const loadConversations = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await conversationAPI.list();
      setConversations(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load conversations');
      console.error('Error loading conversations:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Load specific conversation
   */
  const loadConversation = useCallback(async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      const data = await conversationAPI.get(id);
      setCurrentConversation(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load conversation');
      console.error('Error loading conversation:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Create new conversation
   */
  const createConversation = useCallback(async (messages?: ConversationMessage[]): Promise<Conversation> => {
    try {
      setSaving(true);
      setError(null);

      const conversation = messages
        ? await conversationAPI.createFromMessages(messages)
        : await conversationAPI.create({});

      setCurrentConversation(conversation);

      // Reload conversation list
      await loadConversations();

      return conversation;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create conversation');
      console.error('Error creating conversation:', err);
      throw err;
    } finally {
      setSaving(false);
    }
  }, [loadConversations]);

  /**
   * Save messages to current conversation (or create new one)
   */
  const saveMessages = useCallback(async (messages: ConversationMessage[]) => {
    try {
      setSaving(true);
      setError(null);

      if (currentConversation) {
        // Update existing conversation
        const updated = await conversationAPI.update(currentConversation.id, {
          messages
        });
        setCurrentConversation(updated);
      } else {
        // Create new conversation
        await createConversation(messages);
      }

      // Reload conversation list
      await loadConversations();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save messages');
      console.error('Error saving messages:', err);
    } finally {
      setSaving(false);
    }
  }, [currentConversation, createConversation, loadConversations]);

  /**
   * Delete conversation
   */
  const deleteConversation = useCallback(async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await conversationAPI.delete(id);

      // Clear current conversation if it was deleted
      if (currentConversation?.id === id) {
        setCurrentConversation(null);
      }

      // Reload conversation list
      await loadConversations();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete conversation');
      console.error('Error deleting conversation:', err);
    } finally {
      setLoading(false);
    }
  }, [currentConversation, loadConversations]);

  /**
   * Start new conversation
   */
  const startNewConversation = useCallback(() => {
    setCurrentConversation(null);
  }, []);

  // Load conversations on mount
  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  return {
    currentConversation,
    conversations,
    loading,
    saving,
    error,
    loadConversations,
    loadConversation,
    createConversation,
    saveMessages,
    deleteConversation,
    startNewConversation
  };
};
