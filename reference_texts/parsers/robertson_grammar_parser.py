#!/usr/bin/env python3
"""
Robertson's Grammar Parser
===========================
Parses "A Grammar of the Greek New Testament in the Light of Historical Research"
by A.T. Robertson (1914) to extract grammatical topics and explanations.

This parser implements the modular reference text interface.

Author: AI Gospel Parser Project
Date: 2026-01-18
"""

import re
import json
import unicodedata
from typing import Dict, List, Optional
from pathlib import Path


class RobertsonGrammarParser:
    """
    Parser for Robertson's Grammar (1914).

    Extracts grammatical topics, explanations, and examples organized by
    morphological categories.
    """

    def __init__(self, file_path: str):
        """
        Initialize parser with source file path.

        Args:
            file_path: Path to robertson_grammar.txt
        """
        self.file_path = Path(file_path)
        self.topics = {}

    def is_available(self) -> bool:
        """Check if source file exists."""
        return self.file_path.exists()

    def get_info(self) -> Dict[str, str]:
        """Return metadata about this text."""
        return {
            "name": "Robertson's Grammar",
            "full_title": "A Grammar of the Greek New Testament in the Light of Historical Research",
            "author": "A.T. Robertson",
            "publication_year": "1914",
            "description": "Comprehensive NT Greek grammar with historical linguistics approach",
            "focus": "Syntax, morphology, historical development, Greek tenses/voices/moods",
            "source": "Archive.org DJVU text extraction",
            "license": "Public Domain"
        }

    @staticmethod
    def normalize_greek(text: str) -> str:
        """Normalize Greek text to NFC Unicode form."""
        if not text:
            return ""
        return unicodedata.normalize('NFC', text)

    @staticmethod
    def is_greek_text(text: str) -> bool:
        """Check if text contains Greek characters."""
        if not text:
            return False
        return bool(re.search(r'[\u0370-\u03FF]', text))

    def parse(self) -> Dict[str, dict]:
        """
        Parse Robertson's Grammar and return structured topical data.

        NOTE: Due to OCR quality issues in the source text, this parser
        creates a basic searchable index rather than perfect topic extraction.
        For production use, a higher-quality source text is recommended.

        Returns:
            Dictionary with full text and basic index
        """
        if not self.is_available():
            raise FileNotFoundError(f"Source file not found: {self.file_path}")

        print(f"Parsing Robertson's Grammar from {self.file_path}...")
        print("Note: OCR quality issues - creating searchable index...")

        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Due to OCR corruption, create a simpler structure:
        # - Store full text in manageable chunks
        # - Create keyword index for common grammatical terms
        # - Extract Greek examples where found

        # Split content into chunks of ~2000 characters
        chunk_size = 2000
        chunks = []
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            if len(chunk.strip()) > 100:  # Skip tiny chunks
                chunks.append({
                    'chunk_id': i // chunk_size,
                    'content': chunk,
                    'greek_examples': self._extract_greek_from_text(chunk)[:3]
                })

        # Create keyword index for grammatical concepts
        # Map common terms to chunk IDs where they appear
        grammatical_keywords = [
            'aorist', 'present', 'perfect', 'imperfect', 'future', 'pluperfect',
            'indicative', 'subjunctive', 'optative', 'imperative',
            'active', 'middle', 'passive',
            'nominative', 'genitive', 'dative', 'accusative', 'vocative',
            'participle', 'infinitive', 'article', 'pronoun', 'preposition',
            'syntax', 'morphology', 'verb', 'noun', 'adjective'
        ]

        keyword_index = {}
        for keyword in grammatical_keywords:
            keyword_index[keyword] = []
            for chunk in chunks:
                if keyword.lower() in chunk['content'].lower():
                    keyword_index[keyword].append(chunk['chunk_id'])

        # Store as a single resource
        self.topics['grammar_text'] = {
            'name': 'Robertson Grammar Full Text',
            'total_chunks': len(chunks),
            'chunks': chunks[:100],  # Limit to first 100 chunks to keep JSON manageable
            'keyword_index': {k: v[:10] for k, v in keyword_index.items() if v},  # Limit refs
            'description': 'Searchable grammar reference (OCR quality varies)',
            'source': 'Robertson Grammar (1914)'
        }

        # Also create topic-specific entries from keyword index
        for keyword, chunk_ids in keyword_index.items():
            if chunk_ids:
                relevant_chunks = [chunks[cid] for cid in chunk_ids[:3] if cid < len(chunks)]
                if relevant_chunks:
                    self.topics[keyword] = {
                        'topic': keyword.title(),
                        'chunk_ids': chunk_ids[:10],
                        'sample_content': relevant_chunks[0]['content'][:500] if relevant_chunks else '',
                        'greek_examples': relevant_chunks[0].get('greek_examples', []) if relevant_chunks else [],
                        'source': 'Robertson Grammar (1914)'
                    }

        print(f"✓ Created searchable index with {len(self.topics)} grammatical topics")
        print(f"✓ Indexed {len(chunks)} content chunks")
        return self.topics

    def _extract_topic_sections(self, content: str, topic: str) -> List[Dict[str, str]]:
        """
        Extract all sections related to a grammatical topic.

        Args:
            content: Full text content
            topic: Topic keyword to search for

        Returns:
            List of section dictionaries with heading and content
        """
        sections = []

        # Pattern to match topic headings (case insensitive, with optional Greek)
        # Look for topic in all caps or title case, possibly with Greek equiv.
        pattern = rf'(?:^|\n)([^\n]*{topic}[^\n]*?)(?:\n|$)'

        matches = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))

        for i, match in enumerate(matches):
            heading = match.group(1).strip()

            # Skip if heading is too long (probably not a real heading)
            if len(heading) > 200:
                continue

            # Get start and end positions for this section
            start_pos = match.end()

            # End is either next heading or next major section (3000 chars max)
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else start_pos + 3000
            end_pos = min(end_pos, start_pos + 3000)  # Limit section size

            section_content = content[start_pos:end_pos].strip()

            # Only include if there's substantial content
            if len(section_content) > 100:
                sections.append({
                    'heading': heading,
                    'content': section_content[:2000],  # Limit to 2000 chars
                    'greek_examples': self._extract_greek_from_text(section_content)[:5]
                })

        return sections[:10]  # Limit to 10 sections per topic

    def _count_greek_examples(self, sections: List[Dict]) -> int:
        """Count total Greek examples across sections."""
        count = 0
        for section in sections:
            count += len(section.get('greek_examples', []))
        return count

    def _extract_greek_from_text(self, text: str) -> List[str]:
        """Extract Greek text examples from content."""
        examples = []

        # Find Greek sequences (5+ consecutive Greek/space chars)
        greek_sequences = re.findall(r'[\u0370-\u03FF\s]{5,}', text)

        for seq in greek_sequences:
            seq = seq.strip()
            if seq and 5 <= len(seq) < 100:  # Reasonable length
                # Normalize and clean
                seq = self.normalize_greek(seq)
                seq = re.sub(r'\s+', ' ', seq)  # Normalize whitespace

                if seq not in examples:
                    examples.append(seq)

        return examples

    def lookup_by_topic(self, topic: str) -> Optional[dict]:
        """
        Look up grammatical topic.

        Args:
            topic: Grammatical topic (e.g., "aorist", "genitive", "participle")

        Returns:
            Topic dict or None if not found
        """
        return self.topics.get(topic.lower())

    def search_topics(self, keyword: str) -> List[str]:
        """
        Search for topics matching a keyword.

        Args:
            keyword: Search term

        Returns:
            List of matching topic names
        """
        keyword_lower = keyword.lower()
        matches = []

        for topic_key, topic_data in self.topics.items():
            # Search in topic name and section headings
            if keyword_lower in topic_key:
                matches.append(topic_key)
                continue

            for section in topic_data.get('sections', []):
                if keyword_lower in section.get('heading', '').lower():
                    matches.append(topic_key)
                    break

        return sorted(set(matches))

    def export_to_json(self, output_path: str) -> None:
        """
        Export parsed data to JSON file.

        Args:
            output_path: Path to output JSON file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.topics, f, ensure_ascii=False, indent=2)

        print(f"✓ Exported {len(self.topics)} topics to {output_file}")


def main():
    """Test the parser."""
    import sys

    # Default path
    default_path = Path(__file__).parent.parent / "robertson_grammar" / "robertson_grammar.txt"

    file_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    parser = RobertsonGrammarParser(file_path)

    print(f"Robertson's Grammar Parser")
    print(f"=" * 60)
    print(f"Source file: {parser.file_path}")
    print(f"Available: {parser.is_available()}")
    print()

    # Show metadata
    info = parser.get_info()
    print("Metadata:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()

    # Parse the file
    topics = parser.parse()
    print(f"\nTotal topics extracted: {len(topics)}")

    # Show sample topics
    print("\nSample topics:")
    print("-" * 60)
    sample_topics = [k for k in list(topics.keys())[:5] if k != 'grammar_text']
    for topic_key in sample_topics:
        topic = topics[topic_key]
        print(f"\n{topic.get('topic', topic_key)}:")
        if 'chunk_ids' in topic:
            print(f"  Found in {len(topic['chunk_ids'])} locations")
            print(f"  Greek examples: {len(topic.get('greek_examples', []))}")
            print(f"  Sample: {topic['sample_content'][:100]}...")

    # Test search functionality
    print("\n\nTesting search:")
    print("-" * 60)
    test_searches = ["aorist", "tense", "participle", "genitive"]
    for search_term in test_searches:
        matches = parser.search_topics(search_term)
        print(f"'{search_term}': {len(matches)} topics - {matches[:3]}")

    # Export to JSON
    output_path = Path(__file__).parent.parent / "robertson_grammar" / "robertson_grammar_topics.json"
    parser.export_to_json(output_path)


if __name__ == "__main__":
    main()
