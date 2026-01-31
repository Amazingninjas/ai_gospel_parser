export interface LexiconEntry {
  strongs_number: string;
  greek: string;
  transliteration: string;
  pronunciation: string;
  definition: string;
  usage: string;
  derivation?: string;

  // Morphology statistics
  tenses?: string[];
  cases?: string[];
  total_occurrences?: number;

  // Enhanced definitions
  thayers?: string;
  moulton_milligan?: string;

  // Related entries
  see_also?: string[];
}

export interface LexiconSearchResult {
  entries: LexiconEntry[];
  total: number;
}
