#!/usr/bin/env python3
"""
Josephus Works Parser
======================
Parses "The Antiquities of the Jews" by Flavius Josephus (Whiston translation, 1737)
to extract structured data for historical and theological research.

This parser implements the modular reference text interface.

Author: AI Gospel Parser Project
Date: 2026-01-18
"""

import re
import json
from typing import Dict, List, Optional
from pathlib import Path

class JosephusParser:
    """
    Parser for Flavius Josephus' "The Antiquities of the Jews".
    """

    def __init__(self, file_path: str):
        """
        Initialize parser with source file path.

        Args:
            file_path: Path to josephus_whiston.txt
        """
        self.file_path = Path(file_path)
        self.data = {}
        self.topics = {
            'rulers': ['Herod', 'Pilate', 'Felix', 'Festus', 'Agrippa', 'Caesar'],
            'groups': ['Pharisees', 'Sadducees', 'Essenes', 'Zealots'],
            'places': ['Jerusalem', 'Temple', 'Galilee', 'Judea'],
            'events': ['revolt', 'famine', 'festival']
        }

    def is_available(self) -> bool:
        """Check if source file exists."""
        return self.file_path.exists()

    def get_info(self) -> Dict[str, str]:
        """Return metadata about this text."""
        return {
            "name": "The Antiquities of the Jews",
            "full_title": "The Antiquities of the Jews",
            "authors": "Flavius Josephus (translated by William Whiston)",
            "publication_years": "c. 94 AD (translation 1737)",
            "description": "A history of the Jewish people, from creation to the First Jewish-Roman War.",
            "focus": "Jewish history, 1st-century cultural and political context",
            "source": "Project Gutenberg",
            "license": "Public Domain"
        }

    def parse(self) -> Dict:
        """
        Parse the Josephus text and return structured data.

        Returns:
            Dictionary containing books, chapters, and a topic index.
        """
        if not self.is_available():
            raise FileNotFoundError(f"Source file not found: {self.file_path}")

        print(f"Parsing Josephus from {self.file_path}...")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the start of the actual content (skip TOC/Preface)
        content_start_match = re.search(r"BOOK I\.\s*Containing", content, re.IGNORECASE)
        if not content_start_match:
            print("Could not find the start of Book I. Parsing might be inaccurate.")
            content_start_index = 0
        else:
            # We need to find the actual start of chapter 1 content, not the TOC entry
            # Let's find the second occurence of the chapter
            chapter1_starts = [m.start() for m in re.finditer(r"CHAPTER 1. The Constitution Of The World", content, re.IGNORECASE)]
            if len(chapter1_starts) > 1:
                content_start_index = chapter1_starts[1]
            else:
                content_start_index = content_start_match.start()


        content = content[content_start_index:]
        
        # Split content into books
        # The split will be on "BOOK X." but also "ANTIQUITIES OF THE JEWS. BOOK XV."
        book_splits = re.split(r"(?:ANTIQUITIES OF THE JEWS\.\s*)?BOOK\s+[IVXLC]+\.", content)
        
        books_content = book_splits[1:] # first element is before the first book
        
        parsed_data = {}
        topic_index = {topic: [] for category in self.topics.values() for topic in category}


        book_num = 1
        for book_text in books_content:
            book_key = f"book_{book_num}"
            
            # Extract book title from the start of the text
            title_match = re.search(r"Containing The Interval Of.*", book_text)
            book_title = title_match.group(0).strip() if title_match else f"Book {book_num}"
            
            chapters_data = []
            book_topics = set()
            
            # Split book into chapters
            chapter_splits = re.split(r"CHAPTER\s+(\d+)\.", book_text)
            
            if len(chapter_splits) < 3:
                book_num += 1
                continue

            chapter_numbers = chapter_splits[1::2]
            chapters_content = chapter_splits[2::2]

            for i, chap_content in enumerate(chapters_content):
                chap_num = chapter_numbers[i]
                
                # Simple preview
                chap_content_cleaned = chap_content.strip().replace('\n', ' ')
                content_preview = ' '.join(chap_content_cleaned.split()[:50]) + "..."
                
                chapter_ref = f"{book_key}_chapter_{chap_num}"

                # Search for topics
                for category, keywords in self.topics.items():
                    for keyword in keywords:
                        if re.search(r'\b' + keyword + r'\b', chap_content, re.IGNORECASE):
                            topic_index.setdefault(keyword.lower(), []).append(chapter_ref)
                            book_topics.add(keyword.lower())
                
                chapters_data.append({
                    'chapter_num': chap_num,
                    'title': f"Chapter {chap_num}", # Titles are harder to extract reliably, using placeholder
                    'content_preview': content_preview,
                })

            parsed_data[book_key] = {
                'title': book_title,
                'chapters': chapters_data,
                'topics_mentioned': sorted(list(book_topics))
            }
            book_num += 1

        parsed_data['topic_index'] = topic_index
        self.data = parsed_data
        
        print(f"✓ Parsed {len(books_content)} books from Josephus.")
        return self.data

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

        print(f"✓ Exported Josephus data to {output_file}")


def main():
    """Test the parser."""
    import sys

    # Default path
    default_path = Path(__file__).parent.parent / "josephus" / "josephus_whiston.txt"

    file_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    parser = JosephusParser(file_path)

    print("Josephus Parser")
    print("=" * 60)
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
    data = parser.parse()

    if data:
        # Show sample output
        print("\nSample Output:")
        print("-" * 60)
        
        # Print info for the first book
        first_book_key = next(iter(data))
        if first_book_key != 'topic_index':
            first_book = data[first_book_key]
            print(f"Book: {first_book['title']}")
            print(f"  Chapters: {len(first_book['chapters'])}")
            print(f"  Topics: {first_book['topics_mentioned']}")
            if first_book['chapters']:
                print(f"  First chapter preview: {first_book['chapters'][0]['content_preview'][:100]}...")

        # Print some topic index data
        print("\nTopic Index Sample:")
        for topic, refs in data.get('topic_index', {}).items():
            if refs:
                print(f"  '{topic}': {len(refs)} mentions (e.g., {refs[0]})")
        
        # Export to JSON
        output_path = Path(__file__).parent.parent / "josephus" / "josephus_data.json"
        parser.export_to_json(output_path)

if __name__ == "__main__":
    main()
