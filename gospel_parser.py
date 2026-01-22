
import os
import xml.etree.ElementTree as ET
import chromadb
import re
import sys
import argparse
from ai_providers import get_provider, get_ollama_host

# --- CONFIGURATION ---
# Adjust these paths and model names as needed
LXX_PATH = "LXX-Swete/src/First1KGreek-LXX-RAW/"
GNT_PATH = "sblgnt/"
LEXICON_PATH = "strongsgreek.xml"
CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "gospel_ai"
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # A good starting model
OLLAMA_MODEL = "mistral" 
GEMINI_MODEL = "gemini-pro" # Use a valid Gemini model name



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

        # Extract definitions, cleaning them up
        kjv_def_node = entry.find("kjv_def")
        kjv_def = (kjv_def_node.text or "").strip() if kjv_def_node is not None else ""
        
        strongs_def_node = entry.find("strongs_def")
        strongs_def_parts = [
            (t or "").strip() for t in strongs_def_node.itertext()
        ] if strongs_def_node is not None else []
        strongs_def = " ".join(filter(None, strongs_def_parts))

        full_def = f"G{strongs_num} {greek_word}: KJV: {kjv_def}. Thayer: {strongs_def}"
        
        # Each definition is a document
        entries.append({
            "text": full_def,
            "metadata": {
                "source": "Thayer",
                "strongs": f"G{strongs_num}",
                "book": "Lexicon"
            }
        })
    print(f"  -> Parsed {len(entries)} lexicon entries.")
    return entries

def parse_bible_text(file_path, book_name, source):
    """Parses a single plain-text bible book."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple sentence splitting on periods, question marks, etc.
    # A more advanced library like NLTK could be used here for better accuracy.
    sentences = re.split(r'(?<=[.·;])\s+', content)
    
    documents = []
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Basic verse detection - assumes [chapter:verse] format
        ref_match = re.match(r'(\d+:\d+)', sentence)
        verse = ref_match.group(1) if ref_match else f"s{i+1}"
        
        documents.append({
            "text": sentence,
            "metadata": {
                "source": source,
                "book": book_name,
                "reference": f"{book_name} {verse}"
            }
        })
    return documents

def seed_database(client):
    """Parses all source files and seeds the ChromaDB database."""
    print("---"" Seeding Database ---")
    
    # Check if collection exists and has documents
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
        if collection.count() > 0:
            print("Database already seeded. Skipping.")
            return collection
    except Exception:
        print(f"Creating new collection: '{COLLECTION_NAME}'")
        collection = client.create_collection(name=COLLECTION_NAME)

    # 1. Parse Lexicon
    documents = parse_lexicon(LEXICON_PATH)

    # 2. Parse Septuagint (LXX)
    print("Parsing Septuagint (LXX)...")
    if os.path.exists(LXX_PATH):
        for filename in os.listdir(LXX_PATH):
            if filename.endswith(".txt"):
                book_name = os.path.splitext(filename)[0].split('.')[1] # "1.Genesis" -> "Genesis"
                documents.extend(parse_bible_text(os.path.join(LXX_PATH, filename), book_name, "LXX"))
    else:
        print(f"  [!] LXX directory not found at {LXX_PATH}")

    # 3. Parse Greek New Testament (GNT)
    print("Parsing Greek New Testament (GNT)...")
    if os.path.exists(GNT_PATH):
        # SBLGNT
        sblgnt_file = os.path.join(GNT_PATH, "SBLGNT.txt")
        if os.path.exists(sblgnt_file):
            documents.extend(parse_bible_text(sblgnt_file, "SBLGNT", "GNT"))
        # Byzantine
        byz_file = os.path.join(GNT_PATH, "RP-2005.txt")
        if os.path.exists(byz_file):
            documents.extend(parse_bible_text(byz_file, "Byzantine", "GNT"))
    else:
        print(f"  [!] GNT directory not found at {GNT_PATH}")

    # Add to ChromaDB in batches
    print(f"\nAdding {len(documents)} total documents to ChromaDB. This may take a while...")
    batch_size = 1000
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        
        collection.add(
            documents=[doc["text"] for doc in batch],
            metadatas=[doc["metadata"] for doc in batch],
            ids=[f"doc_{i+j}" for j in range(len(batch))]
        )
        print(f"  Added batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")

    print("---"" Database Seeding Complete ---")
    return collection

# --- QUERY ENGINE ---

def main():
    """Main function to run the query engine."""
    parser = argparse.ArgumentParser(description="AI Gospel Parser")
    parser.add_argument(
        '--provider', 
        choices=['ollama', 'gemini'], 
        default='ollama',
        help="The AI provider to use. 'gemini' requires GOOGLE_API_KEY."
    )
    parser.add_argument(
        '-q', '--query',
        type=str,
        default=None,
        help="Run in non-interactive mode with a single query."
    )
    args = parser.parse_args()
    
    print("---"" AI Gospel Parser ---")

    # Initialize ChromaDB
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    except Exception as e:
        print(f"Error initializing ChromaDB: {e}")
        print("Please ensure you have run 'pip install chromadb'")
        sys.exit(1)

    collection = seed_database(chroma_client)

    # Initialize AI provider
    try:
        print(f"Initializing AI provider: {args.provider}")
        provider_args = {}
        if args.provider == 'ollama':
            provider_args = {'model': OLLAMA_MODEL, 'host': get_ollama_host()}
        elif args.provider == 'gemini':
            # The GeminiProvider will automatically look for the GOOGLE_API_KEY env var.
            provider_args = {'model': GEMINI_MODEL}
        
        ai_provider = get_provider(args.provider, **provider_args)

        if not ai_provider.test_connection():
            print(f"[!] Failed to connect to {ai_provider.get_info()}.")
            if args.provider == 'gemini':
                print("    Ensure your GOOGLE_API_KEY is set correctly.")
            elif args.provider == 'ollama':
                print(f"    Is the Ollama server running and the '{OLLAMA_MODEL}' model pulled?")
            sys.exit(1)
            
        print(f"Successfully connected to {ai_provider.get_info()}")

    except (ImportError, ValueError, Exception) as e:
        print(f"[!] Error initializing AI provider: {e}")
        sys.exit(1)


    # System message that persists throughout the conversation
    system_message = """You are an expert research assistant specializing in the Greek Bible.
