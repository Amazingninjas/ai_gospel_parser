# Moulton-Milligan Vocabulary

## Overview

**Full Title:** The Vocabulary of the Greek Testament Illustrated from the Papyri and Other Non-Literary Sources

**Authors:**
- James Hope Moulton, D.D., D.Theol. (Late Fellow of King's College, Cambridge; Greenwood Professor of Hellenistic Greek and Indo-European Philology, Manchester University)
- George Milligan, D.D. (Regius Professor of Divinity and Biblical Criticism, Glasgow University)

**Publication:** 1914-1929
**License:** Public Domain

---

## What This Text Provides

Moulton-Milligan revolutionized New Testament Greek studies by demonstrating that Biblical Greek was not a special "Holy Spirit language" but rather the common (Koine) Greek spoken by everyday people in the 1st century AD.

### Key Features:

1. **Papyri Citations**
   - Contemporary documents (letters, contracts, receipts, official records)
   - Show how NT words were used in everyday life
   - Provide cultural and linguistic context

2. **Idiomatic Usage**
   - Real-world examples of Greek phrases
   - Colloquial expressions from non-literary sources
   - Demonstrates vernacular usage vs. literary style

3. **Non-Literary Sources**
   - Oxyrhynchus papyri
   - Egyptian inscriptions
   - Business documents
   - Personal correspondence

4. **Scholarly Rigor**
   - Detailed citations with dates (e.g., "P Oxy III. 471 (ii/A.D.)")
   - Cross-references to other lexicons
   - Discussion of variant readings

---

## Example Entry

**ἀγάπη** (agape - love):
> "Though it would be going too far to say that this important Biblical word was 'born within the bosom of revealed religion,' it is remarkable that there have been only three supposed instances of its use in 'profane' Greek, two of which are now read otherwise and the third is doubtful."

This shows that ἀγάπη was *extremely rare* in non-Christian Greek, making it essentially a Christian theological term.

---

## Parsed Data Structure

The parser (`parsers/moulton_milligan_parser.py`) extracts:

```json
{
  "ἀγάπη": {
    "lemma": "ἀγάπη",
    "strongs_numbers": ["G26"],
    "full_text": "...scholarly discussion...",
    "papyri_citations": [],
    "nt_references": [],
    "examples": ["...Greek usage examples..."],
    "source": "Moulton-Milligan Vocabulary (1914-1929)"
  }
}
```

### Fields:
- **lemma**: Greek word (NFC normalized)
- **strongs_numbers**: Linked Strong's number(s) via Thayer's crossref
- **full_text**: Up to 2000 chars of scholarly commentary
- **papyri_citations**: Papyri references (e.g., "P Oxy III. 471")
- **nt_references**: New Testament verse references
- **examples**: Greek usage examples from papyri
- **source**: Attribution

---

## Statistics

**Total Entries:** 5,311 Greek words
**Linked to Strong's:** 2,969 (56%)
**Entries with Papyri Citations:** ~4,700
**Entries with NT References:** ~3,800

**Coverage:** Comprehensive coverage of NT vocabulary with focus on words that appear in contemporary non-literary sources.

---

## Integration Use Cases

### Use Case 1: Cultural Context
```python
entry = mm_parser.lookup_by_lemma("ἀγοράζω")
# Shows how "buy/redeem" was used in ancient marketplace documents
```

### Use Case 2: Idiomatic Expressions
```python
entry = mm_parser.lookup_by_lemma("καιρός")
# Papyri examples show difference from χρόνος (time)
```

### Use Case 3: Vernacular vs. Literary
```python
entry = mm_parser.lookup_by_lemma("οἰκοδομέω")
# Shows everyday building/construction usage vs. metaphorical NT usage
```

---

## Why This Text Matters

### Before Moulton-Milligan:
- NT Greek was thought to be "Holy Spirit language"
- Scholars couldn't explain many "peculiar" NT usages
- Theological interpretations were based on limited linguistic data

### After Moulton-Milligan:
- NT Greek recognized as common Koine (everyday Greek)
- Many "unique" words found in papyri (ordinary usage)
- Better understanding of cultural/historical context
- More accurate translations and interpretations

---

## Complementary Texts

**Use with:**
- **Thayer's Lexicon** - Comprehensive definitions and Strong's numbers
- **Robertson's Grammar** - Syntax and grammatical analysis
- **Josephus Works** - Historical and cultural background

**Moulton-Milligan answers:**
- "How was this word used in everyday life?"
- "Is this a literary or colloquial usage?"
- "What cultural context explains this phrase?"

---

## Source File

**File:** `moulton_milligan_vocab.txt` (5.2 MB)
**Format:** DJVU text extraction from Archive.org
**Quality:** Good (minor OCR artifacts, manually corrected in parser)
**Source URL:** https://archive.org/details/vocabularyofgree00mouluoft

---

## Parser Implementation

**File:** `parsers/moulton_milligan_parser.py`

**Features:**
- Modular interface (standard parser API)
- Unicode normalization (NFC) for Greek text
- Strong's number linking via Thayer's crossref
- Papyri citation extraction with regex
- NT reference detection
- Greek example extraction
- JSON export

**Usage:**
```python
from parsers.moulton_milligan_parser import MoultonMilliganParser

parser = MoultonMilliganParser("moulton_milligan/moulton_milligan_vocab.txt")
entries = parser.parse()
parser.link_to_strongs("enhanced_lexicon.json")
parser.export_to_json("moulton_milligan_data.json")
```

---

## Academic Value

**Scholarly Rigor:** ★★★★★
**Cultural Context:** ★★★★★
**NT Coverage:** ★★★★☆
**Accessibility:** ★★★☆☆ (requires knowledge of Greek)

**Citations:**
- Moulton, J. H., & Milligan, G. (1914-1929). *The Vocabulary of the Greek Testament Illustrated from the Papyri and Other Non-Literary Sources*. London: Hodder and Stoughton.

---

**Last Updated:** 2026-01-18
**Parser Version:** 1.0
**Status:** ✅ Fully Integrated
