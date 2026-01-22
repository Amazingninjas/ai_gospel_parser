#!/usr/bin/env python3
"""
Downloads World English Bible (WEB) New Testament JSON files from GitHub.
Source: https://github.com/TehShrike/world-english-bible

Public Domain - No copyright restrictions.
"""

import os
import json
import urllib.request
import sys

# GitHub raw content base URL
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/"

# Output directory
OUTPUT_DIR = "web_bible_json"

# New Testament books (matching SBLGNT book codes)
NT_BOOKS = {
    40: "matthew",
    41: "mark",
    42: "luke",
    43: "john",
    44: "acts",
    45: "romans",
    46: "1corinthians",
    47: "2corinthians",
    48: "galatians",
    49: "ephesians",
    50: "philippians",
    51: "colossians",
    52: "1thessalonians",
    53: "2thessalonians",
    54: "1timothy",
    55: "2timothy",
    56: "titus",
    57: "philemon",
    58: "hebrews",
    59: "james",
    60: "1peter",
    61: "2peter",
    62: "1john",
    63: "2john",
    64: "3john",
    65: "jude",
    66: "revelation",
}

def download_file(url, output_path):
    """Downloads a file from URL to output_path"""
    try:
        print(f"  Downloading: {os.path.basename(output_path)}", end="")
        with urllib.request.urlopen(url) as response:
            data = response.read()
        with open(output_path, 'wb') as f:
            f.write(data)
        print(" ✓")
        return True
    except urllib.error.HTTPError as e:
        print(f" ✗ (HTTP {e.code})")
        return False
    except Exception as e:
        print(f" ✗ ({e})")
        return False

def main():
    print("=" * 60)
    print("World English Bible (WEB) - New Testament Downloader")
    print("=" * 60)
    print(f"Source: {GITHUB_RAW_BASE}")
    print(f"Output: {OUTPUT_DIR}/")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Download each NT book
    success_count = 0
    fail_count = 0

    for book_code, book_name in NT_BOOKS.items():
        url = f"{GITHUB_RAW_BASE}{book_name}.json"
        output_path = os.path.join(OUTPUT_DIR, f"{book_code:02d}-{book_name}.json")

        if download_file(url, output_path):
            success_count += 1
        else:
            fail_count += 1

    # Summary
    print()
    print("=" * 60)
    print(f"✓ Successfully downloaded: {success_count}/{len(NT_BOOKS)} books")
    if fail_count > 0:
        print(f"✗ Failed downloads: {fail_count}")
    print("=" * 60)

    if success_count > 0:
        print("\nFiles saved to:", os.path.abspath(OUTPUT_DIR))
        print("Ready to integrate with gospel_parser_interlinear.py")

    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
