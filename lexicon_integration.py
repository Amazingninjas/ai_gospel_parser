#!/usr/bin/env python3
"""
Lexicon Integration Module
===========================
Integrates Thayer's Greek Lexicon with SBLGNT morphological data.

Phase 1: Enhanced parsing and ChromaDB integration
- Parse Thayer's XML with ALL fields (etymology, cross-refs, transliteration)
- Aggregate SBLGNT morphology statistics per Strong's number
- Create unified lexicon entries (definitions + morphology)
- Store in dedicated ChromaDB collection

Author: AI Gospel Parser Project
Date: 2026-01-18
"""

import os
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
import re
import unicodedata


# --- MORPHOLOGY CODE PARSING ---

MORPH_POS_MAP = {
    'N-': 'Noun',
    'A-': 'Adjective',
    'V-': 'Verb',
    'P-': 'Preposition',
    'C-': 'Conjunction',
    'D-': 'Adverb',
    'RA': 'Article (definite)',
    'RD': 'Demonstrative pronoun',
    'RI': 'Interrogative pronoun',
    'RP': 'Personal pronoun',
    'RR': 'Relative pronoun',
    'I-': 'Interjection',
    'X-': 'Particle'
}

def parse_morphology_code(pos_code, morph_code):
    """
    Parse SBLGNT morphology code into human-readable components.

    SBLGNT Format from MorphGNT documentation:
    - POS column: 2 characters (V-, N-, A-, RA, etc.)
    - MORPH column: 8 characters (based on actual data analysis):
      Position 0: Person (1,2,3, or -)
      Position 1: Tense (P,I,F,A,X,Y, or -)
      Position 2: Voice (A,M,P, or -)
      Position 3: Mood (I,S,O,M,N,P,D, or -)
      Position 4: Case (N,G,D,A,V, or -)
      Position 5: Number (S,P, or -)
      Position 6: Gender (M,F,N, or -)
      Position 7: Degree (C,S, or -)

    Examples:
    - Verb: 3IAI-S-- = 3rd person, Imperfect, Active, Indicative, Singular
    - Noun: ----NSF- = Nominative, Singular, Feminine

    Returns: dict with parsed components
    """
    result = {
        'pos_code': pos_code,
        'pos': MORPH_POS_MAP.get(pos_code, pos_code)  # Use code itself if not in map
    }

    if not morph_code or len(morph_code) < 7:
        return result

    # Position 0: Person (verbs only)
    if morph_code[0] in '123':
        result['person'] = {'1': '1st', '2': '2nd', '3': '3rd'}[morph_code[0]]

    # Position 1: Tense (verbs only)
    tense_map = {
        'P': 'Present', 'I': 'Imperfect', 'F': 'Future',
        'A': 'Aorist', 'X': 'Perfect', 'Y': 'Pluperfect'
    }
    if morph_code[1] in tense_map:
        result['tense'] = tense_map[morph_code[1]]

    # Position 2: Voice (verbs only)
    voice_map = {'A': 'Active', 'M': 'Middle', 'P': 'Passive'}
    if morph_code[2] in voice_map:
        result['voice'] = voice_map[morph_code[2]]

    # Position 3: Mood (verbs only)
    mood_map = {
        'I': 'Indicative', 'S': 'Subjunctive', 'O': 'Optative',
        'M': 'Imperative', 'N': 'Infinitive', 'P': 'Participle', 'D': 'Imperative'
    }
    if morph_code[3] in mood_map:
        result['mood'] = mood_map[morph_code[3]]

    # Position 4: Case (nouns, adjectives, articles, pronouns, participles)
    case_map = {
        'N': 'Nominative', 'G': 'Genitive', 'D': 'Dative',
        'A': 'Accusative', 'V': 'Vocative'
    }
    if morph_code[4] in case_map:
        result['case'] = case_map[morph_code[4]]

    # Position 5: Number
    number_map = {'S': 'Singular', 'P': 'Plural'}
    if morph_code[5] in number_map:
        result['number'] = number_map[morph_code[5]]

    # Position 6: Gender
    gender_map = {'M': 'Masculine', 'F': 'Feminine', 'N': 'Neuter'}
    if morph_code[6] in gender_map:
        result['gender'] = gender_map[morph_code[6]]

    return result


