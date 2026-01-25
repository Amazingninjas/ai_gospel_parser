#!/usr/bin/env python3
"""
Vincent's Word Studies Parser
=============================
Parses "Vincent's Word Studies in the New Testament" to extract structured 
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

class VincentWordStudiesParser:
    """
    Parser for Marvin R. Vincent's "Word Studies in the New Testament".
    """

    def __init__(self, file_path: str):
        """
        Initialize parser with source file path.

        Args:
            file_path: Path to vincent_word_studies.txt
        """
        self.file_path = Path(file_path)
        self.data = {}
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
            "name": "Vincent's Word Studies in the New Testament",
            "authors": "Marvin R. Vincent",
            "publication_years": "1887",
            "description": "Verse-by-verse etymological and word study commentary.",
            "focus": "Etymology, classical Greek, word history",
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
        Parse the Vincent's Word Studies text and return structured data.

        Returns:
            Dictionary containing data organized by book, chapter, and verse.
        """
        if not self.is_available():
            raise FileNotFoundError(f"Source file not found: {self.file_path}")

        print(f"Parsing Vincent's Word Studies from {self.file_path}...")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        parsed_data = {}
        verse_count = 0
        current_book = ""
        current_chapter = 0
        
        # Regex to identify book headers (e.g., "THE GOSPEL ACCORDING TO MATTHEW.")
        book_header_re = re.compile(r"THE GOSPEL ACCORDING TO\s+([A-Z]+)\.")
        # Regex for chapter headers (e.g., "CHAPTER I.")
        chapter_re = re.compile(r"CHAPTER\s+([IVXLC]+)\.")
        # Regex for verse references. This text often has verse numbers on their own line.
        verse_re = re.compile(r"^\s*(\d+)\s*$")

        for i, line in enumerate(lines):
            # Check for book header
            book_match = book_header_re.search(line)
            if book_match:
                book_name_raw = book_match.group(1).title()
                book_name = self.book_map.get(book_name_raw, book_name_raw)
                if book_name:
                    current_book = book_name
                    if current_book not in parsed_data:
                        parsed_data[current_book] = {}
                    current_chapter = 0 # Reset chapter on new book
                continue

            # Check for chapter header
            chapter_match = chapter_re.search(line)
            if chapter_match:
                # This is a roman numeral, we need to convert it. A simple dict is fine for this context.
                roman = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100}
                num = 0
                prev_val = 0
                for char in chapter_match.group(1):
                    val = roman[char]
                    num += val
                    if val > prev_val:
                        num -= 2 * prev_val
                    prev_val = val
                current_chapter = num
                if current_book and str(current_chapter) not in parsed_data[current_book]:
                    parsed_data[current_book][str(current_chapter)] = {}
                continue
                
            # Check for verse line
            verse_match = verse_re.match(line)
            if verse_match and current_book and current_chapter > 0:
                verse = int(verse_match.group(1))
                
                # The commentary for this verse is on the following lines, until the next verse number or chapter.
                commentary_lines = []
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    if verse_re.match(next_line) or chapter_re.search(next_line) or book_header_re.search(next_line):
                        break
                    commentary_lines.append(next_line.strip())
                
                commentary_text = " ".join(commentary_lines)

                # Extract Greek words and etymology
                greek_words = re.findall(r'[ιΙα-ωΑ-Ω\s]+', commentary_text)
                greek_words_normalized = [self._normalize_greek(word.strip()) for word in greek_words if word.strip()]
                
                etymology = [] # Vincent often has specific sections for this
                if "Etymology:" in commentary_text:
                    etymology_match = re.search(r"Etymology:(.*)", commentary_text)
                    if etymology_match:
                        etymology.append(etymology_match.group(1).strip())

                if str(verse) not in parsed_data[current_book][str(current_chapter)]:
                    parsed_data[current_book][str(current_chapter)][str(verse)] = []

                parsed_data[current_book][str(current_chapter)][str(verse)].append({
                    "book_name": current_book,
                    "chapter": current_chapter,
                    "verse": verse,
                    "word_study": commentary_text,
                    "greek_words": greek_words_normalized,
                    "etymology": etymology
                })
                verse_count += 1
        
        self.data = parsed_data
        print(f"✓ Parsed {verse_count} verse commentaries from Vincent's Word Studies.")
        return self.data
    
    def lookup_verse(self, book: str, chapter: int, verse: int) -> Optional[List[Dict]]:
        """
        Lookup a specific verse commentary.
        
        Args:
            book: The name of the book (e.g., "Matthew").
            chapter: The chapter number.
            verse: The verse number.

        Returns:
            A list of commentaries for the verse, or None if not found.
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
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        print(f"✓ Exported Vincent's Word Studies data to {output_file}")


def main():
    """Test the parser."""
    import sys

    default_path = Path(__file__).parent.parent / "vincent_word_studies" / "vincent_word_studies.txt"
    file_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    parser = VincentWordStudiesParser(file_path)

    print("Vincent's Word Studies Parser")
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
        
        sample = parser.lookup_verse("Matthew", 5, 3)
        if sample:
            print("Sample lookup for Matthew 5:3:")
            print(json.dumps(sample, indent=2))

        output_path = Path(__file__).parent.parent / "vincent_word_studies" / "vincent_word_studies_data.json"
        parser.export_to_json(output_path)

if __name__ == "__main__":
    main()
