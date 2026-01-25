#!/usr/bin/env python3
"""
Robertson's Word Pictures - HTML Parser (CCEL Version)
=======================================================
Parses structured HTML files from Christian Classics Ethereal Library (CCEL)
for A.T. Robertson's Word Pictures in the New Testament.

This parser handles the clean, structured HTML format which provides MUCH better
extraction than the OCR DjVu text files.

Author: AI Gospel Parser Project
Date: 2026-01-24
"""

import re
import json
import os
from typing import Dict, List, Optional
from pathlib import Path
from html.parser import HTMLParser
from html import unescape

class RobertsonHTMLParser(HTMLParser):
    """
    HTML parser for extracting verse commentary from Robertson's Word Pictures CCEL HTML files.
    """

    def __init__(self):
        super().__init__()
        self.current_verse = None
        self.current_commentary = []
        self.in_paragraph = False
        self.verses = {}

    def handle_starttag(self, tag, attrs):
        """Handle opening HTML tags."""
        if tag == 'p':
            self.in_paragraph = True
            self.current_commentary = []

    def handle_endtag(self, tag):
        """Handle closing HTML tags."""
        if tag == 'p' and self.in_paragraph:
            self.in_paragraph = False
            # Save the verse if we found one
            if self.current_verse and self.current_commentary:
                commentary_text = ' '.join(self.current_commentary).strip()
                if len(commentary_text) > 50:  # Filter out very short entries
                    self.verses[self.current_verse] = commentary_text

    def handle_data(self, data):
        """Handle text data within tags."""
        if self.in_paragraph:
            # Check if this starts with a verse number (e.g., "1:1 ", "12:34 ")
            verse_match = re.match(r'^(\d+):(\d+)\s+', data)
            if verse_match:
                chapter, verse = verse_match.groups()
                self.current_verse = f"{chapter}:{verse}"
                # Get the rest of the text after the verse number
                remaining_text = data[verse_match.end():].strip()
                if remaining_text:
                    self.current_commentary.append(remaining_text)
            elif self.current_verse:
                # Continue adding to current commentary
                text = data.strip()
                if text:
                    self.current_commentary.append(text)


