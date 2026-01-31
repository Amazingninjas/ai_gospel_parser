import { useState, useEffect } from 'react';
import { lexiconAPI } from '../services/lexiconAPI';
import type { LexiconEntry } from '../types/lexicon';
import { LexiconLoadingSkeleton } from './SkeletonLoader';
import { formatErrorMessage } from '../services/api';

interface LexiconPanelProps {
  strongsNumber?: string;
  greekWord?: string;
}

const LexiconPanel = ({ strongsNumber, greekWord }: LexiconPanelProps) => {
  const [entry, setEntry] = useState<LexiconEntry | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (strongsNumber) {
      fetchLexiconEntry(strongsNumber);
    } else if (greekWord) {
      // Lookup by Greek word if no Strong's number
      fetchByGreekWord(greekWord);
    }
  }, [strongsNumber, greekWord]);

  const fetchLexiconEntry = async (number: string) => {
    setLoading(true);
    setError(null);

    try {
      const data = await lexiconAPI.getByStrongs(number);
      setEntry(data);
    } catch (err: any) {
      setError(formatErrorMessage(err));
      setEntry(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchByGreekWord = async (word: string) => {
    setLoading(true);
    setError(null);

    try {
      const data = await lexiconAPI.getByGreek(word);
      if (data && data.length > 0) {
        setEntry(data[0]); // Show first match
      } else {
        setError(`No lexicon entry found for "${word}"`);
        setEntry(null);
      }
    } catch (err: any) {
      setError(formatErrorMessage(err));
      setEntry(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 h-[600px] overflow-y-auto">
      <h2 className="text-xl font-semibold mb-4">Lexicon</h2>

      {loading && <LexiconLoadingSkeleton />}

      {error && !loading && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
          {error}
        </div>
      )}

      {entry && !loading && (
        <div className="space-y-4">
          {/* Header */}
          <div className="border-b pb-3">
            <div className="flex items-center justify-between mb-2">
              <h3 className="greek-text text-2xl font-semibold">{entry.greek}</h3>
              <span className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">
                {entry.strongs_number}
              </span>
            </div>
            <p className="text-gray-700 italic">{entry.transliteration}</p>
            {entry.pronunciation && (
              <p className="text-sm text-gray-600">/{entry.pronunciation}/</p>
            )}
          </div>

          {/* Definition */}
          <div>
            <h4 className="text-sm font-semibold text-gray-700 mb-1">Definition</h4>
            <p className="text-gray-800">{entry.definition}</p>
          </div>

          {/* Usage */}
          {entry.usage && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-1">Usage</h4>
              <p className="text-gray-800">{entry.usage}</p>
            </div>
          )}

          {/* Derivation */}
          {entry.derivation && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-1">Derivation</h4>
              <p className="text-gray-700 text-sm">{entry.derivation}</p>
            </div>
          )}

          {/* Thayer's Definition */}
          {entry.thayers && (
            <div className="bg-blue-50 p-3 rounded-md">
              <h4 className="text-sm font-semibold text-blue-900 mb-1">
                Thayer's Greek Lexicon
              </h4>
              <p className="text-blue-900 text-sm whitespace-pre-wrap">{entry.thayers}</p>
            </div>
          )}

          {/* Moulton-Milligan */}
          {entry.moulton_milligan && (
            <div className="bg-green-50 p-3 rounded-md">
              <h4 className="text-sm font-semibold text-green-900 mb-1">
                Moulton-Milligan Vocabulary
              </h4>
              <p className="text-green-900 text-sm whitespace-pre-wrap">
                {entry.moulton_milligan}
              </p>
            </div>
          )}

          {/* Morphology Statistics */}
          {(entry.tenses || entry.cases || entry.total_occurrences) && (
            <div className="bg-gray-50 p-3 rounded-md">
              <h4 className="text-sm font-semibold text-gray-700 mb-2">
                Morphology Statistics
              </h4>
              <div className="space-y-1 text-sm">
                {entry.total_occurrences && (
                  <p className="text-gray-700">
                    <span className="font-medium">Occurrences:</span> {entry.total_occurrences}
                  </p>
                )}
                {entry.tenses && entry.tenses.length > 0 && (
                  <p className="text-gray-700">
                    <span className="font-medium">Tenses:</span> {entry.tenses.join(', ')}
                  </p>
                )}
                {entry.cases && entry.cases.length > 0 && (
                  <p className="text-gray-700">
                    <span className="font-medium">Cases:</span> {entry.cases.join(', ')}
                  </p>
                )}
              </div>
            </div>
          )}

          {/* See Also */}
          {entry.see_also && entry.see_also.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-1">See Also</h4>
              <div className="flex flex-wrap gap-2">
                {entry.see_also.map((ref, index) => (
                  <button
                    key={index}
                    onClick={() => fetchLexiconEntry(ref)}
                    className="text-sm bg-blue-100 text-blue-700 px-2 py-1 rounded hover:bg-blue-200 transition"
                  >
                    {ref}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {!entry && !loading && !error && (
        <div className="text-center py-8 text-gray-500">
          <p>Click on a Greek word in the verse to see its lexicon entry</p>
          <p className="text-sm mt-2">Strong's numbers and definitions will appear here</p>
        </div>
      )}
    </div>
  );
};

export default LexiconPanel;
