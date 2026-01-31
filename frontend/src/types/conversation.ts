/**
 * Conversation Types
 * ==================
 * TypeScript interfaces for conversation history.
 */

export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface Conversation {
  id: number;
  user_id: number;
  title: string | null;
  messages: ConversationMessage[];
  created_at: string;
  updated_at: string;
}

export interface ConversationListItem {
  id: number;
  title: string;
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface ConversationCreate {
  title?: string;
  messages?: ConversationMessage[];
}

export interface ConversationUpdate {
  title?: string;
  messages?: ConversationMessage[];
}
