/**
 * Greek Text Utilities
 *
 * Helper functions for working with Greek text in the New Testament.
 */

/**
 * Normalize Greek text for consistent display
 * Handles Unicode normalization and cleanup
 */
export const normalizeGreekText = (text: string): string => {
  if (!text) return '';

  // Normalize to NFC (Canonical Composition)
  // This ensures consistent representation of accented characters
  return text.normalize('NFC').trim();
};

/**
 * Remove diacritical marks from Greek text
 * Useful for searching/matching
 */
export const removeDiacritics = (text: string): string => {
  if (!text) return '';

  // Decompose to NFD, then filter out combining marks
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove combining diacritical marks
    .normalize('NFC');
};

/**
 * Check if text contains Greek characters
 */
export const containsGreek = (text: string): boolean => {
  if (!text) return false;

  // Greek and Coptic: U+0370 to U+03FF
  // Greek Extended: U+1F00 to U+1FFF
  const greekRegex = /[\u0370-\u03FF\u1F00-\u1FFF]/;
  return greekRegex.test(text);
};

/**
 * Split Greek text into words
 * Handles Greek-specific punctuation
 */
export const splitGreekWords = (text: string): string[] => {
  if (!text) return [];

  // Split on whitespace and common Greek punctuation
  return text
    .split(/[\s·]+/) // Split on spaces and middle dot
    .map(word => word.trim())
    .filter(word => word.length > 0);
};

/**
 * Clean Greek word for lookup
 * Removes punctuation and normalizes
 */
export const cleanGreekWord = (word: string): string => {
  if (!word) return '';

  // Remove common punctuation marks
  return word
    .replace(/[.,;:·⸀⸁]/g, '')
    .trim();
};

/**
 * Format Strong's number
 * Ensures consistent G prefix
 */
export const formatStrongsNumber = (number: string): string => {
  if (!number) return '';

  const cleaned = number.trim().toUpperCase();
  if (cleaned.startsWith('G')) {
    return cleaned;
  }
  return `G${cleaned}`;
};

/**
 * Parse verse reference
 * Converts "John 3:16" to { book: "John", chapter: 3, verse: 16 }
 */
export const parseVerseReference = (ref: string): {
  book: string;
  chapter: number;
  verse: number;
} | null => {
  if (!ref) return null;

  // Pattern: Book Chapter:Verse
  const pattern = /^(\d*\s*[A-Za-z]+)\s+(\d+):(\d+)$/;
  const match = ref.trim().match(pattern);

  if (!match) return null;

  return {
    book: match[1].trim(),
    chapter: parseInt(match[2], 10),
    verse: parseInt(match[3], 10),
  };
};

/**
 * Format verse reference for display
 */
export const formatVerseReference = (book: string, chapter: number, verse: number): string => {
  return `${book} ${chapter}:${verse}`;
};

/**
 * Truncate Greek text with ellipsis
 * Useful for previews
 */
export const truncateGreekText = (text: string, maxLength: number = 100): string => {
  if (!text || text.length <= maxLength) return text;

  // Try to break at word boundary
  const truncated = text.substring(0, maxLength);
  const lastSpace = truncated.lastIndexOf(' ');

  if (lastSpace > maxLength * 0.8) {
    return truncated.substring(0, lastSpace) + '...';
  }

  return truncated + '...';
};
