#!/usr/bin/env python3
"""
Vincent's Word Studies - HTML Parser (StudyLight Version)
==========================================================
Parses structured HTML files from StudyLight.org for Marvin R. Vincent's
Word Studies in the New Testament.

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
from html import unescape

class VincentWordStudiesHTMLParser:
    """
    Main parser for Vincent's Word Studies HTML files from StudyLight.org.
    """

    # Map StudyLight book names to standard names
    BOOK_MAP = {
        'matthew': 'Matthew',
        'mark': 'Mark',
        'luke': 'Luke',
        'john': 'John',
        'acts': 'Acts',
        'romans': 'Romans',
        '1-corinthians': '1 Corinthians',
        '2-corinthians': '2 Corinthians',
        'galatians': 'Galatians',
        'ephesians': 'Ephesians',
        'philippians': 'Philippians',
        'colossians': 'Colossians',
        '1-thessalonians': '1 Thessalonians',
        '2-thessalonians': '2 Thessalonians',
        '1-timothy': '1 Timothy',
        '2-timothy': '2 Timothy',
        'titus': 'Titus',
        'philemon': 'Philemon',
        'hebrews': 'Hebrews',
        'james': 'James',
        '1-peter': '1 Peter',
        '2-peter': '2 Peter',
        '1-john': '1 John',
        '2-john': '2 John',
        '3-john': '3 John',
        'jude': 'Jude',
        'revelation': 'Revelation'
    }

    def __init__(self, html_dir: str):
        """
        Initialize parser with HTML directory path.

        Args:
            html_dir: Path to directory containing StudyLight HTML files
        """
        self.html_dir = Path(html_dir)
        self.data = {}

    def is_available(self) -> bool:
        """Check if HTML directory exists."""
        return self.html_dir.exists() and self.html_dir.is_dir()

    def get_info(self) -> Dict[str, str]:
        """Return metadata about this text."""
        return {
            "name": "Vincent's Word Studies in the New Testament (StudyLight HTML)",
            "full_title": "Word Studies in the New Testament",
            "authors": "Marvin R. Vincent",
            "publication_years": "1886-1900",
            "description": "Verse-by-verse Greek word analysis with cultural and theological context",
            "focus": "Greek vocabulary, etymology, cultural nuances",
            "source": "StudyLight.org",
            "license": "Public Domain",
            "format": "Structured HTML"
        }

    def parse_chapter(self, html_file: Path) -> Dict[str, dict]:
        """
        Parse a single chapter HTML file.

        Args:
            html_file: Path to HTML chapter file

        Returns:
            Dictionary of {verse_number: verse_data}
        """
        verses = {}

        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()

        # Extract verse entries using the pattern:
        # <h3 class="commentaries-entry-number"><a name="verse-X"...>Verse X</a></h3>
        # followed by <P> tags with commentary

        # Find all verse headers
        verse_headers = re.finditer(
            r'<h3[^>]*><a name="verse-(\d+)"[^>]*>Verse \d+</a></h3>',
            html_content,
            re.IGNORECASE
        )

        header_positions = [(m.group(1), m.end()) for m in verse_headers]

        # Extract commentary for each verse
        for i, (verse_num, start_pos) in enumerate(header_positions):
            # Find where this verse's commentary ends (next verse header or end of file)
            if i + 1 < len(header_positions):
                end_pos = html_content.rfind('<h3', 0, header_positions[i + 1][1])
            else:
                # Last verse - find script tag or end
                end_pos = html_content.find('<script', start_pos)
                if end_pos == -1:
                    end_pos = len(html_content)

            # Extract the commentary section
            verse_html = html_content[start_pos:end_pos]

            # Extract all <P> tags (commentary text)
            paragraphs = re.findall(r'<P>(.*?)</[Pp]>', verse_html, re.DOTALL | re.IGNORECASE)

            if paragraphs:
                # Combine all paragraphs
                full_commentary = ' '.join(paragraphs)

                # Remove HTML tags
                commentary_text = re.sub(r'<[^>]+>', '', full_commentary)

                # Decode HTML entities
                commentary_text = unescape(commentary_text)

                # Clean up whitespace
                commentary_text = re.sub(r'\s+', ' ', commentary_text).strip()

                # Only save if we have substantial content
                if len(commentary_text) > 50:
                    verses[verse_num] = {
                        'verse_num': verse_num,
                        'commentary_text': commentary_text,
                        'word_count': len(commentary_text.split())
                    }

        return verses

    def parse(self) -> Dict:
        """
        Parse all HTML files and return structured data.

        Returns:
            Dictionary organized as: {book: {chapter: {verse: commentary}}}
        """
        if not self.is_available():
            raise FileNotFoundError(f"HTML directory not found: {self.html_dir}")

        print(f"Parsing Vincent's Word Studies HTML files from {self.html_dir}...")

        # Find all HTML files (e.g., "matthew-1.html", "john-3.html")
        html_files = sorted(self.html_dir.glob("*.html"))

        if not html_files:
            print(f"  ⚠ No HTML files found in {self.html_dir}")
            return self.data

        total_verses = 0
        total_chapters = 0

        for html_file in html_files:
            # Extract book and chapter from filename (e.g., "matthew-1.html")
            filename = html_file.stem  # "matthew-1"
            match = re.match(r'([a-z0-9-]+)-(\d+)', filename)

            if not match:
                continue

            book_slug, chapter = match.groups()
            book_name = self.BOOK_MAP.get(book_slug, book_slug.title())

            # Parse this chapter
            verses = self.parse_chapter(html_file)

            if verses:
                # Organize by book/chapter/verse
                if book_name not in self.data:
                    self.data[book_name] = {}

                if chapter not in self.data[book_name]:
                    self.data[book_name][chapter] = {}

                self.data[book_name][chapter] = verses
                total_verses += len(verses)
                total_chapters += 1

        print(f"✓ Parsed {total_verses} verses from Vincent's Word Studies (HTML).")
        print(f"  Books covered: {len(self.data)}")
        print(f"  Total chapters: {total_chapters}")

        return self.data

    def export_json(self, output_path: str):
        """Export parsed data to JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        print(f"✓ Exported Vincent's Word Studies (HTML) to {output_file}")

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
    print("Vincent's Word Studies HTML Parser (StudyLight)")
    print("=" * 60)

    # Path to StudyLight HTML files
    html_dir = Path(__file__).parent.parent / "vincent_word_studies" / "studylight_html"

    parser = VincentWordStudiesHTMLParser(html_dir)

    print(f"HTML directory: {html_dir}")
    print(f"Available: {parser.is_available()}")
    print()

    if not parser.is_available():
        print(f"✗ HTML directory not found. Please download StudyLight HTML files first.")
        return

    # Get metadata
    metadata = parser.get_info()
    print("Metadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    print()

    # Parse a few sample files
    sample_files = list(html_dir.glob("matthew-*.html"))[:3]
    if sample_files:
        print(f"Testing with {len(sample_files)} sample files:")
        for f in sample_files:
            print(f"  - {f.name}")
        print()

        # Create temporary parser for samples
        temp_parser = VincentWordStudiesHTMLParser(html_dir)
        temp_data = {}

        for html_file in sample_files:
            filename = html_file.stem
            match = re.match(r'([a-z0-9-]+)-(\d+)', filename)
            if match:
                book_slug, chapter = match.groups()
                book_name = temp_parser.BOOK_MAP.get(book_slug, book_slug.title())

                verses = temp_parser.parse_chapter(html_file)
                if verses:
                    if book_name not in temp_data:
                        temp_data[book_name] = {}
                    temp_data[book_name][chapter] = verses

        if temp_data:
            print()
            print("Sample Output:")
            print("-" * 60)

            # Show first book/chapter/verse
            first_book = list(temp_data.keys())[0]
            first_chapter = list(temp_data[first_book].keys())[0]
            first_verse = list(temp_data[first_book][first_chapter].keys())[0]

            sample = temp_data[first_book][first_chapter][first_verse]
            print(f"{first_book} {first_chapter}:{first_verse}")
            print(f"Word count: {sample['word_count']}")
            print(f"Commentary preview: {sample['commentary_text'][:200]}...")
    else:
        print("No HTML files found for testing.")


if __name__ == "__main__":
    main()
