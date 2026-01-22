#!/usr/bin/env python3
"""
Build Enhanced Lexicon and Store in ChromaDB
=============================================
Builds the enhanced Thayer's lexicon with SBLGNT morphology and stores it in ChromaDB.

Usage:
    python3 build_enhanced_lexicon.py

Output:
    - ChromaDB collection: lexicon_enhanced
    - JSON backup: enhanced_lexicon.json
"""

import json
import sys
import chromadb
from chromadb.config import Settings
from lexicon_integration import build_enhanced_lexicon


# Configuration
THAYERS_XML = "strongsgreek.xml"
SBLGNT_PATH = "sblgnt"
CHROMA_DB_PATH = "chroma_db_interlinear"
COLLECTION_NAME = "lexicon_enhanced"
JSON_BACKUP = "enhanced_lexicon.json"


def format_lexicon_text(entry):
    """
    Format lexicon entry as searchable text for ChromaDB.

    Creates rich text that includes all definitions, etymology, and morphology summary.
    """
    parts = []

    # Header
    parts.append(f"Strong's {entry['strongs']}: {entry['lemma']} ({entry.get('transliteration', '')})")
    parts.append(f"Part of Speech: {entry.get('part_of_speech', 'Unknown')}")

    # Definitions
    if entry.get('definition_strongs'):
        parts.append(f"\nDefinition: {entry['definition_strongs']}")
    if entry.get('definition_kjv'):
        parts.append(f"KJV: {entry['definition_kjv']}")

    # Etymology
    if entry.get('derivation'):
        parts.append(f"\nEtymology: {entry['derivation']}")

    # Morphology summary
    if entry.get('morphology'):
        morph = entry['morphology']
        parts.append(f"\nOccurrences in NT: {morph['total_occurrences']}")

        if morph.get('tenses'):
            tenses_str = ', '.join(f"{t} ({c})" for t, c in sorted(morph['tenses'].items(), key=lambda x: -x[1])[:3])
            parts.append(f"Common tenses: {tenses_str}")

        if morph.get('cases'):
            cases_str = ', '.join(f"{c} ({cnt})" for c, cnt in sorted(morph['cases'].items(), key=lambda x: -x[1])[:3])
            parts.append(f"Common cases: {cases_str}")

    return "\n".join(parts)


def build_chromadb_collection(enhanced_lexicon):
    """
    Store enhanced lexicon in ChromaDB for semantic search.

    Creates collection with:
    - Text: Formatted lexicon entry (for embedding)
    - Metadata: Strong's number, lemma, POS, occurrence count, etc.
    - ID: Strong's number (G1, G2, etc.)
    """
    print(f"\n{'='*60}")
    print("STORING IN CHROMADB")
    print(f"{'='*60}")

    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    # Delete existing collection if it exists
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except:
        pass

    # Create new collection
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Enhanced Thayer's Greek Lexicon with SBLGNT morphology"}
    )

    print(f"Created collection: {COLLECTION_NAME}")

    # Prepare data for batch insertion
    documents = []
    metadatas = []
    ids = []

    for strongs_id, entry in enhanced_lexicon.items():
        # Format text for embedding
        text = format_lexicon_text(entry)

        # Prepare metadata (ChromaDB requires simple types, no nested dicts)
        metadata = {
            "strongs": entry['strongs'],
            "strongs_num": entry['strongs_num'],
            "lemma": entry['lemma'],
            "transliteration": entry.get('transliteration', ''),
            "part_of_speech": entry.get('part_of_speech', 'Unknown'),
            "pronunciation": entry.get('pronunciation', ''),
            "type": "lexicon"
        }

        # Add morphology stats
        if entry.get('morphology'):
            morph = entry['morphology']
            metadata["occurrences"] = morph['total_occurrences']

            # Top tense
            if morph.get('tenses'):
                top_tense = max(morph['tenses'].items(), key=lambda x: x[1])
                metadata["top_tense"] = top_tense[0]

            # Top case
            if morph.get('cases'):
                top_case = max(morph['cases'].items(), key=lambda x: x[1])
                metadata["top_case"] = top_case[0]

        documents.append(text)
        metadatas.append(metadata)
        ids.append(strongs_id)

    # Batch insert (ChromaDB has batch size limits)
    print(f"Inserting {len(documents)} lexicon entries...")
    BATCH_SIZE = 1000  # Safe batch size
    total_inserted = 0

    for i in range(0, len(documents), BATCH_SIZE):
        batch_docs = documents[i:i+BATCH_SIZE]
        batch_metas = metadatas[i:i+BATCH_SIZE]
        batch_ids = ids[i:i+BATCH_SIZE]

        collection.add(
            documents=batch_docs,
            metadatas=batch_metas,
            ids=batch_ids
        )
        total_inserted += len(batch_docs)
        print(f"  Inserted batch {i//BATCH_SIZE + 1}: {total_inserted}/{len(documents)}")

    print(f"✅ Successfully inserted {total_inserted} entries into ChromaDB")
    print(f"   Collection: {COLLECTION_NAME}")
    print(f"   Path: {CHROMA_DB_PATH}")

    return collection


def save_json_backup(enhanced_lexicon):
    """Save enhanced lexicon as JSON for backup and manual inspection."""
    print(f"\nSaving JSON backup: {JSON_BACKUP}")

    with open(JSON_BACKUP, 'w', encoding='utf-8') as f:
        json.dump(enhanced_lexicon, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(enhanced_lexicon)} entries to {JSON_BACKUP}")


def main():
    """Main execution function."""
    print("="*60)
    print("ENHANCED LEXICON BUILDER")
    print("="*60)

    # Step 1: Build enhanced lexicon
    enhanced_lexicon = build_enhanced_lexicon(THAYERS_XML, SBLGNT_PATH)

    # Step 2: Store in ChromaDB
    collection = build_chromadb_collection(enhanced_lexicon)

    # Step 3: Save JSON backup
    save_json_backup(enhanced_lexicon)

    # Summary
    print(f"\n{'='*60}")
    print("BUILD COMPLETE")
    print(f"{'='*60}")
    print(f"Total entries: {len(enhanced_lexicon)}")
    print(f"Entries with NT occurrences: {sum(1 for e in enhanced_lexicon.values() if e.get('morphology'))}")
    print(f"ChromaDB collection: {COLLECTION_NAME}")
    print(f"JSON backup: {JSON_BACKUP}")
    print()

    # Test query
    print("Testing semantic search...")
    results = collection.query(
        query_texts=["love charity affection"],
        n_results=5
    )

    print("\nTop 5 results for 'love charity affection':")
    for i, (doc_id, metadata) in enumerate(zip(results['ids'][0], results['metadatas'][0])):
        print(f"  {i+1}. {doc_id}: {metadata['lemma']} ({metadata.get('part_of_speech', 'Unknown')})")

    print(f"\n{'='*60}")
    print("✅ Enhanced lexicon ready for use!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
