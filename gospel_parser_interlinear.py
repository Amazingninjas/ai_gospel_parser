
import os
import json
import xml.etree.ElementTree as ET
import chromadb
import re
import sys
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required

# Import AI provider system
from ai_providers import get_provider, get_ollama_host

# Import lexicon helper for enhanced definitions
try:
    from lexicon_helper import ThayersLexicon
    LEXICON_AVAILABLE = True
except ImportError:
    LEXICON_AVAILABLE = False
    print("[!] lexicon_helper not available - will skip enhanced definitions")

# --- CONFIGURATION ---
LXX_PATH = "LXX-Swete/src/First1KGreek-LXX-RAW/"
GNT_PATH = "sblgnt/"
LEXICON_PATH = "strongsgreek.xml"
WEB_BIBLE_PATH = "web_bible_json/"
CHROMA_DB_PATH = "chroma_db_interlinear"
COLLECTION_NAME = "gospel_interlinear"

# AI Provider Configuration (from .env or defaults)
AI_PROVIDER_TYPE = os.getenv("AI_PROVIDER", "ollama").lower()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mixtral")
OLLAMA_HOST = get_ollama_host()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# --- BIBLE BOOK MAPPING ---
# Maps book names to SBLGNT numeric codes
BIBLE_BOOKS = {
    # New Testament
    "matthew": {"code": 40, "abbrev": ["mt", "matt", "mat"]},
    "mark": {"code": 41, "abbrev": ["mk", "mar"]},
    "luke": {"code": 42, "abbrev": ["lk", "luk", "lu"]},
    "john": {"code": 43, "abbrev": ["jn", "joh"]},
    "acts": {"code": 44, "abbrev": ["ac", "act"]},
    "romans": {"code": 45, "abbrev": ["ro", "rom", "rm"]},
    "1 corinthians": {"code": 46, "abbrev": ["1co", "1cor", "1 cor"]},
    "2 corinthians": {"code": 47, "abbrev": ["2co", "2cor", "2 cor"]},
    "galatians": {"code": 48, "abbrev": ["ga", "gal"]},
    "ephesians": {"code": 49, "abbrev": ["eph", "ephes"]},
    "philippians": {"code": 50, "abbrev": ["php", "phil", "pp"]},
    "colossians": {"code": 51, "abbrev": ["col"]},
    "1 thessalonians": {"code": 52, "abbrev": ["1th", "1thes", "1thess", "1 thess", "1 th"]},
    "2 thessalonians": {"code": 53, "abbrev": ["2th", "2thes", "2thess", "2 thess", "2 th"]},
    "1 timothy": {"code": 54, "abbrev": ["1ti", "1tim", "1 tim", "1 ti"]},
    "2 timothy": {"code": 55, "abbrev": ["2ti", "2tim", "2 tim", "2 ti"]},
    "titus": {"code": 56, "abbrev": ["tit", "ti"]},
    "philemon": {"code": 57, "abbrev": ["phm", "philem", "pm"]},
    "hebrews": {"code": 58, "abbrev": ["heb", "he"]},
    "james": {"code": 59, "abbrev": ["jas", "jam", "jm"]},
    "1 peter": {"code": 60, "abbrev": ["1pe", "1pet", "1pt", "1 pet", "1 pe"]},
    "2 peter": {"code": 61, "abbrev": ["2pe", "2pet", "2pt", "2 pet", "2 pe"]},
    "1 john": {"code": 62, "abbrev": ["1jn", "1jo", "1j", "1 joh", "1 john"]},
    "2 john": {"code": 63, "abbrev": ["2jn", "2jo", "2j", "2 joh", "2 john"]},
    "3 john": {"code": 64, "abbrev": ["3jn", "3jo", "3j", "3 joh", "3 john"]},
    "jude": {"code": 65, "abbrev": ["jud", "jd"]},
    "revelation": {"code": 66, "abbrev": ["re", "rev", "rv"]},
}

