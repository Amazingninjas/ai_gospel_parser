"""
Verse Lookup Service
====================
Wraps existing gospel_parser_interlinear.py logic for API use.
"""
import sys
import os
from pathlib import Path
from typing import Optional
import chromadb

# Add parent directory to path to import existing code
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import settings


class VerseService:
    """
    Service for verse lookups using existing ChromaDB and SBLGNT data.

    This wraps the logic from gospel_parser_interlinear.py in a reusable service.
    """

    # Bible book mapping (from gospel_parser_interlinear.py)
    BIBLE_BOOKS = {
        # New Testament
        "matthew": {"code": 61, "abbrev": ["mt", "matt", "mat"]},
        "mark": {"code": 62, "abbrev": ["mk", "mar"]},
        "luke": {"code": 63, "abbrev": ["lk", "luk", "lu"]},
        "john": {"code": 64, "abbrev": ["jn", "joh"]},
        "acts": {"code": 65, "abbrev": ["ac", "act"]},
        "romans": {"code": 66, "abbrev": ["ro", "rom", "rm"]},
        "1 corinthians": {"code": 67, "abbrev": ["1co", "1cor", "1 cor"]},
        "2 corinthians": {"code": 68, "abbrev": ["2co", "2cor", "2 cor"]},
        "galatians": {"code": 69, "abbrev": ["ga", "gal"]},
        "ephesians": {"code": 70, "abbrev": ["eph", "ephes"]},
        "philippians": {"code": 71, "abbrev": ["php", "phil", "pp"]},
        "colossians": {"code": 72, "abbrev": ["col"]},
        "1 thessalonians": {"code": 73, "abbrev": ["1th", "1thes", "1thess", "1 thess", "1 th"]},
        "2 thessalonians": {"code": 74, "abbrev": ["2th", "2thes", "2thess", "2 thess", "2 th"]},
        "1 timothy": {"code": 75, "abbrev": ["1ti", "1tim", "1 tim", "1 ti"]},
        "2 timothy": {"code": 76, "abbrev": ["2ti", "2tim", "2 tim", "2 ti"]},
        "titus": {"code": 77, "abbrev": ["tit", "ti"]},
        "philemon": {"code": 78, "abbrev": ["phm", "philem", "pm"]},
        "hebrews": {"code": 79, "abbrev": ["heb", "he"]},
        "james": {"code": 80, "abbrev": ["jas", "jam", "jm"]},
        "1 peter": {"code": 81, "abbrev": ["1pe", "1pet", "1pt", "1 pet", "1 pe"]},
        "2 peter": {"code": 82, "abbrev": ["2pe", "2pet", "2pt", "2 pet", "2 pe"]},
        "1 john": {"code": 83, "abbrev": ["1jn", "1jo", "1j", "1 joh", "1 john"]},
        "2 john": {"code": 84, "abbrev": ["2jn", "2jo", "2j", "2 joh", "2 john"]},
        "3 john": {"code": 85, "abbrev": ["3jn", "3jo", "3j", "3 joh", "3 john"]},
        "jude": {"code": 86, "abbrev": ["jud", "jd"]},
        "revelation": {"code": 87, "abbrev": ["re", "rev", "rv"]},
    }

    # Reverse lookup: code to book name
    CODE_TO_BOOK = {info["code"]: name.title() for name, info in BIBLE_BOOKS.items()}

    def __init__(self):
        """Initialize ChromaDB connection (singleton pattern)"""
        self.chroma_client = None
        self.collection = None
        self.web_bible_cache = {}  # Cache for WEB Bible JSON
        self._initialize_db()

    def _initialize_db(self):
        """Initialize ChromaDB client and collection"""
        try:
            self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
            self.collection = self.chroma_client.get_collection(name="gospel_interlinear")
            print(f"✓ Connected to ChromaDB ({self.collection.count()} documents)")
        except Exception as e:
            print(f"⚠ Error initializing ChromaDB: {e}")
            print(f"   Make sure ChromaDB exists at: {settings.CHROMA_DB_PATH}")
            raise

    def parse_verse_reference(self, ref_string: str) -> Optional[dict | list[dict]]:
        """
        Parse verse references like:
        - 'John 3:16' → {'book': 64, 'chapter': 3, 'verse': 16}
        - 'John 3:16-18' → [{'book': 64, 'chapter': 3, 'verse': 16}, ...]
        - '1 John 2:1' → {'book': 83, 'chapter': 2, 'verse': 1}

        Returns: dict or list of dicts with verse info, or None if invalid
        """
        import re

        ref_string = ref_string.strip().lower()

        # Pattern: (optional number + space) + book name + chapter:verse(-verse)?
        pattern = r'^(\d+\s+)?([a-z]+)\s+(\d+):(\d+)(?:-(\d+))?$'
        match = re.match(pattern, ref_string)

        if not match:
            return None

        num_prefix, book_name, chapter, start_verse, end_verse = match.groups()

        # Build full book name
        full_book_name = f"{num_prefix.strip()} {book_name}" if num_prefix else book_name
        full_book_name = full_book_name.strip()

        # Find book code
        book_code = None
        for book, info in self.BIBLE_BOOKS.items():
            if book == full_book_name or full_book_name in info["abbrev"]:
                book_code = info["code"]
                break

        if not book_code:
            return None

        chapter = int(chapter)
        start_verse = int(start_verse)

        # Handle verse range
        if end_verse:
            end_verse = int(end_verse)
            return [
                {"book": book_code, "book_name": self.CODE_TO_BOOK[book_code],
                 "chapter": chapter, "verse": v}
                for v in range(start_verse, end_verse + 1)
            ]
        else:
            return {
                "book": book_code,
                "book_name": self.CODE_TO_BOOK[book_code],
                "chapter": chapter,
                "verse": start_verse
            }

    def format_reference_id(self, book: int, chapter: int, verse: int) -> str:
        """Formats a reference ID like '64-03-16' for John 3:16"""
        return f"{book:02d}-{chapter:02d}-{verse:02d}"

    def get_english_text(self, book: int, chapter: int, verse: int) -> str:
        """
        Get English text from WEB Bible JSON files.

        Args:
            book: SBLGNT book code (61-87)
            chapter: Chapter number
            verse: Verse number

        Returns:
            English text or empty string if not found
        """
        # Map SBLGNT codes (61-87) to WEB codes (40-66)
        # SBLGNT NT: 61-87, WEB NT: 40-66
        web_book_code = book - 21  # 61 → 40, 64 → 43, etc.

        # Load WEB Bible JSON if not cached
        if web_book_code not in self.web_bible_cache:
            web_bible_path = project_root / "web_bible_json"

            try:
                import glob
                import json

                # Find JSON file for this book
                files = glob.glob(str(web_bible_path / f"{web_book_code}-*.json"))
                if files:
                    with open(files[0], 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Build verse lookup dict: (chapter, verse) -> text
                        verse_dict = {}
                        for item in data:
                            if item.get('type') == 'paragraph text':
                                ch = item.get('chapterNumber')
                                vs = item.get('verseNumber')
                                text = item.get('value', '').strip()
                                if ch and vs and text:
                                    verse_dict[(ch, vs)] = text
                        self.web_bible_cache[web_book_code] = verse_dict
                else:
                    print(f"⚠ WEB Bible JSON not found for book {web_book_code}")
                    self.web_bible_cache[web_book_code] = {}
                    return ""
            except Exception as e:
                print(f"⚠ Error loading WEB Bible JSON: {e}")
                self.web_bible_cache[web_book_code] = {}
                return ""

        # Look up verse from cache
        verse_dict = self.web_bible_cache.get(web_book_code, {})
        return verse_dict.get((chapter, verse), "")

        # Look up verse
        book_data = self.web_bible_cache.get(web_book_code, {})
        chapters = book_data.get('chapters', [])

        if chapter <= len(chapters):
            chapter_data = chapters[chapter - 1]
            if verse <= len(chapter_data):
                return chapter_data[verse - 1]

        return ""

    def lookup_verse(self, verse_ref: dict) -> Optional[tuple[str, dict]]:
        """
        Look up a specific verse by reference.

        Args:
            verse_ref: dict with 'book', 'chapter', 'verse' keys

        Returns:
            Tuple of (text, metadata) or (None, None) if not found
        """
        ref_id = self.format_reference_id(
            verse_ref['book'],
            verse_ref['chapter'],
            verse_ref['verse']
        )

        try:
            results = self.collection.get(where={"reference_id": ref_id})

            if results['documents']:
                metadata = results['metadatas'][0]

                # Add English text from WEB Bible
                english_text = self.get_english_text(
                    verse_ref['book'],
                    verse_ref['chapter'],
                    verse_ref['verse']
                )
                metadata['english_text'] = english_text

                return results['documents'][0], metadata
            return None, None
        except Exception as e:
            print(f"Error looking up verse {ref_id}: {e}")
            return None, None

    def get_all_books(self) -> list[dict]:
        """
        Get list of all Bible books.

        Returns:
            List of dicts with book info (name, code, abbreviations)
        """
        books = []
        for name, info in sorted(self.BIBLE_BOOKS.items(), key=lambda x: x[1]["code"]):
            books.append({
                "name": name.title(),
                "code": info["code"],
                "abbreviations": info["abbrev"]
            })
        return books


# Singleton instance
_verse_service = None

def get_verse_service() -> VerseService:
    """Get singleton instance of VerseService (dependency injection)"""
    global _verse_service
    if _verse_service is None:
        _verse_service = VerseService()
    return _verse_service
