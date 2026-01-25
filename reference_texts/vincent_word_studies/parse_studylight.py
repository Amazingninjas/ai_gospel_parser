#!/usr/bin/env python3
"""
Parse all Vincent's Word Studies HTML files from StudyLight.org
and export to JSON.
"""

import sys
from pathlib import Path

# Add parsers directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'parsers'))

from vincent_word_studies_html_parser import VincentWordStudiesHTMLParser

def main():
    html_dir = Path(__file__).parent / "studylight_html"
    output_file = Path(__file__).parent / "vincent_word_studies_data_studylight.json"

    print("=" * 70)
    print("Vincent's Word Studies - Complete Parse (StudyLight HTML)")
    print("=" * 70)
    print()

    parser = VincentWordStudiesHTMLParser(html_dir)

    if not parser.is_available():
        print(f"✗ HTML directory not found: {html_dir}")
        return 1

    # Get metadata
    metadata = parser.get_info()
    print("Source Information:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    print()

    # Parse all files
    data = parser.parse()

    if not data:
        print("⚠ No data parsed!")
        return 1

    # Export to JSON
    parser.export_json(output_file)

    # Statistics
    total_verses = sum(
        len(data[book][chapter])
        for book in data
        for chapter in data[book]
    )

    total_words = sum(
        data[book][chapter][verse].get('word_count', 0)
        for book in data
        for chapter in data[book]
        for verse in data[book][chapter]
    )

    print()
    print("=" * 70)
    print("Parse Complete!")
    print("=" * 70)
    print(f"  Books: {len(data)}")
    print(f"  Chapters: {sum(len(data[b]) for b in data)}")
    print(f"  Verses: {total_verses}")
    print(f"  Total words: {total_words:,}")
    print(f"  Average words per verse: {total_words / total_verses:.0f}")
    print()
    print(f"Output file: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
    print("=" * 70)

    return 0

if __name__ == "__main__":
    sys.exit(main())
