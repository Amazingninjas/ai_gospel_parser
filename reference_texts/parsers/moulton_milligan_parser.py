#!/usr/bin/env python3
"""
Moulton-Milligan Vocabulary Parser
===================================
Parses "The Vocabulary of the Greek Testament" by Moulton & Milligan
to extract papyri examples and idiomatic usages of Koine Greek words.

This parser implements the modular reference text interface.

Author: AI Gospel Parser Project
Date: 2026-01-18
"""

import re
import json
import unicodedata
from typing import Dict, List, Optional
from pathlib import Path


class MoultonMilliganParser:
    """
    Parser for Moulton-Milligan Vocabulary (1914-1929).

    Extracts Greek lexical entries with papyri citations and idiomatic examples.
    """

    def __init__(self, file_path: str):
        """
        Initialize parser with source file path.

        Args:
            file_path: Path to moulton_milligan_vocab.txt
        """
        self.file_path = Path(file_path)
        self.entries = {}

    def is_available(self) -> bool:
        """Check if source file exists."""
        return self.file_path.exists()

    def get_info(self) -> Dict[str, str]:
        """Return metadata about this text."""
        return {
            "name": "Moulton-Milligan Vocabulary",
            "full_title": "The Vocabulary of the Greek Testament Illustrated from the Papyri and Other Non-Literary Sources",
            "authors": "James Hope Moulton, D.D., D.Theol. and George Milligan, D.D.",
            "publication_years": "1914-1929",
            "description": "Greek NT vocabulary illustrated from contemporary papyri and inscriptions",
            "focus": "Idiomatic usage, papyri examples, cultural context",
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
    def is_greek_word(text: str) -> bool:
        """Check if text is a Greek word (contains Greek characters)."""
        if not text:
            return False
        # Greek Unicode range: 0370-03FF
        return bool(re.search(r'[\u0370-\u03FF]', text))

    def parse(self) -> Dict[str, dict]:
        """
        Parse the Moulton-Milligan text and return structured data.

        Returns:
            Dictionary mapping Greek lemmas to entry data
        """
        if not self.is_available():
            raise FileNotFoundError(f"Source file not found: {self.file_path}")

        print(f"Parsing Moulton-Milligan from {self.file_path}...")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find where vocabulary entries start (after front matter)
        # The vocabulary proper starts after all the introductory material
        # Look for the section header pattern that indicates start of main content
        start_idx = 0
        for i, line in enumerate(lines):
            # Look for a line that marks the start of the main vocabulary
            # Typically after "GENERAL INTRODUCTION" and abbreviations lists
            if i > 3000 and self.is_greek_word(line.strip()) and len(line.strip()) < 20:
                # Found first real entry after substantial front matter
                start_idx = i
                break

        current_lemma = None
        current_content = []
        entries_found = 0

        for i in range(start_idx, len(lines)):
            line = lines[i].strip()

            # Skip empty lines
            if not line:
                continue

            # Check if this line is a Greek word heading
            # Greek headings are typically standalone Greek words at the start of entries
            if self._is_entry_heading(line):
                # Save previous entry
                if current_lemma and current_content:
                    self._save_entry(current_lemma, current_content)
                    entries_found += 1

                # Start new entry
                current_lemma = self.normalize_greek(line.strip().rstrip('.'))
                current_content = []

            elif current_lemma:
                # Accumulate content for current entry
                current_content.append(line)

        # Save last entry
        if current_lemma and current_content:
            self._save_entry(current_lemma, current_content)
            entries_found += 1

        print(f"✓ Parsed {entries_found} Moulton-Milligan entries")
        return self.entries

    def _is_entry_heading(self, line: str) -> bool:
        """
        Determine if a line is a Greek word entry heading.

        Entry headings are:
        - Greek text only (no Latin characters)
        - Usually one word
        - May end with a period
        - Not too long (< 30 chars)
        - Not just Roman numerals or single letters
        """
        if not line or len(line) > 30 or len(line) < 2:
            return False

        # Remove trailing period
        test_line = line.rstrip('.')

        # Must contain Greek
        if not self.is_greek_word(test_line):
            return False

        # Should not contain Latin letters, numbers, or common citation markers
        if re.search(r'[a-zA-Z0-9()]', test_line):
            return False

        # Should not start with common prefixes from references
        if any(test_line.startswith(prefix) for prefix in ['P ', 'BGU', 'Syll', 'OG/S']):
            return False

        # Reject obvious page numbers/section markers (single Greek letters, Roman numerals in Greek)
        # Real entries should be actual words with multiple characters
        if len(test_line) <= 3:
            # Allow only if it's a real short word, not a marker
            # Greek Roman numerals use: Ι, Χ, Ξ, Λ, etc.
            # If it's just these, it's probably a page marker
            if all(c in 'ΙΧΞΛΜ' for c in test_line):
                return False

        return True

    def _save_entry(self, lemma: str, content_lines: List[str]):
        """
        Process and save an entry.

        Args:
            lemma: Greek word (normalized)
            content_lines: Lines of content for this entry
        """
        full_text = ' '.join(content_lines)

        # Extract papyri citations
        papyri_citations = self._extract_papyri_citations(full_text)

        # Extract NT references
        nt_references = self._extract_nt_references(full_text)

        # Extract example usages (Greek text within the content)
        examples = self._extract_greek_examples(content_lines)

        # Create structured entry
        self.entries[lemma] = {
            'lemma': lemma,
            'full_text': full_text[:2000],  # Limit to 2000 chars to avoid huge entries
            'papyri_citations': papyri_citations[:10],  # Limit to 10 citations
            'nt_references': nt_references,
            'examples': examples[:5],  # Limit to 5 examples
            'source': 'Moulton-Milligan Vocabulary (1914-1929)'
        }

    def _extract_papyri_citations(self, text: str) -> List[str]:
        """
        Extract papyri citations from text.

        Common patterns:
        - P Oxy III. 471 (ii/A.D.)
        - BGU I. 267 (A.D. 199)
        - P Tebt I. 104 (B.C. 92)
        """
        citations = []

        # Pattern for papyri references
        pattern = r'(P\s+[A-Za-z]+|BGU|Syll|OG/S|PSI)\s+[IVX]+\.\s*\d+[a-z]*(?:\s*\([^)]+\))?'

        matches = re.finditer(pattern, text)
        for match in matches:
            citation = match.group(0)
            if citation not in citations:  # Avoid duplicates
                citations.append(citation)

        return citations

    def _extract_nt_references(self, text: str) -> List[str]:
        """
        Extract New Testament references from text.

        Patterns:
        - Mt 19:7, Mk 3:8, Lk 12:3, Jn 1:18
        - Rom 3:9, 1 Cor 5:9, Heb 5:9
        - Ac 25:7
        """
        references = []

        # Common NT book abbreviations used in Moulton-Milligan
        nt_books = r'(?:Mt|Mk|Lk|Jn|Ac|Rom|1\s*Cor|2\s*Cor|Gal|Eph|Phil|Col|1\s*Th|2\s*Th|1\s*Tim|2\s*Tim|Tit|Philem|Heb|Jas|1\s*Pet|2\s*Pet|1\s*Jn|2\s*Jn|3\s*Jn|Jude|Rev)'

        pattern = rf'{nt_books}\s+\d+[:\d]*'

        matches = re.finditer(pattern, text)
        for match in matches:
            ref = match.group(0)
            if ref not in references:
                references.append(ref)

        return references

    def _extract_greek_examples(self, content_lines: List[str]) -> List[str]:
        """
        Extract Greek text examples from content.

        These are Greek phrases/sentences within the English text,
        typically showing idiomatic usage.
        """
        examples = []

        for line in content_lines:
            # Find Greek text sequences (5+ consecutive Greek chars)
            greek_sequences = re.findall(r'[\u0370-\u03FF\s]{5,}', line)

            for seq in greek_sequences:
                seq = seq.strip()
                if seq and len(seq) < 200:  # Reasonable length
                    # Normalize and clean
                    seq = self.normalize_greek(seq)
                    seq = re.sub(r'\s+', ' ', seq)  # Normalize whitespace

                    if seq not in examples:
                        examples.append(seq)

        return examples

    def lookup_by_lemma(self, lemma: str) -> Optional[dict]:
        """
        Look up entry by Greek lemma.

        Args:
            lemma: Greek word to look up

        Returns:
            Entry dict or None if not found
        """
        normalized = self.normalize_greek(lemma)
        return self.entries.get(normalized)

    def link_to_strongs(self, thayers_lexicon_path: str) -> None:
        """
        Link Moulton-Milligan entries to Strong's numbers via Thayer's lexicon.

        Args:
            thayers_lexicon_path: Path to enhanced_lexicon.json from Thayer's integration
        """
        print(f"Linking to Strong's numbers via Thayer's lexicon...")

        # Load Thayer's data
        thayers_file = Path(thayers_lexicon_path)
        if not thayers_file.exists():
            print(f"⚠ Thayer's lexicon not found at {thayers_file}")
            print("  Skipping Strong's number linking")
            return

        with open(thayers_file, 'r', encoding='utf-8') as f:
            thayers_data = json.load(f)

        # Build Greek lemma → Strong's number index
        lemma_to_strongs = {}
        for strongs_id, entry in thayers_data.items():
            lemma = entry.get('lemma', '')
            if lemma:
                normalized = self.normalize_greek(lemma)
                if normalized not in lemma_to_strongs:
                    lemma_to_strongs[normalized] = []
                lemma_to_strongs[normalized].append(strongs_id)

        # Link Moulton-Milligan entries to Strong's
        linked_count = 0
        for lemma, entry in self.entries.items():
            strongs_numbers = lemma_to_strongs.get(lemma, [])
            if strongs_numbers:
                entry['strongs_numbers'] = strongs_numbers
                linked_count += 1

        print(f"✓ Linked {linked_count}/{len(self.entries)} entries to Strong's numbers")

    def export_to_json(self, output_path: str) -> None:
        """
        Export parsed data to JSON file.

        Args:
            output_path: Path to output JSON file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

        print(f"✓ Exported {len(self.entries)} entries to {output_file}")


def main():
    """Test the parser."""
    import sys

    # Default path
    default_path = Path(__file__).parent.parent / "moulton_milligan" / "moulton_milligan_vocab.txt"

    file_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    parser = MoultonMilliganParser(file_path)

    print(f"Moulton-Milligan Parser")
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
    entries = parser.parse()
    print(f"\nTotal entries parsed: {len(entries)}")

    # Link to Strong's numbers via Thayer's lexicon
    thayers_path = Path(__file__).parent.parent.parent / "enhanced_lexicon.json"
    parser.link_to_strongs(str(thayers_path))

    # Show sample entries
    print("\nSample entries:")
    print("-" * 60)
    sample_words = list(entries.keys())[:5]
    for word in sample_words:
        entry = entries[word]
        print(f"\n{word}:")
        print(f"  Strong's: {entry.get('strongs_numbers', 'None')}")
        print(f"  Papyri citations: {len(entry['papyri_citations'])}")
        print(f"  NT references: {entry['nt_references']}")
        print(f"  Examples: {len(entry['examples'])}")
        if entry['examples']:
            print(f"  First example: {entry['examples'][0][:80]}...")

    # Export to JSON
    output_path = Path(__file__).parent.parent / "moulton_milligan" / "moulton_milligan_data.json"
    parser.export_to_json(output_path)


if __name__ == "__main__":
    main()