Your task is to answer the user's questions based on the provided biblical context from ChromaDB.
Use the context to support your answers, but you can also draw on the conversation history.
Cite sources and references when available. Be helpful with follow-up questions."""

    if args.query:
        # Single query mode
        run_single_query_mode(args.query, collection, ai_provider, system_message)
    else:
        # Interactive mode
        run_interactive_mode(collection, ai_provider, system_message)


def perform_query(question, collection, ai_provider, conversation_history, system_message):
    """Encapsulates the logic for a single query to the AI."""
    # 1. Query ChromaDB for relevant context
    # In single-query mode, we don't print status messages
    if not conversation_history: # A bit of a hack to detect single-query mode
        pass
    else:
        print("...searching for context...")

    results = collection.query(
        query_texts=[question],
        n_results=15
    )
    context = "\n".join(results['documents'][0])

    # 2. Construct messages for AI
    messages = [{'role': 'system', 'content': system_message}]
    messages.extend(conversation_history)
    
    current_message = f"""CONTEXT FROM BIBLICAL TEXTS:
---
{context}
---

USER QUESTION: {question}"""
    messages.append({'role': 'user', 'content': current_message})

    # 3. Query AI Provider
    if not conversation_history:
        pass
    else:
        print("...thinking...")
        
    try:
        stream = ai_provider.chat(messages=messages, stream=True)
        response_text = ""
        for chunk in stream:
            # In single query mode, just print the chunks directly.
            # In interactive, we build the full response for history.
            if not conversation_history:
                 print(chunk, end='', flush=True)
            response_text += chunk
        
        if conversation_history is not None:
             print(response_text, end='', flush=True)

        print() # for newline
        return response_text
    except Exception as e:
        print(f"\n[!] Error querying AI provider: {e}")
        return None

def run_single_query_mode(query, collection, ai_provider, system_message):
    """Runs a single query and exits."""
    perform_query(query, collection, ai_provider, [], system_message)

def run_interactive_mode(collection, ai_provider, system_message):
    """Runs the main interactive loop."""
    print(f"\nReady to answer questions. Using '{ai_provider.get_info()}'.")
    print("Conversation memory is enabled - I'll remember our discussion!")
    print("Type 'quit' to exit, 'clear' to clear conversation history.")

    conversation_history = []
    
    while True:
        question = input("\n> ")
        if question.lower() == 'quit':
            break
        if question.lower() == 'clear':
            conversation_history = []
            print("Conversation history cleared.")
            continue
            
        response_text = perform_query(question, collection, ai_provider, conversation_history, system_message)
        
        if response_text:
            conversation_history.append({'role': 'user', 'content': question})
            conversation_history.append({'role': 'assistant', 'content': response_text})


if __name__ == "__main__":
    main()