# Reverse lookup: code to book name
CODE_TO_BOOK = {info["code"]: name.title() for name, info in BIBLE_BOOKS.items()}

# --- VERSE REFERENCE PARSER ---

def parse_verse_reference(ref_string):
    """
    Parses verse references like:
    - 'John 3:16' → {'book': 43, 'chapter': 3, 'verse': 16}
    - 'John 3:16-18' → [{'book': 43, 'chapter': 3, 'verse': 16}, ...]
    - '1 John 2:1' → {'book': 62, 'chapter': 2, 'verse': 1}

    Returns: dict or list of dicts with verse info, or None if invalid
    """
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
    for book, info in BIBLE_BOOKS.items():
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
            {"book": book_code, "book_name": CODE_TO_BOOK[book_code],
             "chapter": chapter, "verse": v}
            for v in range(start_verse, end_verse + 1)
        ]
    else:
        return {
            "book": book_code,
            "book_name": CODE_TO_BOOK[book_code],
            "chapter": chapter,
            "verse": start_verse
        }

def format_reference_id(book, chapter, verse):
    """Formats a reference ID like '40-01-01' for Matthew 1:1"""
    return f"{book:02d}-{chapter:02d}-{verse:02d}"

# --- DATABASE SEEDING ---

def parse_lexicon(file_path):
    """Parses the Thayer's Lexicon XML file."""
    print(f"Parsing lexicon: {file_path}")
    if not os.path.exists(file_path):
        print(f"  [!] Lexicon file not found at {file_path}")
        return []

    tree = ET.parse(file_path)
    root = tree.getroot()
    entries = []
    for entry in root.findall(".//entry"):
        strongs_num = entry.get("strongs")
        greek_node = entry.find("greek")
        if greek_node is not None:
            greek_word = greek_node.get("unicode", "")
        else:
            greek_word = ""

        # Extract definitions
        kjv_def_node = entry.find("kjv_def")
        kjv_def = (kjv_def_node.text or "").strip() if kjv_def_node is not None else ""

        strongs_def_node = entry.find("strongs_def")
        strongs_def_parts = [
            (t or "").strip() for t in strongs_def_node.itertext()
        ] if strongs_def_node is not None else []
        strongs_def = " ".join(filter(None, strongs_def_parts))

        full_def = f"G{strongs_num} {greek_word}: KJV: {kjv_def}. Thayer: {strongs_def}"

        entries.append({
            "text": full_def,
            "metadata": {
                "source": "Thayer",
                "strongs": f"G{strongs_num}",
                "book": "Lexicon",
                "type": "lexicon"
            }
        })
    print(f"  -> Parsed {len(entries)} lexicon entries.")
    return entries

