import { useState, useCallback } from 'react';
import { lexiconAPI } from '../services/lexiconAPI';
import type { LexiconEntry } from '../types/lexicon';

interface UseLexiconReturn {
  entry: LexiconEntry | null;
  loading: boolean;
  error: string | null;
  lookupByStrongs: (strongsNumber: string) => Promise<void>;
  lookupByGreek: (greekWord: string) => Promise<void>;
  clearEntry: () => void;
}

export const useLexicon = (): UseLexiconReturn => {
  const [entry, setEntry] = useState<LexiconEntry | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const lookupByStrongs = useCallback(async (strongsNumber: string) => {
    if (!strongsNumber) return;

    setLoading(true);
    setError(null);

    try {
      const data = await lexiconAPI.getByStrongs(strongsNumber);
      setEntry(data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to fetch lexicon entry';
      setError(errorMessage);
      setEntry(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const lookupByGreek = useCallback(async (greekWord: string) => {
    if (!greekWord) return;

    setLoading(true);
    setError(null);

    try {
      const data = await lexiconAPI.getByGreek(greekWord);
      if (data && data.length > 0) {
        setEntry(data[0]); // Show first match
      } else {
        setError(`No lexicon entry found for "${greekWord}"`);
        setEntry(null);
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to fetch lexicon entry';
      setError(errorMessage);
      setEntry(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearEntry = useCallback(() => {
    setEntry(null);
    setError(null);
  }, []);

  return {
    entry,
    loading,
    error,
    lookupByStrongs,
    lookupByGreek,
    clearEntry,
  };
};