# --- THAYER'S XML PARSING ---

def parse_thayers_enhanced(xml_path):
    """
    Parse Thayer's Greek Lexicon XML with ALL fields.

    Returns: dict mapping Strong's number -> lexicon entry
    """
    print(f"Parsing Thayer's Lexicon (enhanced): {xml_path}")

    if not os.path.exists(xml_path):
        print(f"  [!] Lexicon file not found: {xml_path}")
        return {}

    tree = ET.parse(xml_path)
    root = tree.getroot()
    lexicon = {}

    for entry in root.findall(".//entry"):
        strongs_num = entry.get("strongs", "").lstrip("0")
        if not strongs_num:
            continue

        # Greek word
        greek_node = entry.find("greek")
        greek_unicode = ""
        greek_translit = ""
        greek_beta = ""
        if greek_node is not None:
            greek_unicode = greek_node.get("unicode", "")
            greek_translit = greek_node.get("translit", "")
            greek_beta = greek_node.get("BETA", "")

        # Pronunciation
        pronunciation_node = entry.find("pronunciation")
        pronunciation = ""
        if pronunciation_node is not None:
            pronunciation = pronunciation_node.get("strongs", "")

        # Etymology/Derivation
        derivation_node = entry.find("strongs_derivation")
        derivation = ""
        if derivation_node is not None:
            derivation_parts = [t.strip() for t in derivation_node.itertext() if t.strip()]
            derivation = " ".join(derivation_parts)

        # Strong's Definition
        strongs_def_node = entry.find("strongs_def")
        strongs_def = ""
        if strongs_def_node is not None:
            strongs_def_parts = [t.strip() for t in strongs_def_node.itertext() if t.strip()]
            strongs_def = " ".join(strongs_def_parts)

        # KJV Definition
        kjv_def_node = entry.find("kjv_def")
        kjv_def = ""
        if kjv_def_node is not None:
            kjv_def_parts = [t.strip() for t in kjv_def_node.itertext() if t.strip()]
            kjv_def = " ".join(kjv_def_parts)

        # Cross-references (see tags)
        cross_refs = []
        for see_tag in entry.findall(".//see"):
            ref_lang = see_tag.get("language", "")
            ref_strongs = see_tag.get("strongs", "").lstrip("0")
            if ref_lang == "GREEK" and ref_strongs:
                cross_refs.append(f"G{ref_strongs}")

        # Also check strongsref tags in definitions
        for ref_tag in entry.findall(".//strongsref"):
            ref_lang = ref_tag.get("language", "")
            ref_strongs = ref_tag.get("strongs", "").lstrip("0")
            if ref_lang == "GREEK" and ref_strongs:
                ref_id = f"G{ref_strongs}"
                if ref_id not in cross_refs:
                    cross_refs.append(ref_id)

        lexicon[f"G{strongs_num}"] = {
            'strongs': f"G{strongs_num}",
            'strongs_num': int(strongs_num),
            'lemma': greek_unicode,
            'transliteration': greek_translit,
            'beta_code': greek_beta,
            'pronunciation': pronunciation,
            'derivation': derivation,
            'definition_strongs': strongs_def,
            'definition_kjv': kjv_def,
            'cross_refs': cross_refs
        }

    print(f"  -> Parsed {len(lexicon)} lexicon entries")
    return lexicon


# --- SBLGNT MORPHOLOGY AGGREGATION ---

