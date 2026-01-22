# Greek Text Source Verification

## Summary

✅ **Verified:** The Greek New Testament text used in this project is the **cleanest and most authoritative source available** for computational analysis.

---

## What We're Using

**Source:** MorphGNT SBLGNT v6.12 (2017)
- **Repository:** [github.com/morphgnt/sblgnt](https://github.com/morphgnt/sblgnt)
- **Base Text:** SBLGNT (Society of Biblical Literature Greek New Testament)
- **Editor:** Michael W. Holmes
- **Morphological Tagging:** MorphGNT Project

---

## Verification Details

### 1. Base Text: SBLGNT

**Source:** [Society of Biblical Literature](https://www.sbl-site.org/resources/digital-texts/sbl-greek-new-testament/)

**Provenance:**
- Edited by Michael W. Holmes (respected NT scholar)
- Published by Society of Biblical Literature (authoritative academic body)
- Uses latest manuscript discoveries and critical apparatuses
- Differs from Nestle-Aland/UBS in over 540 variation units
- Free to use under [CC-BY 4.0 License](https://sblgnt.com/)

**Quality Indicators:**
- ✅ Academic rigor (SBL standards)
- ✅ Modern critical edition (incorporates recent scholarship)
- ✅ Freely available for research
- ✅ Used by scholars worldwide

**Relationship to Logos:**
- Source files hosted by [Faithlife/Logos on GitHub](https://github.com/LogosBible/SBLGNT)
- Logos Bible Software distributes SBLGNT with proper licensing
- **BUT:** SBLGNT is *not proprietary to Logos* - it's an SBL resource

### 2. Morphological Tagging: MorphGNT

**Source:** [MorphGNT Project](https://github.com/morphgnt/sblgnt)

**What It Adds:**
- Part of speech classification
- Grammatical parsing codes (tense, voice, mood, case, number, gender, person)
- Lemmatization (dictionary form of each word)
- Normalized word forms
- Text both with and without punctuation

**Data Format:**
```
BBCCVV POS PARSE WORD_W/_PUNCT WORD_NO_PUNCT NORMALIZED LEMMA
040101 N- ----DSF- ἀρχῇ ἀρχῇ ἀρχῇ ἀρχή
```

**Quality Indicators:**
- ✅ Community-maintained (136+ GitHub stars)
- ✅ Stable release (v6.12, 2017)
- ✅ Tab-separated format (clean, parseable)
- ✅ Dual-licensed: SBLGNT text (SBLGNT EULA) + morphology (CC-BY-SA)

---

## Comparison to Other Greek NT Sources

### Alternatives Considered:

| Source | Pros | Cons | Verdict |
|--------|------|------|---------|
| **MorphGNT SBLGNT** | Modern critical text, morphological tags, clean format, free | None significant | ✅ **Using** |
| Nestle-Aland (NA28) | Standard critical text | No free morphological version | ❌ Licensing issues |
| Textus Receptus | Traditional text | Older manuscript basis | ⚠️ Could add as alternative |
| Byzantine Majority | Manuscript weight | Less critical scholarship | ⚠️ Could add as alternative |
| Westcott-Hort | Historical importance | Outdated (1881) | ❌ Superseded |

---

## Current Development Status

### Latest Releases:
- **MorphGNT SBLGNT:** v6.12 (2017) - **Current stable version**
- **No major updates in 2024-2025** (as of January 2026)

### Ongoing Development:
- [Center BLC SBLGNT](https://github.com/CenterBLC/SBLGNT) - Enhanced feature sets (work in progress)
- [Proposal for new tagging schemes](https://github.com/morphgnt/sblgnt/wiki/Proposal-for-a-New-Tagging-Scheme) (under discussion)
- [py-sblgnt](https://github.com/morphgnt/py-sblgnt) - Python API (active)

**Conclusion:** v6.12 remains the authoritative release.

---

## Why This Is the Cleanest Source

### 1. **Data Quality**
- ✅ Modern critical Greek text (SBLGNT)
- ✅ Professional morphological tagging
- ✅ Every word tagged with full grammatical info
- ✅ Lemmatization for dictionary lookups

### 2. **Format Cleanliness**
- ✅ Tab-separated values (trivial to parse)
- ✅ Consistent structure across all 27 NT books
- ✅ No proprietary encoding
- ✅ UTF-8 Greek (standard Unicode)

### 3. **Licensing**
- ✅ Freely usable for research and education
- ✅ CC-BY-SA for morphology (permissive)
- ✅ SBLGNT EULA for text (reasonable restrictions)

### 4. **Authority**
- ✅ SBL (Society of Biblical Literature) - top academic organization
- ✅ Michael W. Holmes - respected NT textual critic
- ✅ MorphGNT - widely used in digital humanities

### 5. **Computational Suitability**
- ✅ Machine-readable format
- ✅ Consistent data structure
- ✅ Rich metadata (morphology + lemmas)
- ✅ No OCR artifacts or digitization errors

---

## Files in This Project

Located in `sblgnt/` directory:

```
61-Mt-morphgnt.txt  - Matthew
62-Mk-morphgnt.txt  - Mark
63-Lk-morphgnt.txt  - Luke
64-Jn-morphgnt.txt  - John
65-Ac-morphgnt.txt  - Acts
66-Ro-morphgnt.txt  - Romans
... (27 NT books total)
```

**Source:** Downloaded from [github.com/morphgnt/sblgnt](https://github.com/morphgnt/sblgnt)

**Version:** 6.12 (2017)

**Verification:** ✅ Confirmed authentic MorphGNT SBLGNT files

---

## Alternative Greek NT Texts (Future Enhancements)

For users who prefer different textual traditions, we could add:

### 1. **Byzantine/Majority Text**
- Source: [Robinson-Pierpont Byzantine Textform](https://github.com/byztxt/byzantine-majority-text)
- Pros: Reflects majority of manuscripts
- Use case: Traditional/confessional preference

### 2. **Textus Receptus**
- Source: Various digitizations available
- Pros: Basis for KJV translation
- Use case: Historical/traditional study

### 3. **Septuagint (LXX) - Old Testament**
- Source: Already included in `LXX-Swete/` directory
- Status: Parsed but not fully integrated yet

---

## Conclusion

**The Greek text in this project (MorphGNT SBLGNT v6.12) is:**

✅ **Authoritative** - From SBL, edited by Michael W. Holmes
✅ **Clean** - Tab-separated, no artifacts, consistent structure
✅ **Complete** - Full morphological tagging + lemmatization
✅ **Current** - Latest stable release (no newer version available)
✅ **Free** - Permissively licensed for research and education
✅ **Accurate** - Modern critical text with latest scholarship

**Verdict:** This is the best available source for AI-powered Greek NT analysis.

---

## Sources

- [SBL Greek New Testament Official Site](https://sblgnt.com/)
- [Society of Biblical Literature - SBLGNT](https://www.sbl-site.org/resources/digital-texts/sbl-greek-new-testament/)
- [MorphGNT SBLGNT Repository](https://github.com/morphgnt/sblgnt)
- [Faithlife/Logos SBLGNT Source Files](https://github.com/LogosBible/SBLGNT)
- [SBLGNT on Logos Bible Software](https://www.logos.com/product/25701/the-greek-new-testament-sbl-edition)
- [Center BLC Enhanced SBLGNT](https://github.com/CenterBLC/SBLGNT)
- [MorphGNT New Tagging Proposals](https://github.com/morphgnt/sblgnt/wiki/Proposal-for-a-New-Tagging-Scheme)

---

**Last Verified:** January 10, 2026
**Current Version:** MorphGNT SBLGNT v6.12 (2017)
**Status:** ✅ Clean, Authoritative, Current