def load_web_bible():
    """
    Loads World English Bible (WEB) JSON files and creates a lookup dictionary.
    Returns: dict with (book_code, chapter, verse) -> english_text
    """
    print("Loading World English Bible (WEB)...")

    if not os.path.exists(WEB_BIBLE_PATH):
        print(f"  [!] WEB Bible directory not found at {WEB_BIBLE_PATH}")
        print(f"  [!] Run 'python download_web_bible.py' to download it")
        return {}

    english_lookup = {}

    for filename in sorted(os.listdir(WEB_BIBLE_PATH)):
        if not filename.endswith(".json"):
            continue

        # Extract book code from filename: "43-john.json" → 43
        try:
            book_code = int(filename.split("-")[0])
        except:
            continue

        file_path = os.path.join(WEB_BIBLE_PATH, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Parse verses from JSON
        for item in data:
            if item.get("type") in ["paragraph text", "line text"]:
                chapter = item.get("chapterNumber")
                verse = item.get("verseNumber")
                value = item.get("value", "").strip()

                if chapter and verse and value:
                    key = (book_code, chapter, verse)
                    # Some verses have multiple sections, concatenate them
                    if key in english_lookup:
                        english_lookup[key] += " " + value
                    else:
                        english_lookup[key] = value

    print(f"  -> Loaded {len(english_lookup)} English verses.")
    return english_lookup

def parse_sblgnt_file(file_path, book_code, book_name, english_lookup=None):
    """
    Parses SBLGNT morphology files like '64-Jn-morphgnt.txt'
    Format: BBCCVV POS MORPH WORD NORM LEMMA LEMMA_FULL
    """
    print(f"  Parsing {book_name}...")

    if not os.path.exists(file_path):
        print(f"    [!] File not found: {file_path}")
        return []

    documents = []
    current_verse = None
    verse_words = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 7:
                continue

            # Parse reference: BBCCVV
            ref_id = parts[0]
            try:
                chapter = int(ref_id[2:4])
                verse = int(ref_id[4:6])
            except:
                continue

            # Word is at index 3 (with punctuation)
            word = parts[3]

            verse_ref = (chapter, verse)

            # If we're starting a new verse, save the previous one
            if current_verse != verse_ref and verse_words:
                prev_chapter, prev_verse = current_verse
                greek_text = " ".join(verse_words)

                # Get English text if available
                english_text = ""
                if english_lookup:
                    english_key = (book_code, prev_chapter, prev_verse)
                    english_text = english_lookup.get(english_key, "")

                documents.append({
                    "text": greek_text,
                    "metadata": {
                        "source": "SBLGNT",
                        "book": book_name,
                        "chapter": prev_chapter,
                        "verse": prev_verse,
                        "reference": f"{book_name} {prev_chapter}:{prev_verse}",
                        "reference_id": format_reference_id(book_code, prev_chapter, prev_verse),
                        "english_text": english_text,
                        "type": "verse"
                    }
                })
                verse_words = []

            current_verse = verse_ref
            verse_words.append(word)

    # Don't forget the last verse
    if verse_words and current_verse:
        chapter, verse = current_verse
        greek_text = " ".join(verse_words)

        # Get English text if available
        english_text = ""
        if english_lookup:
            english_key = (book_code, chapter, verse)
            english_text = english_lookup.get(english_key, "")

        documents.append({
            "text": greek_text,
            "metadata": {
                "source": "SBLGNT",
                "book": book_name,
                "chapter": chapter,
                "verse": verse,
                "reference": f"{book_name} {chapter}:{verse}",
                "reference_id": format_reference_id(book_code, chapter, verse),
                "english_text": english_text,
                "type": "verse"
            }
        })

    return documents

def seed_database(client):
    """Parses all source files and seeds the ChromaDB database."""
    print("--- Seeding Database ---")

    # Check if collection exists and has documents
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
        if collection.count() > 0:
            print("Database already seeded. Skipping.")
            return collection
    except Exception:
        print(f"Creating new collection: '{COLLECTION_NAME}'")
        collection = client.create_collection(name=COLLECTION_NAME)

    documents = []

    # 1. Load World English Bible (WEB) for reference
    english_lookup = load_web_bible()

    # 2. Parse Lexicon
    documents.extend(parse_lexicon(LEXICON_PATH))

    # 3. Parse SBLGNT New Testament
    print("Parsing Greek New Testament (SBLGNT)...")
    if os.path.exists(GNT_PATH):
        for filename in sorted(os.listdir(GNT_PATH)):
            if filename.endswith("-morphgnt.txt"):
                # Extract book code from filename: "64-Jn-morphgnt.txt" → 64
                try:
                    book_code = int(filename.split("-")[0])
                    if book_code in CODE_TO_BOOK:
                        book_name = CODE_TO_BOOK[book_code]
                        file_path = os.path.join(GNT_PATH, filename)
                        documents.extend(parse_sblgnt_file(file_path, book_code, book_name, english_lookup))
                except:
                    continue
    else:
        print(f"  [!] SBLGNT directory not found at {GNT_PATH}")

    # Add to ChromaDB in batches
    print(f"\nAdding {len(documents)} total documents to ChromaDB...")
    batch_size = 1000
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]

        collection.add(
            documents=[doc["text"] for doc in batch],
            metadatas=[doc["metadata"] for doc in batch],
            ids=[f"doc_{i+j}" for j in range(len(batch))]
        )
        print(f"  Added batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")

    print("--- Database Seeding Complete ---")
    return collection

