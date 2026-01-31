/**
 * Conversation API Client
 * =======================
 * HTTP client for conversation history endpoints.
 */

import api from './api';
import type {
  Conversation,
  ConversationListItem,
  ConversationCreate,
  ConversationUpdate,
  ConversationMessage
} from '../types/conversation';

export const conversationAPI = {
  /**
   * List user's conversations
   */
  async list(skip = 0, limit = 50): Promise<ConversationListItem[]> {
    const response = await api.get<ConversationListItem[]>('/conversations', {
      params: { skip, limit }
    });
    return response.data;
  },

  /**
   * Get conversation by ID
   */
  async get(id: number): Promise<Conversation> {
    const response = await api.get<Conversation>(`/conversations/${id}`);
    return response.data;
  },

  /**
   * Create new conversation
   */
  async create(data: ConversationCreate): Promise<Conversation> {
    const response = await api.post<Conversation>('/conversations', data);
    return response.data;
  },

  /**
   * Update conversation
   */
  async update(id: number, data: ConversationUpdate): Promise<Conversation> {
    const response = await api.put<Conversation>(`/conversations/${id}`, data);
    return response.data;
  },

  /**
   * Append message to conversation
   */
  async appendMessage(
    id: number,
    role: 'user' | 'assistant',
    content: string
  ): Promise<Conversation> {
    const response = await api.post<Conversation>(
      `/conversations/${id}/messages`,
      null,
      { params: { role, content } }
    );
    return response.data;
  },

  /**
   * Delete conversation
   */
  async delete(id: number): Promise<void> {
    await api.delete(`/conversations/${id}`);
  },

  /**
   * Create conversation from messages
   */
  async createFromMessages(messages: ConversationMessage[]): Promise<Conversation> {
    // Auto-generate title from first user message
    const firstUserMessage = messages.find(m => m.role === 'user');
    const title = firstUserMessage
      ? firstUserMessage.content.slice(0, 50) + (firstUserMessage.content.length > 50 ? '...' : '')
      : 'New Conversation';

    return this.create({ title, messages });
  }
};