def aggregate_sblgnt_morphology(sblgnt_path):
    """
    Analyze all SBLGNT morphology files and aggregate statistics per Strong's lemma.

    SBLGNT format: BBCCVV POS MORPH WORD NORM LEMMA LEMMA_FULL
    Example: 040101 V- 3IAI-S-- ἦν ἦν ἦν εἰμί

    Returns: dict mapping lemma -> morphology statistics
    """
    print(f"Aggregating SBLGNT morphology data: {sblgnt_path}")

    if not os.path.exists(sblgnt_path):
        print(f"  [!] SBLGNT path not found: {sblgnt_path}")
        return {}

    # Data structure: lemma -> stats
    morphology_data = defaultdict(lambda: {
        'lemma': '',
        'total_occurrences': 0,
        'pos_counts': Counter(),
        'morph_codes': Counter(),
        'parsed_features': {
            'tenses': Counter(),
            'voices': Counter(),
            'moods': Counter(),
            'cases': Counter(),
            'numbers': Counter(),
            'genders': Counter(),
            'persons': Counter()
        },
        'sample_forms': []  # First 10 unique word forms
    })

    files_processed = 0
    for filename in sorted(os.listdir(sblgnt_path)):
        if not filename.endswith("-morphgnt.txt"):
            continue

        file_path = os.path.join(sblgnt_path, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) < 7:
                    continue

                # Parse columns
                ref = parts[0]  # BBCCVV
                pos = parts[1]  # Part of speech
                morph = parts[2]  # Morphology code
                word = parts[3]  # Word form (with punctuation)
                norm = parts[4]  # Normalized word
                lemma_norm = parts[5]  # Normalized lemma
                lemma_full = parts[6]  # Full lemma form

                # Use lemma_full as the key (Greek dictionary form)
                data = morphology_data[lemma_full]
                data['lemma'] = lemma_full
                data['total_occurrences'] += 1
                data['pos_counts'][pos] += 1
                data['morph_codes'][morph] += 1

                # Parse morphology code (pass both POS and MORPH)
                parsed = parse_morphology_code(pos, morph)
                if 'tense' in parsed:
                    data['parsed_features']['tenses'][parsed['tense']] += 1
                if 'voice' in parsed:
                    data['parsed_features']['voices'][parsed['voice']] += 1
                if 'mood' in parsed:
                    data['parsed_features']['moods'][parsed['mood']] += 1
                if 'case' in parsed:
                    data['parsed_features']['cases'][parsed['case']] += 1
                if 'number' in parsed:
                    data['parsed_features']['numbers'][parsed['number']] += 1
                if 'gender' in parsed:
                    data['parsed_features']['genders'][parsed['gender']] += 1
                if 'person' in parsed:
                    data['parsed_features']['persons'][parsed['person']] += 1

                # Collect sample forms (first 10 unique)
                clean_word = word.rstrip('.,;:·')  # Remove punctuation
                if len(data['sample_forms']) < 10:
                    if clean_word not in [form['word'] for form in data['sample_forms']]:
                        data['sample_forms'].append({
                            'word': clean_word,
                            'morph': morph,
                            'parsed': parsed
                        })

        files_processed += 1

    print(f"  -> Processed {files_processed} SBLGNT files")
    print(f"  -> Found {len(morphology_data)} unique lemmas")

    # Convert defaultdict to regular dict
    return dict(morphology_data)


# --- STRONG'S NUMBER MAPPING ---

def map_lemmas_to_strongs(sblgnt_path, lexicon):
    """
    Create mapping from Greek lemmas to Strong's numbers.

    Strategy:
    1. Match lemmas from SBLGNT to Thayer's Greek words (exact match)
    2. Handle variant spellings (accents, breathing marks)
    3. Build bidirectional mapping

    Returns: dict mapping lemma -> Strong's number(s)
    """
    print("Mapping SBLGNT lemmas to Strong's numbers...")

    # Create lemma -> Strong's mapping
    lemma_to_strongs = defaultdict(list)

    # First pass: exact matches
    for strongs_id, entry in lexicon.items():
        lemma = entry['lemma']
        if lemma:
            lemma_to_strongs[lemma].append(strongs_id)

    # Create normalized versions (remove accents for fuzzy matching if needed)
    # For now, we'll rely on exact matches since SBLGNT should match Thayer's

    print(f"  -> Mapped {len(lemma_to_strongs)} lemmas to Strong's numbers")

    return dict(lemma_to_strongs)


