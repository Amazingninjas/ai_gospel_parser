import api from './api';
import type { Verse, Book } from '../types/verse';

export const verseAPI = {
  // Get verse by reference (e.g., "John 3:16")
  getByReference: async (reference: string): Promise<Verse> => {
    const response = await api.get(`/verses/${encodeURIComponent(reference)}`);
    return response.data;
  },

  // Get verse by book code, chapter, and verse number
  getByBookCode: async (code: string, chapter: number, verse: number): Promise<Verse> => {
    const response = await api.get(`/verses/book/${code}/${chapter}/${verse}`);
    return response.data;
  },

  // Get list of all NT books
  getBooks: async (): Promise<Book[]> => {
    const response = await api.get('/verses/books/list');
    return response.data;
  },
};
