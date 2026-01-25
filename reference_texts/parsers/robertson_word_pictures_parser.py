#!/usr/bin/env python3
"""
Robertson's Word Pictures Parser
================================
Parses " Robertson's Word Pictures in the New Testament" to extract structured 
verse-by-verse commentary.

This parser implements the modular reference text interface.

Author: AI Gospel Parser Project
Date: 2026-01-24
"""

import re
import json
from typing import Dict, List, Optional
from pathlib import Path
import unicodedata

class RobertsonWordPicturesParser:
    """
    Parser for A.T. Robertson's "Word Pictures in the New Testament".
    """

    def __init__(self, file_path: str):
        """
        Initialize parser with source file path.

        Args:
            file_path: Path to robertson_word_pictures.txt
        """
        self.file_path = Path(file_path)
        self.data = {}
        # A mapping of book names to a standard format could be useful
        self.book_map = {
            "Matthew": "Matthew", "Matt": "Matthew",
            "Mark": "Mark",
            "Luke": "Luke",
            "John": "John",
            "Acts": "Acts",
            "Romans": "Romans",
            "1 Corinthians": "1 Corinthians", "1 Cor": "1 Corinthians",
            "2 Corinthians": "2 Corinthians", "2 Cor": "2 Corinthians",
            "Galatians": "Galatians", "Gal": "Galatians",
            "Ephesians": "Ephesians", "Eph": "Ephesians",
            "Philippians": "Philippians", "Phil": "Philippians",
            "Colossians": "Colossians", "Col": "Colossians",
            "1 Thessalonians": "1 Thessalonians", "1 Thess": "1 Thessalonians",
            "2 Thessalonians": "2 Thessalonians", "2 Thess": "2 Thessalonians",
            "1 Timothy": "1 Timothy", "1 Tim": "1 Timothy",
            "2 Timothy": "2 Timothy", "2 Tim": "2 Timothy",
            "Titus": "Titus",
            "Philemon": "Philemon",
            "Hebrews": "Hebrews", "Heb": "Hebrews",
            "James": "James",
            "1 Peter": "1 Peter", "1 Pet": "1 Peter",
            "2 Peter": "2 Peter", "2 Pet": "2 Peter",
            "1 John": "1 John",
            "2 John": "2 John",
            "3 John": "3 John",
            "Jude": "Jude",
            "Revelation": "Revelation", "Rev": "Revelation"
        }


    def is_available(self) -> bool:
        """Check if source file exists."""
        return self.file_path.exists()

    def get_info(self) -> Dict[str, str]:
        """Return metadata about this text."""
        return {
            "name": " Robertson's Word Pictures in the New Testament",
            "authors": "A.T. Robertson",
            "publication_years": "1930-1933",
            "description": "Verse-by-verse Greek grammar and theological commentary.",
            "focus": "Grammar, syntax, theological interpretation",
            "source": "Internet Archive",
            "license": "Public Domain"
        }

    def _normalize_greek(self, text: str) -> str:
        """
        Normalize Greek text to NFC.
        """
        return unicodedata.normalize('NFC', text)

    def parse(self) -> Dict:
        """
        Parse the Robertson's Word Pictures text and return structured data.

        Returns:
            Dictionary containing data organized by book, chapter, and verse.
        """
        if not self.is_available():
            raise FileNotFoundError(f"Source file not found: {self.file_path}")

        print(f"Parsing Robertson's Word Pictures from {self.file_path}...")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to capture book, chapter, verse and the commentary
        # This is complex due to the OCR'd nature of the text.
        # It looks for "Book Chapter:Verse" patterns.
        verse_pattern = re.compile(
            r"^\s*([1-3]?\s*[A-Za-z]+)\s+([0-9]+:[0-9]+)\s*(.*)", re.MULTILINE
        )

        parsed_data = {}
        verse_count = 0
        
        current_book = ""
        current_chapter = ""

        # Using finditer for better control over matches
        for match in verse_pattern.finditer(content):
            book_name_raw, verse_ref, commentary_text = match.groups()
            
            # Normalize book name
            book_name = self.book_map.get(book_name_raw.strip())
            if not book_name:
                # This could be a chapter header or a mis-parsed line
                # Simple check to see if it's a book title line
                if "THE GOSPEL ACCORDING TO" in book_name_raw.upper():
                    potential_book = book_name_raw.upper().replace("THE GOSPEL ACCORDING TO", "").strip().title()
                    if potential_book in self.book_map:
                         current_book_explicit = self.book_map[potential_book]
                continue

            try:
                chapter, verse = verse_ref.split(':')
                chapter, verse = int(chapter), int(verse)
            except ValueError:
                continue

            # Handle book transitions
            if book_name != current_book:
                current_book = book_name
                parsed_data[current_book] = {}

            if str(chapter) not in parsed_data[current_book]:
                 parsed_data[current_book][str(chapter)] = {}

            # Extract Greek words (heuristic: often italicized or within parens)
            greek_words = re.findall(r'[ιΙα-ωΑ-Ω\s]+', commentary_text) # Simple regex for Greek chars
            greek_words_normalized = [self._normalize_greek(word.strip()) for word in greek_words if word.strip()]


            parsed_data[current_book][str(chapter)][str(verse)] = {
                "book_name": current_book,
                "chapter": chapter,
                "verse": verse,
                "commentary_text": commentary_text.strip(),
                "greek_words": greek_words_normalized,
            }
            verse_count += 1

        self.data = parsed_data
        print(f"✓ Parsed {verse_count} verses from Robertson's Word Pictures.")
        return self.data
    
    def lookup_verse(self, book: str, chapter: int, verse: int) -> Optional[Dict]:
        """
        Lookup a specific verse commentary.
        
        Args:
            book: The name of the book (e.g., "Matthew").
            chapter: The chapter number.
            verse: The verse number.

        Returns:
            A dictionary with the commentary, or None if not found.
        """
        if not self.data:
            self.parse()
            
        book_data = self.data.get(book)
        if not book_data:
            return None
        
        chapter_data = book_data.get(str(chapter))
        if not chapter_data:
            return None
            
        return chapter_data.get(str(verse))

    def export_to_json(self, output_path: str) -> None:
        """
        Export parsed data to JSON file.

        Args:
            output_path: Path to output JSON file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        print(f"✓ Exported Robertson's Word Pictures data to {output_file}")


def main():
    """Test the parser."""
    import sys

    default_path = Path(__file__).parent.parent / "robertson_word_pictures" / "robertson_word_pictures.txt"
    file_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    parser = RobertsonWordPicturesParser(file_path)

    print("Robertson's Word Pictures Parser")
    print("=" * 60)
    print(f"Source file: {parser.file_path}")
    print(f"Available: {parser.is_available()}")
    print()

    info = parser.get_info()
    print("Metadata:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()

    data = parser.parse()

    if data:
        print("\nSample Output:")
        print("-" * 60)
        
        # Show a sample from Matthew
        sample = parser.lookup_verse("Matthew", 5, 3)
        if sample:
            print("Sample lookup for Matthew 5:3:")
            print(json.dumps(sample, indent=2))

        # Show a sample from a later book
        sample_romans = parser.lookup_verse("Romans", 8, 28)
        if sample_romans:
            print("\nSample lookup for Romans 8:28:")
            print(json.dumps(sample_romans, indent=2))

        # Export to JSON
        output_path = Path(__file__).parent.parent / "robertson_word_pictures" / "robertson_word_pictures_data.json"
        parser.export_to_json(output_path)

if __name__ == "__main__":
    main()
