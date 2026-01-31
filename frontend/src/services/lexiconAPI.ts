import api from './api';
import type { LexiconEntry, LexiconSearchResult } from '../types/lexicon';

export const lexiconAPI = {
  // Get lexicon entry by Strong's number
  getByStrongs: async (number: string): Promise<LexiconEntry> => {
    const response = await api.get(`/lexicon/strongs/${number}`);
    return response.data;
  },

  // Get lexicon entry by Greek word
  getByGreek: async (word: string): Promise<LexiconEntry[]> => {
    const response = await api.get(`/lexicon/greek/${encodeURIComponent(word)}`);
    return response.data;
  },

  // Get lexicon entry by transliteration
  getByTransliteration: async (trans: string): Promise<LexiconEntry[]> => {
    const response = await api.get(`/lexicon/transliteration/${trans}`);
    return response.data;
  },

  // Search lexicon entries
  search: async (query: string): Promise<LexiconSearchResult> => {
    const response = await api.get(`/lexicon/search`, { params: { q: query } });
    return response.data;
  },

  // Get lexicon statistics
  getStats: async (): Promise<any> => {
    const response = await api.get('/lexicon/stats');
    return response.data;
  },
};
