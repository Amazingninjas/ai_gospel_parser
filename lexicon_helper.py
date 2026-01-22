#!/usr/bin/env python3
"""
Lexicon Helper - Fast In-Memory Lookups
========================================
Provides instant O(1) access to enhanced Thayer's lexicon without ChromaDB queries.

Usage:
    from lexicon_helper import ThayersLexicon

    lexicon = ThayersLexicon()
    entry = lexicon.lookup_by_strongs("G25")
    entries = lexicon.lookup_by_greek("ἀγαπάω")
    definition = lexicon.get_definition("G25", format='both')
    morph_summary = lexicon.get_morphology_summary("G25")

Author: AI Gospel Parser Project
Date: 2026-01-18
"""

import json
import os
import unicodedata
from typing import Dict, List, Optional, Union


class ThayersLexicon:
    """
    Fast in-memory access to enhanced Thayer's Greek Lexicon.

    Loads enhanced lexicon JSON into memory for instant lookups.
    Provides multiple access methods: by Strong's number, by Greek lemma, etc.
    """

    def __init__(self, json_path: str = "enhanced_lexicon.json"):
        """
        Initialize lexicon from JSON file.

        Args:
            json_path: Path to enhanced_lexicon.json file
        """
        self.json_path = json_path
        self.entries: Dict[str, dict] = {}  # strongs -> entry
        self.greek_index: Dict[str, List[str]] = {}  # lemma -> [strongs_ids]
        self.translit_index: Dict[str, List[str]] = {}  # transliteration -> [strongs_ids]

        self._load_lexicon()

    @staticmethod
    def normalize_greek(text: str) -> str:
        """Normalize Greek text to NFC form for consistent matching."""
        return unicodedata.normalize('NFC', text) if text else ''

    def _load_lexicon(self):
        """Load lexicon from JSON and build indices."""
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(
                f"Enhanced lexicon not found at {self.json_path}. "
                f"Run build_enhanced_lexicon.py first."
            )

        print(f"Loading enhanced lexicon from {self.json_path}...")

        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.entries = data

        # Build Greek index (with normalization)
        for strongs_id, entry in self.entries.items():
            lemma = self.normalize_greek(entry.get('lemma', ''))
            if lemma:
                if lemma not in self.greek_index:
                    self.greek_index[lemma] = []
                self.greek_index[lemma].append(strongs_id)

            # Build transliteration index
            translit = entry.get('transliteration', '')
            if translit:
                if translit not in self.translit_index:
                    self.translit_index[translit] = []
                self.translit_index[translit].append(strongs_id)

        print(f"  -> Loaded {len(self.entries)} entries")
        print(f"  -> Indexed {len(self.greek_index)} Greek lemmas")
        print(f"  -> Indexed {len(self.translit_index)} transliterations")

    def lookup_by_strongs(self, strongs_id: str) -> Optional[dict]:
        """
        Get lexicon entry by Strong's number.

        Args:
            strongs_id: Strong's number (e.g., "G25", "G3056", or just "25")

        Returns:
            Lexicon entry dict or None if not found
        """
        # Normalize input
        if strongs_id.isdigit():
            strongs_id = f"G{strongs_id}"
        elif not strongs_id.startswith('G'):
            strongs_id = f"G{strongs_id}"

        return self.entries.get(strongs_id, None)

    def lookup_by_greek(self, lemma: str) -> List[dict]:
        """
        Get all lexicon entries for a Greek lemma.

        Args:
            lemma: Greek word (e.g., "ἀγαπάω", "θεός")

        Returns:
            List of lexicon entries (usually 1, sometimes multiple for homographs)
        """
        normalized_lemma = self.normalize_greek(lemma)
        strongs_ids = self.greek_index.get(normalized_lemma, [])
        return [self.entries[sid] for sid in strongs_ids]

    def lookup_by_transliteration(self, translit: str) -> List[dict]:
        """
        Get all lexicon entries by transliteration.

        Args:
            translit: Transliterated Greek (e.g., "agapaō", "theós")

        Returns:
            List of lexicon entries
        """
        strongs_ids = self.translit_index.get(translit, [])
        return [self.entries[sid] for sid in strongs_ids]

    def get_definition(
        self,
        strongs_id: str,
        format: str = 'both'
    ) -> str:
        """
        Get formatted definition for a Strong's number.

        Args:
            strongs_id: Strong's number (e.g., "G25")
            format: Definition format
                - 'strongs': Strong's definition only
                - 'kjv': KJV definition only
                - 'both': Both definitions (default)
                - 'short': One-line summary

        Returns:
            Formatted definition string
        """
        entry = self.lookup_by_strongs(strongs_id)
        if not entry:
            return f"No entry found for {strongs_id}"

        if format == 'strongs':
            return entry.get('definition_strongs', 'No definition')

        elif format == 'kjv':
            return entry.get('definition_kjv', 'No definition')

        elif format == 'short':
            # Create one-line summary
            strongs_def = entry.get('definition_strongs', '')
            if strongs_def:
                # Take first sentence or first 100 chars
                short = strongs_def.split('.')[0] if '.' in strongs_def else strongs_def[:100]
                return short.strip()
            return entry.get('definition_kjv', 'No definition')

        else:  # 'both'
            strongs_def = entry.get('definition_strongs', '')
            kjv_def = entry.get('definition_kjv', '')
            parts = []
            if strongs_def:
                parts.append(f"Strong's: {strongs_def}")
            if kjv_def:
                parts.append(f"KJV: {kjv_def}")
            return '\n'.join(parts) if parts else 'No definition'

    def get_morphology_summary(self, strongs_id: str) -> str:
        """
        Get human-readable morphology summary.

        Args:
            strongs_id: Strong's number (e.g., "G25")

        Returns:
            Formatted morphology summary
        """
        entry = self.lookup_by_strongs(strongs_id)
        if not entry:
            return f"No entry found for {strongs_id}"

        morph = entry.get('morphology')
        if not morph:
            return "This word does not appear in the New Testament."

        lines = [f"Occurs {morph['total_occurrences']} times in the NT"]

        # Tenses (verbs)
        if morph.get('tenses'):
            top_tenses = sorted(morph['tenses'].items(), key=lambda x: -x[1])[:3]
            tenses_str = ', '.join(f"{t} ({c})" for t, c in top_tenses)
            lines.append(f"Common tenses: {tenses_str}")

        # Voices (verbs)
        if morph.get('voices'):
            voices_str = ', '.join(f"{v} ({c})" for v, c in sorted(morph['voices'].items(), key=lambda x: -x[1]))
            lines.append(f"Voices: {voices_str}")

        # Cases (nouns/adjectives)
        if morph.get('cases'):
            top_cases = sorted(morph['cases'].items(), key=lambda x: -x[1])[:3]
            cases_str = ', '.join(f"{c} ({cnt})" for c, cnt in top_cases)
            lines.append(f"Common cases: {cases_str}")

        # Number
        if morph.get('numbers'):
            numbers_str = ', '.join(f"{n} ({c})" for n, c in sorted(morph['numbers'].items(), key=lambda x: -x[1]))
            lines.append(f"Number: {numbers_str}")

        # Gender
        if morph.get('genders'):
            genders_str = ', '.join(f"{g} ({c})" for g, c in sorted(morph['genders'].items(), key=lambda x: -x[1]))
            lines.append(f"Gender: {genders_str}")

        return '\n'.join(lines)

    def get_all_forms(self, strongs_id: str) -> List[dict]:
        """
        Get all morphological forms found in the NT for this lemma.

        Args:
            strongs_id: Strong's number (e.g., "G25")

        Returns:
            List of sample forms with morphology
        """
        entry = self.lookup_by_strongs(strongs_id)
        if not entry or not entry.get('morphology'):
            return []

        return entry['morphology'].get('sample_forms', [])

    def explain_word_in_context(
        self,
        strongs_id: str,
        morph_code: Optional[str] = None
    ) -> str:
        """
        Explain a Greek word with its morphological form.

        Args:
            strongs_id: Strong's number (e.g., "G25")
            morph_code: Optional morphology code (e.g., "3IAI-S--")

        Returns:
            Human-readable explanation
        """
        entry = self.lookup_by_strongs(strongs_id)
        if not entry:
            return f"No entry found for {strongs_id}"

        lemma = entry.get('lemma', '')
        translit = entry.get('transliteration', '')
        pos = entry.get('part_of_speech', 'Unknown')

        explanation = f"{strongs_id} {lemma} ({translit})\n"
        explanation += f"Part of Speech: {pos}\n"
        explanation += f"\n{self.get_definition(strongs_id, format='short')}"

        if morph_code:
            explanation += f"\n\nForm: {morph_code}"
            # TODO: Parse morph_code and explain it
            # For now, just show it

        return explanation

    def search(self, query: str) -> List[dict]:
        """
        Simple search across lemma, transliteration, and definitions.

        Args:
            query: Search term

        Returns:
            List of matching entries
        """
        query_lower = query.lower()
        results = []

        for strongs_id, entry in self.entries.items():
            # Check lemma
            if query in entry.get('lemma', ''):
                results.append(entry)
                continue

            # Check transliteration
            if query_lower in entry.get('transliteration', '').lower():
                results.append(entry)
                continue

            # Check definitions
            if query_lower in entry.get('definition_strongs', '').lower():
                results.append(entry)
                continue

            if query_lower in entry.get('definition_kjv', '').lower():
                results.append(entry)
                continue

        return results

    def get_cross_references(self, strongs_id: str) -> List[dict]:
        """
        Get all cross-referenced words for a Strong's number.

        Args:
            strongs_id: Strong's number (e.g., "G25")

        Returns:
            List of cross-referenced lexicon entries
        """
        entry = self.lookup_by_strongs(strongs_id)
        if not entry:
            return []

        cross_refs = entry.get('cross_refs', [])
        return [self.lookup_by_strongs(ref) for ref in cross_refs if self.lookup_by_strongs(ref)]

    def __len__(self):
        """Return number of entries in lexicon."""
        return len(self.entries)

    def __contains__(self, strongs_id: str):
        """Check if Strong's number exists in lexicon."""
        if strongs_id.isdigit():
            strongs_id = f"G{strongs_id}"
        return strongs_id in self.entries