# --- MERGE DATA ---

def normalize_greek(text):
    """Normalize Greek text to NFC form for consistent matching."""
    return unicodedata.normalize('NFC', text) if text else ''


def merge_lexicon_and_morphology(lexicon, morphology_data, lemma_to_strongs):
    """
    Merge Thayer's lexicon entries with SBLGNT morphology statistics.

    Returns: enhanced lexicon dict
    """
    print("Merging lexicon definitions with morphology data...")

    # Normalize all morphology_data keys
    normalized_morph_data = {}
    for lemma, data in morphology_data.items():
        normalized_lemma = normalize_greek(lemma)
        normalized_morph_data[normalized_lemma] = data

    enhanced_lexicon = {}
    matched_count = 0

    for strongs_id, entry in lexicon.items():
        enhanced_entry = entry.copy()

        # Find morphology data for this lemma (with normalization)
        lemma = normalize_greek(entry['lemma'])
        morph_data = normalized_morph_data.get(lemma, None)

        if morph_data:
            matched_count += 1

            # Infer part of speech from most common POS code
            if morph_data['pos_counts']:
                most_common_pos = morph_data['pos_counts'].most_common(1)[0][0]
                enhanced_entry['part_of_speech'] = MORPH_POS_MAP.get(most_common_pos, 'Unknown')
                enhanced_entry['pos_code'] = most_common_pos

            # Add morphology statistics
            enhanced_entry['morphology'] = {
                'total_occurrences': morph_data['total_occurrences'],
                'tenses': dict(morph_data['parsed_features']['tenses']),
                'voices': dict(morph_data['parsed_features']['voices']),
                'moods': dict(morph_data['parsed_features']['moods']),
                'cases': dict(morph_data['parsed_features']['cases']),
                'numbers': dict(morph_data['parsed_features']['numbers']),
                'genders': dict(morph_data['parsed_features']['genders']),
                'persons': dict(morph_data['parsed_features']['persons']),
                'sample_forms': morph_data['sample_forms'][:5]  # Limit to 5 samples
            }
        else:
            # No morphology data found (word might not appear in NT)
            enhanced_entry['part_of_speech'] = 'Unknown'
            enhanced_entry['morphology'] = None

        enhanced_lexicon[strongs_id] = enhanced_entry

    print(f"  -> Matched {matched_count}/{len(lexicon)} entries with morphology data")
    print(f"  -> {len(lexicon) - matched_count} entries have no NT occurrences")

    return enhanced_lexicon


# --- MAIN INTEGRATION FUNCTION ---

def build_enhanced_lexicon(thayers_xml_path, sblgnt_path):
    """
    Complete integration pipeline.

    Steps:
    1. Parse Thayer's XML (all fields)
    2. Aggregate SBLGNT morphology
    3. Map lemmas to Strong's numbers
    4. Merge data into enhanced lexicon

    Returns: enhanced lexicon dict
    """
    print("=" * 60)
    print("BUILDING ENHANCED LEXICON")
    print("=" * 60)

    # Step 1: Parse Thayer's
    lexicon = parse_thayers_enhanced(thayers_xml_path)

    # Step 2: Aggregate morphology
    morphology_data = aggregate_sblgnt_morphology(sblgnt_path)

    # Step 3: Map lemmas to Strong's
    lemma_to_strongs = map_lemmas_to_strongs(sblgnt_path, lexicon)

    # Step 4: Merge
    enhanced_lexicon = merge_lexicon_and_morphology(lexicon, morphology_data, lemma_to_strongs)

    print("=" * 60)
    print(f"COMPLETE: {len(enhanced_lexicon)} enhanced lexicon entries")
    print("=" * 60)

    return enhanced_lexicon


