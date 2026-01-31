"""
Lexicon Lookup Service
======================
Provides access to Thayer's Greek Lexicon with enhanced morphology data.
"""
import json
import os
from pathlib import Path
from typing import Optional
import unicodedata

from config import settings


class LexiconService:
    """
    Service for lexicon lookups using enhanced_lexicon.json.

    Loads the entire lexicon into memory on startup for fast O(1) lookups.
    """

    def __init__(self):
        """Initialize lexicon from JSON file"""
        self.entries = {}  # strongs -> entry
        self.greek_index = {}  # normalized greek -> list of strongs
        self.transliteration_index = {}  # transliteration -> list of strongs
        self._load_lexicon()

    def _normalize_greek(self, text: str) -> str:
        """Normalize Greek text for consistent matching"""
        if not text:
            return ""
        # Strip punctuation
        text = text.strip('.,;:·⸀')
        # Unicode normalization (NFD to decompose, then NFC to recompose)
        # This handles different accent representations
        normalized = unicodedata.normalize('NFD', text)
        # Strip combining diacriticals (accents) for broader matching
        stripped = ''.join(
            char for char in normalized
            if unicodedata.category(char) != 'Mn'  # Mn = Mark, Nonspacing
        )
        # Normalize back to NFC and lowercase
        normalized = unicodedata.normalize('NFC', stripped)
        return normalized.lower().strip()

    def _load_lexicon(self):
        """Load enhanced lexicon from JSON file"""
        lexicon_path = settings.ENHANCED_LEXICON_PATH

        if not os.path.exists(lexicon_path):
            print(f"⚠ Enhanced lexicon not found at: {lexicon_path}")
            print(f"   Run 'python build_enhanced_lexicon.py' to create it")
            return

        try:
            with open(lexicon_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Build indexes
            for strongs, entry in data.items():
                self.entries[strongs] = entry

                # Greek lemma index
                lemma = entry.get('lemma', '')
                if lemma:
                    normalized = self._normalize_greek(lemma)
                    if normalized not in self.greek_index:
                        self.greek_index[normalized] = []
                    self.greek_index[normalized].append(strongs)

                # Transliteration index
                translit = entry.get('transliteration', '')
                if translit:
                    translit_key = translit.lower().strip()
                    if translit_key not in self.transliteration_index:
                        self.transliteration_index[translit_key] = []
                    self.transliteration_index[translit_key].append(strongs)

            print(f"✓ Loaded lexicon ({len(self.entries)} entries)")

        except Exception as e:
            print(f"⚠ Error loading lexicon: {e}")

    def lookup_by_strongs(self, strongs_number: str) -> Optional[dict]:
        """
        Look up entry by Strong's number.

        Args:
            strongs_number: Strong's number (e.g., 'G25', 'g25', '25')

        Returns:
            Lexicon entry dict or None if not found
        """
        # Normalize Strong's number format
        strongs_number = strongs_number.strip().upper()
        if not strongs_number.startswith('G'):
            strongs_number = f"G{strongs_number}"

        return self.entries.get(strongs_number)

    def lookup_by_greek(self, greek_word: str) -> list[dict]:
        """
        Look up entries by Greek lemma.

        Args:
            greek_word: Greek word (e.g., 'ἀγαπάω')

        Returns:
            List of matching entries (may be multiple for same lemma)
        """
        normalized = self._normalize_greek(greek_word)
        strongs_numbers = self.greek_index.get(normalized, [])

        return [
            self.entries[strongs]
            for strongs in strongs_numbers
            if strongs in self.entries
        ]

    def lookup_by_transliteration(self, transliteration: str) -> list[dict]:
        """
        Look up entries by transliteration.

        Args:
            transliteration: Transliterated Greek (e.g., 'agapao')

        Returns:
            List of matching entries
        """
        translit_key = transliteration.lower().strip()
        strongs_numbers = self.transliteration_index.get(translit_key, [])

        return [
            self.entries[strongs]
            for strongs in strongs_numbers
            if strongs in self.entries
        ]

    def search(self, query: str, limit: int = 20) -> list[tuple[dict, float]]:
        """
        Full-text search across lexicon entries.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of (entry, relevance_score) tuples, sorted by relevance
        """
        query_lower = query.lower().strip()
        results = []

        for strongs, entry in self.entries.items():
            score = 0.0

            # Check Strong's number (exact match = highest score)
            if strongs.lower() == f"g{query_lower}" or strongs.lower() == query_lower:
                score += 100.0

            # Check lemma (high score for exact match)
            lemma = entry.get('lemma', '')
            if lemma and query_lower in self._normalize_greek(lemma):
                score += 50.0

            # Check transliteration (high score)
            translit = entry.get('transliteration', '')
            if translit and query_lower in translit.lower():
                score += 40.0

            # Check definitions (medium score)
            definition_strongs = entry.get('definition_strongs', '')
            if definition_strongs and query_lower in definition_strongs.lower():
                score += 20.0

            definition_kjv = entry.get('definition_kjv', '')
            if definition_kjv and query_lower in definition_kjv.lower():
                score += 15.0

            # Check derivation (low score)
            derivation = entry.get('derivation', '')
            if derivation and query_lower in derivation.lower():
                score += 5.0

            if score > 0:
                results.append((entry, score))

        # Sort by relevance score (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        # Return top results
        return results[:limit]

    def get_all_entries(self, limit: Optional[int] = None) -> list[dict]:
        """
        Get all lexicon entries.

        Args:
            limit: Optional limit on number of entries

        Returns:
            List of all entries (or first N if limited)
        """
        entries = list(self.entries.values())

        if limit:
            return entries[:limit]
        return entries

    def get_stats(self) -> dict:
        """
        Get lexicon statistics.

        Returns:
            Dict with stats (total entries, etc.)
        """
        return {
            "total_entries": len(self.entries),
            "entries_with_morphology": sum(
                1 for e in self.entries.values()
                if e.get('morphology')
            ),
            "parts_of_speech": list(set(
                e.get('part_of_speech', 'Unknown')
                for e in self.entries.values()
            ))
        }


# Singleton instance
_lexicon_service = None

def get_lexicon_service() -> LexiconService:
    """Get singleton instance of LexiconService (dependency injection)"""
    global _lexicon_service
    if _lexicon_service is None:
        _lexicon_service = LexiconService()
    return _lexicon_service