class RobertsonWordPicturesHTMLParser:
    """
    Main parser for Robertson's Word Pictures HTML files from CCEL.
    """

    # Map CCEL file prefixes to full book names
    BOOK_MAP = {
        'MT': 'Matthew',
        'MR': 'Mark',
        'LU': 'Luke',
        'JOH': 'John',
        'AC': 'Acts',
        'RO': 'Romans',
        '1CO': '1 Corinthians',
        '2CO': '2 Corinthians',
        'GA': 'Galatians',
        'EPH': 'Ephesians',
        'PHP': 'Philippians',
        'COL': 'Colossians',
        '1TH': '1 Thessalonians',
        '2TH': '2 Thessalonians',
        '1TI': '1 Timothy',
        '2TI': '2 Timothy',
        'TIT': 'Titus',
        'PHM': 'Philemon',
        'HEB': 'Hebrews',
        'JAS': 'James',
        '1PE': '1 Peter',
        '2PE': '2 Peter',
        '1JO': '1 John',
        '2JO': '2 John',
        '3JO': '3 John',
        'JUDE': 'Jude',
        'RE': 'Revelation'
    }

    def __init__(self, html_dir: str):
        """
        Initialize parser with HTML directory path.

        Args:
            html_dir: Path to directory containing CCEL HTML files
        """
        self.html_dir = Path(html_dir)
        self.data = {}

    def is_available(self) -> bool:
        """Check if HTML directory exists."""
        return self.html_dir.exists() and self.html_dir.is_dir()

    def get_info(self) -> Dict[str, str]:
        """Return metadata about this text."""
        return {
            "name": "Robertson's Word Pictures in the New Testament (CCEL HTML)",
            "full_title": "Word Pictures in the New Testament",
            "authors": "A.T. Robertson",
            "publication_years": "1930-1933",
            "description": "Verse-by-verse Greek grammar and theological commentary (parsed from CCEL HTML)",
            "focus": "Grammar, syntax, theological interpretation",
            "source": "Christian Classics Ethereal Library (CCEL)",
            "license": "Public Domain",
            "format": "Structured HTML"
        }

    def parse(self) -> Dict:
        """
        Parse all HTML files and return structured data.

        Returns:
            Dictionary organized as: {book: {chapter: {verse: commentary}}}
        """
        if not self.is_available():
            raise FileNotFoundError(f"HTML directory not found: {self.html_dir}")

        print(f"Parsing Robertson's Word Pictures HTML files from {self.html_dir}...")

        # Find all .RWP.html files
        html_files = sorted(self.html_dir.glob("*.RWP.html"))

        if not html_files:
            print(f"  ⚠ No .RWP.html files found in {self.html_dir}")
            return self.data

        total_verses = 0

        for html_file in html_files:
            # Extract book and chapter from filename (e.g., "MT1.RWP.html" -> Matthew 1)
            filename = html_file.stem  # "MT1.RWP"
            match = re.match(r'([A-Z0-9]+?)(\d+)\.RWP', filename)

            if not match:
                continue

            book_code, chapter = match.groups()
            book_name = self.BOOK_MAP.get(book_code, book_code)

            # Read HTML file
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            # Extract the main content paragraph (between <p> and </BODY>)
            content_match = re.search(r'<p>(.+?)</BODY>', html_content, re.DOTALL | re.IGNORECASE)
            if not content_match:
                continue

            content = content_match.group(1)

            # Verses are separated by patterns like:
            #   1:1 <B>{Title}</B> ...commentary...
            #   1:2 <B>{Title}</B> ...commentary...
            # Each verse starts with CHAPTER:VERSE followed by optional whitespace and <B>
            verse_pattern = re.compile(
                r'\s*(\d+):(\d+)\s+<B>(.+?)(?=\s*\d+:\d+\s+<B>|$)',
                re.DOTALL | re.IGNORECASE
            )

            # Organize by book/chapter/verse
            if book_name not in self.data:
                self.data[book_name] = {}

            if chapter not in self.data[book_name]:
                self.data[book_name][chapter] = {}

            # Find all verses in this chapter
            for match in verse_pattern.finditer(content):
                ch_num, v_num, commentary_html = match.groups()

                # Verify chapter matches filename
                if ch_num != chapter:
                    continue

                # Clean up the commentary HTML
                commentary_text = commentary_html

                # Remove HTML tags
                commentary_text = re.sub(r'<[^>]+>', '', commentary_text)

                # Decode HTML entities
                commentary_text = unescape(commentary_text)

                # Clean up whitespace
                commentary_text = re.sub(r'\s+', ' ', commentary_text).strip()

                # Only save if we have substantial content
                if len(commentary_text) > 50:
                    self.data[book_name][chapter][v_num] = {
                        'verse': f"{ch_num}:{v_num}",
                        'commentary_text': commentary_text,
                        'book': book_name,
                        'chapter': chapter,
                        'verse_num': v_num
                    }
                    total_verses += 1

        print(f"✓ Parsed {total_verses} verses from Robertson's Word Pictures (HTML).")
        print(f"  Books covered: {len(self.data)}")
        print(f"  Total chapters: {sum(len(self.data[b]) for b in self.data)}")

        return self.data

    def export_json(self, output_path: str):
        """Export parsed data to JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        print(f"✓ Exported Robertson's Word Pictures (HTML) to {output_file}")

    def lookup_verse(self, book: str, chapter: int, verse: int) -> Optional[Dict]:
        """
        Look up commentary for a specific verse.

        Args:
            book: Book name (e.g., "Matthew", "Romans")
            chapter: Chapter number
            verse: Verse number

        Returns:
            Dictionary with verse commentary or None
        """
        chapter_str = str(chapter)
        verse_str = str(verse)

        if book in self.data and chapter_str in self.data[book]:
            return self.data[book][chapter_str].get(verse_str)

        return None


def main():
    """Test the HTML parser."""
    print("Robertson's Word Pictures HTML Parser (CCEL)")
    print("=" * 60)

    # Path to CCEL HTML files
    html_dir = Path(__file__).parent.parent / "robertson_word_pictures" / "ccel_html"

    parser = RobertsonWordPicturesHTMLParser(html_dir)

    print(f"HTML directory: {html_dir}")
    print(f"Available: {parser.is_available()}")
    print()

    if not parser.is_available():
        print(f"✗ HTML directory not found. Please download CCEL HTML files first.")
        return

    # Get metadata
    metadata = parser.get_info()
    print("Metadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    print()

    # Parse all HTML files
    data = parser.parse()

    if data:
        print()
        print("Sample Output:")
        print("-" * 60)

        # Show first book/chapter/verse
        first_book = list(data.keys())[0]
        first_chapter = list(data[first_book].keys())[0]
        first_verse = list(data[first_book][first_chapter].keys())[0]

        sample = data[first_book][first_chapter][first_verse]
        print(f"{first_book} {first_chapter}:{first_verse}")
        print(f"Commentary: {sample['commentary_text'][:200]}...")

        # Export to JSON
        output_path = html_dir.parent / "robertson_word_pictures_data_html.json"
        parser.export_json(output_path)
    else:
        print("⚠ No data parsed from HTML files")


if __name__ == "__main__":
    main()