# --- QUERY ENGINE ---

def lookup_verse(collection, verse_ref):
    """
    Looks up a specific verse by reference.
    verse_ref: dict with 'book', 'chapter', 'verse' keys
    """
    ref_id = format_reference_id(
        verse_ref['book'],
        verse_ref['chapter'],
        verse_ref['verse']
    )

    results = collection.get(
        where={"reference_id": ref_id}
    )

    if results['documents']:
        return results['documents'][0], results['metadatas'][0]
    return None, None


def extract_greek_words_and_lookup(text, lexicon):
    """
    Extract Greek words from context and look up their Strong's numbers.

    Args:
        text: Context text (may contain Greek words)
        lexicon: ThayersLexicon instance

    Returns: List of Strong's numbers found
    """
    if not lexicon:
        return []

    # Strategy 1: Look for explicit Strong's numbers (G1234)
    strongs_pattern = r'G\d{1,4}'
    strongs_numbers = set(re.findall(strongs_pattern, text))

    # Strategy 2: Extract Greek words (Unicode Greek block)
    # Greek unicode range: \u0370-\u03FF (Greek and Coptic)
    # Extended Greek: \u1F00-\u1FFF (Greek Extended)
    greek_pattern = r'[\u0370-\u03FF\u1F00-\u1FFF]+'
    greek_words = re.findall(greek_pattern, text)

    # Look up each Greek word in lexicon
    for word in greek_words:
        # Clean word (remove punctuation)
        clean_word = word.strip('.,;:·')
        if not clean_word:
            continue

        # Try looking up this word as a lemma
        entries = lexicon.lookup_by_greek(clean_word)
        for entry in entries:
            strongs_numbers.add(entry['strongs'])

    return list(strongs_numbers)


def build_lexicon_context(strongs_numbers, lexicon):
    """
    Build rich lexicon context from Strong's numbers.

    Args:
        strongs_numbers: List of Strong's numbers (e.g., ['G25', 'G26'])
        lexicon: ThayersLexicon instance

    Returns:
        Formatted lexicon context string
    """
    if not strongs_numbers or not lexicon:
        return ""

    lexicon_parts = []
    lexicon_parts.append("\n=== LEXICON DEFINITIONS (Thayer's Enhanced) ===\n")

    for strongs_id in sorted(strongs_numbers)[:10]:  # Limit to 10 most relevant
        entry = lexicon.lookup_by_strongs(strongs_id)
        if not entry:
            continue

        # Build concise but informative entry
        parts = []
        parts.append(f"{strongs_id} {entry['lemma']} ({entry.get('transliteration', '')})")
        parts.append(f"  Part of Speech: {entry.get('part_of_speech', 'Unknown')}")

        # Definition
        definition = entry.get('definition_strongs', '')
        if definition:
            # Truncate if too long
            if len(definition) > 150:
                definition = definition[:147] + "..."
            parts.append(f"  Definition: {definition}")

        # Morphology summary (if available)
        morph = entry.get('morphology')
        if morph:
            parts.append(f"  NT Occurrences: {morph['total_occurrences']}")

            # For verbs: show common tenses
            if morph.get('tenses'):
                top_tenses = sorted(morph['tenses'].items(), key=lambda x: -x[1])[:2]
                tenses_str = ', '.join(f"{t} ({c})" for t, c in top_tenses)
                parts.append(f"  Common tenses: {tenses_str}")

            # For nouns: show common cases
            if morph.get('cases'):
                top_cases = sorted(morph['cases'].items(), key=lambda x: -x[1])[:2]
                cases_str = ', '.join(f"{c} ({cnt})" for c, cnt in top_cases)
                parts.append(f"  Common cases: {cases_str}")

        # Etymology (if interesting)
        if entry.get('derivation') and len(entry['derivation']) < 100:
            parts.append(f"  Etymology: {entry['derivation']}")

        # Cross-references (show 1-2)
        if entry.get('cross_refs'):
            refs = entry['cross_refs'][:2]
            cross_ref_str = ', '.join(refs)
            parts.append(f"  Related: {cross_ref_str}")

        lexicon_parts.append('\n'.join(parts))
        lexicon_parts.append("")  # Blank line between entries

    lexicon_parts.append("=== END LEXICON DEFINITIONS ===\n")

    return '\n'.join(lexicon_parts)

