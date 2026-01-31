import { useState } from 'react';
import { verseAPI } from '../services/verseAPI';
import type { Verse, VerseWord } from '../types/verse';
import { cleanGreekWord, normalizeGreekText } from '../utils/greekText';
import { VerseLoadingSkeleton } from './SkeletonLoader';
import { formatErrorMessage } from '../services/api';

interface VerseDisplayProps {
  onWordClick?: (strongsNumber: string, greekWord: string) => void;
  onVerseLoaded?: (reference: string) => void;
}

const VerseDisplay = ({ onWordClick, onVerseLoaded }: VerseDisplayProps) => {
  const [reference, setReference] = useState('');
  const [verse, setVerse] = useState<Verse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reference.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await verseAPI.getByReference(reference);
      setVerse(data);
      // Notify parent component of the loaded verse
      if (onVerseLoaded) {
        onVerseLoaded(data.reference);
      }
    } catch (err: any) {
      setError(formatErrorMessage(err));
      setVerse(null);
    } finally {
      setLoading(false);
    }
  };

  const handleWordClick = (word: VerseWord) => {
    if (onWordClick && word.strongs_number) {
      onWordClick(word.strongs_number, word.greek);
    }
  };

  const handleGreekWordClick = (greekWord: string) => {
    // Clean up punctuation using utility function
    const cleaned = cleanGreekWord(greekWord);
    if (onWordClick && cleaned) {
      // Call lexicon lookup by Greek word (no Strong's number yet)
      onWordClick('', cleaned);
    }
  };

  // Split Greek text into words for simple clickability
  const splitGreekText = (text: string): string[] => {
    return text.split(/\s+/).filter(w => w.length > 0);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Verse Lookup</h2>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={reference}
            onChange={(e) => setReference(e.target.value)}
            placeholder="Enter verse reference (e.g., John 3:16)"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition"
          >
            {loading ? 'Loading...' : 'Search'}
          </button>
        </div>
      </form>

      {/* Loading State */}
      {loading && <VerseLoadingSkeleton />}

      {/* Error Message */}
      {error && !loading && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Verse Display */}
      {verse && !loading && (
        <div className="space-y-6">
          {/* Reference Header */}
          <div className="border-b pb-2">
            <h3 className="text-lg font-semibold text-gray-900">{verse.reference}</h3>
          </div>

          {/* Greek Text */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3">Greek (SBLGNT)</h4>
            {verse.words && verse.words.length > 0 ? (
              <div className="greek-text space-y-2">
                {verse.words.map((word, index) => (
                  <span key={index} className="inline-block mr-2 mb-2">
                    <button
                      onClick={() => handleWordClick(word)}
                      className="group hover:bg-blue-50 rounded px-1 transition"
                      title={`${word.transliteration} - ${word.english}\n${word.morphology}\n${word.strongs_number}`}
                    >
                      <span className="greek-text text-lg group-hover:text-blue-600">
                        {word.greek}
                      </span>
                      {word.strongs_number && (
                        <span className="text-xs text-gray-500 ml-1">
                          {word.strongs_number}
                        </span>
                      )}
                    </button>
                  </span>
                ))}
              </div>
            ) : (
              <div className="space-y-2 bg-amber-50 p-4 rounded-md border border-amber-100">
                {splitGreekText(normalizeGreekText(verse.greek_text)).map((word, index) => (
                  <button
                    key={index}
                    onClick={() => handleGreekWordClick(word)}
                    className="inline-block mr-3 mb-2 hover:bg-blue-100 rounded px-2 py-1 transition hover:shadow-sm"
                    title="Click to see lexicon entry"
                  >
                    <span className="greek-text">{word}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* English Text */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">English (WEB)</h4>
            <p className="text-gray-800">{verse.english_text}</p>
          </div>

          {/* Word Count Info */}
          {verse.words && verse.words.length > 0 && (
            <div className="text-xs text-gray-500 pt-2 border-t">
              {verse.words.length} words • Click any Greek word to see lexicon entry
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!verse && !error && !loading && (
        <div className="text-center py-8 text-gray-500">
          <p>Enter a verse reference to begin studying</p>
          <p className="text-sm mt-2">Try: John 3:16, Romans 8:28, Matthew 5:1</p>
        </div>
      )}
    </div>
  );
};

export default VerseDisplay;
