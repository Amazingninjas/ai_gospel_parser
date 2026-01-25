#!/usr/bin/env python3
"""
Enhanced Lexicon Helper - Modular Reference Text System
========================================================
Provides unified access to multiple reference texts based on configuration.

Supports:
- Thayer's Greek Lexicon (core)
- Moulton-Milligan Vocabulary (idiomatic usage)
- Josephus Works (historical context)
- Robertson's Grammar (syntax) - when available

Usage:
    from enhanced_lexicon_helper import EnhancedLexiconHelper
    from reference_config import ReferenceTextConfig

    helper = EnhancedLexiconHelper(config=ReferenceTextConfig)

    # Lookup by Strong's number across all enabled texts
    results = helper.lookup_strongs("G25")
    # Returns: {'thayers': {...}, 'moulton_milligan': {...}}

    # Search for historical context
    context = helper.get_historical_context("Pilate")

Author: AI Gospel Parser Project
Date: 2026-01-18
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from reference_config import ReferenceTextConfig


class EnhancedLexiconHelper:
    """
    Unified interface to multiple reference texts.

    Loads only enabled texts based on configuration.
    """

    def __init__(self, config=ReferenceTextConfig):
        """
        Initialize helper with configuration.

        Args:
            config: ReferenceTextConfig class (not instance)
        """
        self.config = config
        self.thayers = None
        self.moulton_milligan = None
        self.josephus = None
        self.robertson = None
        self.robertson_word_pictures = None
        self.vincent_word_studies = None

        self._load_enabled_texts()

    def _load_enabled_texts(self):
        """Load only enabled reference texts."""
        print("Loading reference texts...")
        print(self.config.get_config_summary())
        print()

        # Load Thayer's lexicon (core)
        if self.config.THAYERS_ENABLED:
            try:
                thayers_path = "enhanced_lexicon.json"
                if os.path.exists(thayers_path):
                    with open(thayers_path, 'r', encoding='utf-8') as f:
                        self.thayers = json.load(f)
                    print(f"✓ Loaded Thayer's Lexicon ({len(self.thayers)} entries)")
                else:
                    print(f"⚠ Thayer's lexicon not found at {thayers_path}")
            except Exception as e:
                print(f"⚠ Error loading Thayer's: {e}")

        # Load Moulton-Milligan vocabulary
        if self.config.MOULTON_MILLIGAN_ENABLED:
            try:
                mm_path = "reference_texts/moulton_milligan/moulton_milligan_data.json"
                if os.path.exists(mm_path):
                    with open(mm_path, 'r', encoding='utf-8') as f:
                        self.moulton_milligan = json.load(f)
                    print(f"✓ Loaded Moulton-Milligan ({len(self.moulton_milligan)} entries)")
                else:
                    print(f"⚠ Moulton-Milligan data not found at {mm_path}")
            except Exception as e:
                print(f"⚠ Error loading Moulton-Milligan: {e}")

        # Load Josephus works
        if self.config.JOSEPHUS_ENABLED:
            try:
                josephus_path = "reference_texts/josephus/josephus_data.json"
                if os.path.exists(josephus_path):
                    with open(josephus_path, 'r', encoding='utf-8') as f:
                        self.josephus = json.load(f)
                    num_books = len([k for k in self.josephus.keys() if k.startswith('book_')])
                    print(f"✓ Loaded Josephus ({num_books} books)")
                else:
                    print(f"⚠ Josephus data not found at {josephus_path}")
            except Exception as e:
                print(f"⚠ Error loading Josephus: {e}")

        # Load Robertson's Grammar (if available and not corrupted)
        if self.config.ROBERTSON_GRAMMAR_ENABLED:
            try:
                robertson_path = "reference_texts/robertson_grammar/robertson_grammar_topics.json"
                if os.path.exists(robertson_path):
                    with open(robertson_path, 'r', encoding='utf-8') as f:
                        self.robertson = json.load(f)
                    print(f"✓ Loaded Robertson's Grammar ({len(self.robertson)} topics)")
                else:
                    print(f"⚠ Robertson's Grammar data not found at {robertson_path}")
            except Exception as e:
                print(f"⚠ Error loading Robertson's Grammar: {e}")

        # Load Robertson's Word Pictures
        if self.config.ROBERTSON_WORD_PICTURES_ENABLED:
            try:
                rwp_path = "reference_texts/robertson_word_pictures/robertson_word_pictures_data.json"
                if os.path.exists(rwp_path):
                    with open(rwp_path, 'r', encoding='utf-8') as f:
                        self.robertson_word_pictures = json.load(f)
                    print(f"✓ Loaded Robertson's Word Pictures")
                else:
                    print(f"⚠ Robertson's Word Pictures data not found at {rwp_path}")
            except Exception as e:
                print(f"⚠ Error loading Robertson's Word Pictures: {e}")

        # Load Vincent's Word Studies
        if self.config.VINCENT_WORD_STUDIES_ENABLED:
            try:
                vws_path = "reference_texts/vincent_word_studies/vincent_word_studies_data.json"
                if os.path.exists(vws_path):
                    with open(vws_path, 'r', encoding='utf-8') as f:
                        self.vincent_word_studies = json.load(f)
                    print(f"✓ Loaded Vincent's Word Studies")
                else:
                    print(f"⚠ Vincent's Word Studies data not found at {vws_path}")
            except Exception as e:
                print(f"⚠ Error loading Vincent's Word Studies: {e}")

        print()

    def lookup_strongs(self, strongs_id: str) -> Dict[str, dict]:
        """
        Look up Strong's number across all enabled texts.

        Args:
            strongs_id: Strong's number (e.g., "G25", "25")

        Returns:
            Dictionary with results from each enabled text
        """
        # Normalize Strong's ID
        if strongs_id.isdigit():
            strongs_id = f"G{strongs_id}"
        elif not strongs_id.startswith('G'):
            strongs_id = f"G{strongs_id}"

        results = {}

        # Thayer's lookup
        if self.thayers and strongs_id in self.thayers:
            results['thayers'] = self.thayers[strongs_id]

        # Moulton-Milligan lookup (by lemma via Thayer's)
        if self.moulton_milligan and self.thayers and strongs_id in self.thayers:
            lemma = self.thayers[strongs_id].get('lemma', '')
            if lemma and lemma in self.moulton_milligan:
                results['moulton_milligan'] = self.moulton_milligan[lemma]

        return results

    def get_historical_context(self, keyword: str) -> Optional[Dict]:
        """
        Search Josephus for historical/cultural context.

        Args:
            keyword: Person, place, or event (e.g., "Pilate", "Jerusalem")

        Returns:
            Dictionary with references to Josephus passages
        """
        if not self.josephus:
            return None

        topic_index = self.josephus.get('topic_index', {})
        keyword_lower = keyword.lower()

        if keyword_lower in topic_index:
            return {
                'keyword': keyword,
                'references': topic_index[keyword_lower],
                'count': len(topic_index[keyword_lower])
            }

        return None

    def get_grammar_context(self, topic: str) -> Optional[Dict]:
        """
        Search Robertson's Grammar for grammatical information.

        Args:
            topic: Grammatical topic (e.g., "aorist", "genitive")

        Returns:
            Grammar topic data if available
        """
        if not self.robertson:
            return None

        topic_lower = topic.lower()
        if topic_lower in self.robertson:
            return self.robertson[topic_lower]

        return None

    def lookup_verse_commentary(self, book: str, chapter: int, verse: int) -> Dict[str, dict]:
        """
        Look up verse commentary from enabled texts.

        Args:
            book: Name of the book.
            chapter: Chapter number.
            verse: Verse number.

        Returns:
            Dictionary with results from each enabled text.
        """
        results = {}
        # Robertson's Word Pictures lookup
        if self.robertson_word_pictures:
            book_data = self.robertson_word_pictures.get(book, {})
            chapter_data = book_data.get(str(chapter), {})
            verse_data = chapter_data.get(str(verse))
            if verse_data:
                results['robertson_word_pictures'] = verse_data

        # Vincent's Word Studies lookup
        if self.vincent_word_studies:
            book_data = self.vincent_word_studies.get(book, {})
            chapter_data = book_data.get(str(chapter), {})
            verse_data = chapter_data.get(str(verse))
            if verse_data:
                results['vincent_word_studies'] = verse_data

        return results

    def build_ai_context(self, strongs_numbers: List[str], keywords: List[str] = None, book: str = None, chapter: int = None, verse: int = None) -> str:
        """
        Build comprehensive AI context from all enabled texts.

        Args:
            strongs_numbers: List of Strong's numbers to look up
            keywords: Optional list of historical keywords (people, places, events)
            book: Optional book for verse-specific context.
            chapter: Optional chapter for verse-specific context.
            verse: Optional verse for verse-specific context.

        Returns:
            Formatted context string for AI
        """
        context_parts = []

        # Lexicon data (Thayer's + Moulton-Milligan)
        for strongs_id in strongs_numbers[:10]:  # Limit to 10 to avoid bloat
            lookup = self.lookup_strongs(strongs_id)

            if lookup:
                context_parts.append(f"\n**{strongs_id}:**")

                if 'thayers' in lookup:
                    entry = lookup['thayers']
                    context_parts.append(f"  Thayer's: {entry.get('definition', 'N/A')[:200]}")

                    # Add morphology if available
                    morph = entry.get('morphology_summary', {})
                    if morph:
                        context_parts.append(f"  Morphology: {morph}")

                if 'moulton_milligan' in lookup:
                    mm = lookup['moulton_milligan']
                    context_parts.append(f"  Moulton-Milligan: Papyri examples available")
                    if mm.get('papyri_citations'):
                        context_parts.append(f"    Citations: {', '.join(mm['papyri_citations'][:3])}")

        # Historical context (Josephus)
        if keywords and self.josephus:
            context_parts.append("\n**Historical Context (Josephus):**")
            for keyword in keywords[:5]:  # Limit to 5 keywords
                hist_context = self.get_historical_context(keyword)
                if hist_context:
                    context_parts.append(f"  {keyword}: {hist_context['count']} mentions in Josephus")

        # Verse Commentary
        if book and chapter and verse:
            commentaries = self.lookup_verse_commentary(book, chapter, verse)
            if commentaries:
                context_parts.append(f"\n**Commentary on {book} {chapter}:{verse}:**")
                if 'robertson_word_pictures' in commentaries:
                    rwp = commentaries['robertson_word_pictures']
                    context_parts.append(f"  Robertson's Word Pictures: {rwp.get('commentary_text', 'N/A')[:250]}...")
                if 'vincent_word_studies' in commentaries:
                    vws = commentaries['vincent_word_studies']
                    # Vincent can have multiple entries per verse
                    for entry in vws[:2]:
                        context_parts.append(f"  Vincent's Word Studies: {entry.get('word_study', 'N/A')[:250]}...")
        
        return '\n'.join(context_parts)


def main():
    """Test the enhanced helper."""
    print("Enhanced Lexicon Helper - Test")
    print("=" * 60)
    print()

    # Initialize with default config
    helper = EnhancedLexiconHelper()

    # Test Strong's lookup
    print("\n1. Testing Strong's lookup (G25 - agapao):")
    print("-" * 60)
    results = helper.lookup_strongs("G25")
    for source, data in results.items():
        print(f"\n{source.upper()}:")
        if source == 'thayers':
            print(f"  Lemma: {data.get('lemma', 'N/A')}")
            print(f"  Definition: {data.get('definition', 'N/A')[:100]}...")
        elif source == 'moulton_milligan':
            print(f"  Full text: {data.get('full_text', 'N/A')[:100]}...")

    # Test historical context
    print("\n\n2. Testing historical context (Pilate):")
    print("-" * 60)
    hist = helper.get_historical_context("Pilate")
    if hist:
        print(f"Keyword: {hist['keyword']}")
        print(f"Found {hist['count']} mentions in Josephus")
        print(f"Sample references: {hist['references'][:3]}")
    else:
        print("No historical context found (Josephus not loaded)")

    # Test AI context building
    print("\n\n3. Testing AI context building:")
    print("-" * 60)
    context = helper.build_ai_context(
        strongs_numbers=["G25", "G2316"],
        keywords=["Pilate", "Jerusalem"]
    )
    print(context)


if __name__ == "__main__":
    main()