# --- DISPLAY HELPERS ---

def display_lexicon_entry(entry):
    """Pretty-print a lexicon entry for testing."""
    print(f"\n{'=' * 60}")
    print(f"Strong's: {entry['strongs']}")
    print(f"Lemma: {entry['lemma']} ({entry.get('transliteration', 'N/A')})")
    print(f"Pronunciation: {entry.get('pronunciation', 'N/A')}")
    print(f"Part of Speech: {entry.get('part_of_speech', 'Unknown')}")
    print(f"\nDefinition (Strong's): {entry.get('definition_strongs', 'N/A')}")
    print(f"Definition (KJV): {entry.get('definition_kjv', 'N/A')}")
    print(f"\nDerivation: {entry.get('derivation', 'N/A')}")

    if entry.get('cross_refs'):
        print(f"Cross-references: {', '.join(entry['cross_refs'])}")

    if entry.get('morphology'):
        morph = entry['morphology']
        print(f"\n--- Morphology Statistics ---")
        print(f"Total occurrences in NT: {morph['total_occurrences']}")

        if morph.get('tenses') and morph['tenses']:
            tenses_str = ', '.join(f"{t}: {c}" for t, c in sorted(morph['tenses'].items(), key=lambda x: -x[1]))
            print(f"Tenses: {tenses_str}")
        if morph.get('voices') and morph['voices']:
            voices_str = ', '.join(f"{v}: {c}" for v, c in sorted(morph['voices'].items(), key=lambda x: -x[1]))
            print(f"Voices: {voices_str}")
        if morph.get('moods') and morph['moods']:
            moods_str = ', '.join(f"{m}: {c}" for m, c in sorted(morph['moods'].items(), key=lambda x: -x[1]))
            print(f"Moods: {moods_str}")
        if morph.get('cases') and morph['cases']:
            cases_str = ', '.join(f"{c}: {cnt}" for c, cnt in sorted(morph['cases'].items(), key=lambda x: -x[1]))
            print(f"Cases: {cases_str}")
        if morph.get('numbers') and morph['numbers']:
            numbers_str = ', '.join(f"{n}: {c}" for n, c in sorted(morph['numbers'].items(), key=lambda x: -x[1]))
            print(f"Numbers: {numbers_str}")
        if morph.get('genders') and morph['genders']:
            genders_str = ', '.join(f"{g}: {c}" for g, c in sorted(morph['genders'].items(), key=lambda x: -x[1]))
            print(f"Genders: {genders_str}")
        if morph.get('persons') and morph['persons']:
            persons_str = ', '.join(f"{p}: {c}" for p, c in sorted(morph['persons'].items(), key=lambda x: -x[1]))
            print(f"Persons: {persons_str}")

        if morph.get('sample_forms'):
            print(f"\nSample forms:")
            for form in morph['sample_forms']:
                parsed_str = ', '.join(f"{k}: {v}" for k, v in form['parsed'].items() if k != 'pos_code')
                if parsed_str:
                    print(f"  {form['word']} ({form['morph']}) - {parsed_str}")
                else:
                    print(f"  {form['word']} ({form['morph']})")

    print(f"{'=' * 60}\n")


# --- TESTING ---

if __name__ == "__main__":
    # Configuration
    THAYERS_XML = "strongsgreek.xml"
    SBLGNT_PATH = "sblgnt"

    # Build enhanced lexicon
    enhanced_lexicon = build_enhanced_lexicon(THAYERS_XML, SBLGNT_PATH)

    # Test: Display some interesting entries
    test_strongs = ["G25", "G26", "G3056", "G2316"]  # agapaō, agapē, logos, theos

    print("\n\n" + "=" * 60)
    print("SAMPLE ENTRIES")
    print("=" * 60)

    for strongs_id in test_strongs:
        if strongs_id in enhanced_lexicon:
            display_lexicon_entry(enhanced_lexicon[strongs_id])