# --- CONVENIENCE FUNCTIONS ---

def quick_lookup(strongs_or_greek: str, lexicon: Optional[ThayersLexicon] = None) -> str:
    """
    Quick lookup function for command-line or REPL use.

    Args:
        strongs_or_greek: Either Strong's number ("G25") or Greek word ("ἀγαπάω")
        lexicon: Optional pre-loaded lexicon (creates new one if None)

    Returns:
        Formatted lexicon entry
    """
    if lexicon is None:
        lexicon = ThayersLexicon()

    # Try Strong's number first
    if strongs_or_greek.upper().startswith('G') or strongs_or_greek.isdigit():
        entry = lexicon.lookup_by_strongs(strongs_or_greek)
        if entry:
            return format_entry(entry)
        return f"No entry found for {strongs_or_greek}"

    # Try Greek lemma
    entries = lexicon.lookup_by_greek(strongs_or_greek)
    if entries:
        return '\n\n'.join(format_entry(e) for e in entries)

    # Try transliteration
    entries = lexicon.lookup_by_transliteration(strongs_or_greek)
    if entries:
        return '\n\n'.join(format_entry(e) for e in entries)

    return f"No entries found for '{strongs_or_greek}'"


def format_entry(entry: dict) -> str:
    """Format a lexicon entry for display."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"{entry['strongs']}: {entry['lemma']} ({entry.get('transliteration', '')})")
    lines.append(f"Part of Speech: {entry.get('part_of_speech', 'Unknown')}")

    if entry.get('definition_strongs'):
        lines.append(f"\nDefinition: {entry['definition_strongs']}")

    if entry.get('derivation'):
        lines.append(f"Etymology: {entry['derivation']}")

    if entry.get('morphology'):
        morph = entry['morphology']
        lines.append(f"\nOccurs {morph['total_occurrences']} times in the NT")

    lines.append(f"{'='*60}")
    return '\n'.join(lines)


# --- TESTING ---

if __name__ == "__main__":
    print("Testing ThayersLexicon...")

    # Initialize
    lex = ThayersLexicon()

    # Test lookups
    print("\n" + "="*60)
    print("TEST 1: Lookup by Strong's number (G25)")
    print("="*60)
    print(quick_lookup("G25", lex))

    print("\n" + "="*60)
    print("TEST 2: Lookup by Greek word (ἀγάπη)")
    print("="*60)
    print(quick_lookup("ἀγάπη", lex))

    print("\n" + "="*60)
    print("TEST 3: Get morphology summary (G3056 - λόγος)")
    print("="*60)
    print(lex.get_morphology_summary("G3056"))

    print("\n" + "="*60)
    print("TEST 4: Get cross-references (G25)")
    print("="*60)
    cross_refs = lex.get_cross_references("G25")
    for ref in cross_refs:
        print(f"  {ref['strongs']}: {ref['lemma']} - {ref.get('definition_strongs', '')[:50]}...")

    print("\n" + "="*60)
    print("TEST 5: Search for 'love'")
    print("="*60)
    results = lex.search("love")
    print(f"Found {len(results)} results:")
    for r in results[:5]:
        print(f"  {r['strongs']}: {r['lemma']} ({r.get('transliteration', '')})")

    print(f"\n✅ All tests complete! Lexicon has {len(lex)} entries.")
