#!/usr/bin/env python3
"""
Quick test to verify English reference layer integration.
Tests that WEB English text is properly aligned with Greek SBLGNT.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gospel_parser_interlinear import load_web_bible, CODE_TO_BOOK

def test_web_loading():
    """Test that WEB Bible loads correctly"""
    print("=" * 60)
    print("TEST 1: Loading World English Bible")
    print("=" * 60)

    english_lookup = load_web_bible()

    if not english_lookup:
        print("❌ FAIL: No English verses loaded")
        return False

    print(f"✓ Loaded {len(english_lookup)} verses")

    # Test specific verses
    test_verses = [
        (43, 1, 1, "John 1:1"),  # John 1:1
        (43, 3, 16, "John 3:16"), # John 3:16
        (45, 8, 28, "Romans 8:28"), # Romans 8:28
    ]

    print("\nSample verses:")
    for book, chapter, verse, ref in test_verses:
        key = (book, chapter, verse)
        english = english_lookup.get(key, "")

        if english:
            print(f"\n{ref}:")
            print(f"  {english[:80]}...")
        else:
            print(f"\n❌ {ref}: NOT FOUND")
            return False

    print("\n✓ TEST 1 PASSED\n")
    return True

def test_verse_alignment():
    """Test that English aligns with known Greek verses"""
    print("=" * 60)
    print("TEST 2: Verse Alignment")
    print("=" * 60)

    english_lookup = load_web_bible()

    # Known verses to check
    checks = [
        {
            "ref": "John 1:1",
            "book": 43, "chapter": 1, "verse": 1,
            "expected_keywords": ["beginning", "Word", "God"]
        },
        {
            "ref": "John 3:16",
            "book": 43, "chapter": 3, "verse": 16,
            "expected_keywords": ["God", "loved", "world", "Son"]
        },
        {
            "ref": "1 John 4:8",
            "book": 62, "chapter": 4, "verse": 8,
            "expected_keywords": ["God", "love"]
        }
    ]

    for check in checks:
        key = (check["book"], check["chapter"], check["verse"])
        english = english_lookup.get(key, "").lower()

        if not english:
            print(f"❌ {check['ref']}: NOT FOUND")
            return False

        missing = [kw for kw in check["expected_keywords"] if kw.lower() not in english]

        if missing:
            print(f"❌ {check['ref']}: Missing keywords {missing}")
            print(f"   Got: {english}")
            return False

        print(f"✓ {check['ref']}: {english[:60]}...")

    print("\n✓ TEST 2 PASSED\n")
    return True

def test_coverage():
    """Test NT coverage"""
    print("=" * 60)
    print("TEST 3: New Testament Coverage")
    print("=" * 60)

    english_lookup = load_web_bible()

    # Count verses per book
    book_counts = {}
    for (book, chapter, verse), text in english_lookup.items():
        if book not in book_counts:
            book_counts[book] = 0
        book_counts[book] += 1

    expected_books = range(40, 67)  # Matthew (40) through Revelation (66)

    print(f"\nBooks loaded: {len(book_counts)}/27 NT books")

    missing = []
    for book_code in expected_books:
        if book_code not in book_counts:
            missing.append(CODE_TO_BOOK.get(book_code, f"Book {book_code}"))

    if missing:
        print(f"❌ Missing books: {', '.join(missing)}")
        return False

    # Show some statistics
    total_verses = sum(book_counts.values())
    print(f"✓ All 27 NT books present")
    print(f"✓ Total verses: {total_verses}")
    print(f"\nSample counts:")
    for book_code in [40, 43, 45, 66]:  # Matthew, John, Romans, Revelation
        book_name = CODE_TO_BOOK[book_code]
        count = book_counts.get(book_code, 0)
        print(f"  {book_name}: {count} verses")

    print("\n✓ TEST 3 PASSED\n")
    return True

def main():
    print("\n" + "=" * 60)
    print("English Reference Layer Integration Tests")
    print("=" * 60 + "\n")

    # Check if WEB directory exists
    if not os.path.exists("web_bible_json"):
        print("❌ ERROR: web_bible_json/ directory not found")
        print("   Please run: python download_web_bible.py")
        return 1

    tests = [
        test_web_loading,
        test_verse_alignment,
        test_coverage
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ TEST EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(tests)}")
        return 1
    else:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nEnglish reference layer is properly integrated.")
        print("Ready to run: python gospel_parser_interlinear.py")
        return 0

if __name__ == "__main__":
    sys.exit(main())