def main():
    """Main function to run the query engine."""

    print("--- AI Gospel Parser (Interlinear Mode) ---")

    # Initialize ChromaDB
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    except Exception as e:
        print(f"Error initializing ChromaDB: {e}")
        sys.exit(1)

    collection = seed_database(chroma_client)

    # Initialize AI Provider
    print(f"\nInitializing AI provider: {AI_PROVIDER_TYPE.upper()}")
    try:
        if AI_PROVIDER_TYPE == "ollama":
            ai_provider = get_provider("ollama", model=OLLAMA_MODEL, host=OLLAMA_HOST)
        elif AI_PROVIDER_TYPE == "gemini":
            ai_provider = get_provider("gemini", model=GEMINI_MODEL)
        else:
            print(f"Error: Unknown AI provider '{AI_PROVIDER_TYPE}'")
            print("Valid options: ollama, gemini")
            sys.exit(1)

        print(f"Connected to: {ai_provider.get_info()}")
    except Exception as e:
        print(f"\nError initializing AI provider: {e}")
        print("\nTroubleshooting:")
        if AI_PROVIDER_TYPE == "ollama":
            print("- Is Ollama running? (ollama serve)")
            print(f"- Is {OLLAMA_MODEL} downloaded? (ollama pull {OLLAMA_MODEL})")
        elif AI_PROVIDER_TYPE == "gemini":
            print("- Is GOOGLE_API_KEY set in .env file?")
            print("- Get API key at: https://makersuite.google.com/app/apikey")
        sys.exit(1)

    # Initialize enhanced lexicon
    lexicon = None
    if LEXICON_AVAILABLE:
        try:
            print("\nLoading enhanced Thayer's lexicon...")
            lexicon = ThayersLexicon()
            print(f"✓ Loaded {len(lexicon)} lexicon entries with morphology")
        except Exception as e:
            print(f"[!] Could not load lexicon: {e}")
            print("    Continuing without enhanced definitions...")
            lexicon = None

    print(f"\nReady to answer questions.")
    print("\nCommands:")
    print("  - Ask questions: 'What does agape mean?'")
    print("  - Look up verses: 'John 3:16' or 'Show me Romans 8:28'")
    print("  - Type 'quit' to exit, 'clear' to clear conversation history")
    print("\nNote: English text (WEB) shown for reference, but AI analyzes GREEK ONLY.")
    if lexicon:
        print("      Enhanced lexicon loaded - AI has access to Thayer's definitions + morphology!\n")
    else:
        print()

    # Initialize conversation history
    conversation_history = []

    # Updated system message - focuses on Greek only
    system_message = """You are an expert research assistant specializing in the Greek Bible.

CRITICAL INSTRUCTION: You must answer questions based EXCLUSIVELY on the GREEK TEXT provided in the context.

The English text is provided ONLY as a reference for verse identification and navigation.
DO NOT quote, analyze, reference, or mention the English text in your responses UNLESS
the user explicitly asks for it (e.g., "compare with English", "show me the English",
"what does the English say").

Your responses should focus on:
- Greek word meanings, etymology, and usage
- Greek grammar, syntax, and word order
- Strong's numbers and lexical definitions
- Original Greek text analysis and interpretation
- Manuscript variants (when relevant)

Always cite Greek text and references. Be scholarly and precise."""

    while True:
        question = input("\n> ")
        if question.lower() == 'quit':
            break

        if question.lower() == 'clear':
            conversation_history = []
            print("Conversation history cleared.")
            continue

        # Check if this is a verse reference lookup
        verse_ref = parse_verse_reference(question)

        if verse_ref:
            # Direct verse lookup
            if isinstance(verse_ref, list):
                # Multiple verses (range)
                print(f"\n--- {verse_ref[0]['book_name']} {verse_ref[0]['chapter']}:{verse_ref[0]['verse']}-{verse_ref[-1]['verse']} ---")
                for ref in verse_ref:
                    text, metadata = lookup_verse(collection, ref)
                    if text:
                        print(f"\n{metadata['reference']}")
                        print(f"Greek:   {text}")
                        if metadata.get('english_text'):
                            print(f"English: {metadata['english_text']}")
            else:
                # Single verse
                text, metadata = lookup_verse(collection, verse_ref)
                if text:
                    print(f"\n--- {metadata['reference']} ---")
                    print(f"Greek:   {text}")
                    if metadata.get('english_text'):
                        print(f"English: {metadata['english_text']}")

                    # Ask if they want AI analysis
                    follow_up = input("\nWould you like AI analysis of this verse? (y/n): ")
                    if follow_up.lower() == 'y':
                        question = f"Analyze this verse: {text}"
                        # Continue to AI query below
                    else:
                        continue
                else:
                    print("Verse not found.")
                    continue

        # Regular AI query with context search
        print("...searching for context...")
        results = collection.query(
            query_texts=[question],
            n_results=15
        )

        context_documents = results['documents'][0]
        context = "\n".join(context_documents)

        # Extract Greek words and look up lexicon data
        lexicon_context = ""
        if lexicon:
            strongs_numbers = extract_greek_words_and_lookup(context + " " + question, lexicon)
            if strongs_numbers:
                print(f"...enriching with lexicon data ({len(strongs_numbers)} entries)...")
                lexicon_context = build_lexicon_context(strongs_numbers, lexicon)

        # Construct messages for Ollama
        messages = [{'role': 'system', 'content': system_message}]

        # Add conversation history (last 10 exchanges)
        recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        messages.extend(recent_history)

        # Add current question with context
        current_message = f"""CONTEXT FROM GREEK BIBLICAL TEXTS:
---
{context}
---
{lexicon_context}

USER QUESTION: {question}

REMEMBER: Focus ONLY on the Greek text. Do not reference English unless explicitly asked.
When citing lexicon definitions, mention "According to Thayer's lexicon..." for attribution."""

        messages.append({'role': 'user', 'content': current_message})

        # Query AI Provider
        print("...thinking...")
        try:
            # Stream response from AI provider
            response_text = ""
            for chunk in ai_provider.chat(messages, stream=True):
                print(chunk, end='', flush=True)
                response_text += chunk
            print()

            # Add to conversation history
            conversation_history.append({'role': 'user', 'content': question})
            conversation_history.append({'role': 'assistant', 'content': response_text})

        except Exception as e:
            print(f"\n[!] Error querying AI: {e}")
            if AI_PROVIDER_TYPE == "ollama":
                print(f"    Is Ollama running? (ollama serve)")
                print(f"    Have you pulled '{OLLAMA_MODEL}'? (ollama pull {OLLAMA_MODEL})")
            elif AI_PROVIDER_TYPE == "gemini":
                print(f"    Check your GOOGLE_API_KEY in .env file")
                print(f"    Get API key at: https://makersuite.google.com/app/apikey")


if __name__ == "__main__":
    main()
