import { useState, useCallback } from 'react';
import { verseAPI } from '../services/verseAPI';
import type { Verse } from '../types/verse';

interface UseVerseReturn {
  verse: Verse | null;
  loading: boolean;
  error: string | null;
  searchVerse: (reference: string) => Promise<void>;
  clearVerse: () => void;
}

export const useVerse = (): UseVerseReturn => {
  const [verse, setVerse] = useState<Verse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const searchVerse = useCallback(async (reference: string) => {
    if (!reference.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await verseAPI.getByReference(reference);
      setVerse(data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to fetch verse';
      setError(errorMessage);
      setVerse(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearVerse = useCallback(() => {
    setVerse(null);
    setError(null);
  }, []);

  return {
    verse,
    loading,
    error,
    searchVerse,
    clearVerse,
  };
};
