# AI Gospel Parser - Project Context

## Project Overview

A comprehensive Biblical text analysis system with AI-powered Greek language study capabilities. This project demonstrates intelligent document processing, semantic search, multilingual text analysis, and dual AI provider support (local and cloud) for scholarly biblical research.

**Current Status:** Production-ready interlinear Greek-English system with full installer and user documentation.


**WORKFLOW:**

1. **When user requests coding/writing/debugging:**

   **Phase 1 - Exploration & Planning (Claude):**
   - Read files to understand current state (Read, Grep, Glob tools)
   - Explore codebase architecture and patterns
   - Identify what needs to change and why
   - Formulate a clear implementation plan
   - This phase should be QUICK (5-10 file reads max, not extensive analysis)

   **Phase 2 - Execution (Gemini):**
   - **Once you know WHAT to do, IMMEDIATELY delegate to Gemini** - no exceptions
   - Format: `gemini -y "Detailed instruction about what to do, including file paths, requirements, context"`
   - Include all context from exploration phase in the prompt
   - Wait for Gemini to complete the task
   - Report results back to user

   **Critical Delegation Rule:**
   - **The moment you would use Edit, Write, or NotebookEdit → delegate to Gemini instead**
   - Don't write code yourself "just this once" or "because it's quick"
   - Don't make file modifications directly unless Gemini is unavailable
   - **ONLY exception:** User explicitly says "Claude, do this yourself" or similar

2. **When Gemini hits rate limit:**
   - Gemini will return an error message about quota/rate limiting
   - Inform user: "Gemini has hit its rate limit. Taking over with Claude now."
   - Complete the task yourself using normal Claude Code tools

3. **When to use Claude directly (skip Gemini entirely):**
   - **Pure exploration/research tasks** - "How does X work?", "Find files that do Y"
   - **Planning and architecture discussions** - "What's the best approach?"
   - **Answering questions about code** - No modifications needed
   - **Bug diagnosis** - Reading/understanding errors before deciding on fix
   - User explicitly says "Claude, do this yourself" or similar

   **Note:** These are tasks with NO file modifications. If the task ends with "...and then fix it" or "...and implement X", you still need Gemini for the execution phase.

## Overarching Business Goal

**Mission:** Establish a business focused on AI integration services with two core competencies:

1. **Building Quality Augmentation through AI**
   - Enhance existing products, systems, and workflows with AI capabilities
   - Focus on practical, measurable improvements to quality and efficiency
   - Leverage AI for error detection, consistency checking, and intelligent automation

2. **AI Infrastructure Integration (Local LLMs)**
   - Specialize in deploying and integrating local/on-premises LLM solutions
   - Provide privacy-focused AI that runs on client infrastructure
   - Minimize cloud dependencies and recurring API costs
   - Enable offline-capable, secure AI integrations

**Strategic Alignment:**
This project demonstrates advanced document processing, semantic search capabilities, and AI-powered text analysis. It showcases how local LLMs can be used for specialized domain knowledge applications, including multilingual text processing and intelligent content organization.

## Expanded Business Vision (Long-Term Roadmap)

### Phase 1: Greek New Testament Study Tool (COMPLETE)
**Status:** ✅ Production Ready
- Greek New Testament (SBLGNT) with morphological tagging
- World English Bible (WEB) English reference layer
- Strong's Greek Lexicon integration
- Verse-by-verse navigation and AI analysis
- Dual AI provider support (Ollama local + Google Gemini API)
- Comprehensive installer with system requirements checking

### Phase 2: Comprehensive Biblical Library (6-12 months)
**Goal:** Expand to complete Old Testament and foundational Christian texts

**Planned Additions:**
- Septuagint (Greek Old Testament) - LXX integration
- Hebrew Old Testament (Biblia Hebraica Stuttgartensia)
- Hebrew lexicon (Brown-Driver-Briggs)
- Vulgate (Latin) with morphological tagging
- English translations (KJV, ESV, NASB) as references
- Cross-reference system linking related passages
- Advanced morphological analysis and syntax trees

**Features:**
- Multi-language support (Greek, Hebrew, Latin, English)
- Advanced search with grammatical filters
- Parallel passage comparison
- Export to PDF/HTML with interlinear formatting
- Custom study note system

### Phase 3: Theological Library Integration (12-24 months)
**Goal:** Add dozens of essential Christian theological works

**Planned Text Collections:**
- **Early Church Fathers:**
  - Apostolic Fathers (Clement, Ignatius, Polycarp)
  - Ante-Nicene Fathers (Irenaeus, Tertullian, Origen)
  - Nicene & Post-Nicene Fathers (Augustine, Chrysostom, Jerome)
  - Greek and Latin originals with English translations

- **Systematic Theology:**
  - Calvin's Institutes of the Christian Religion
  - Aquinas' Summa Theologica
  - Barth's Church Dogmatics
  - Systematic theologies (Berkhof, Grudem, Horton)

- **Commentaries:**
  - Matthew Henry Complete Commentary
  - Calvin's Commentaries
  - Keil & Delitzsch (Old Testament)
  - Modern critical commentaries

- **Historical Confessions:**
  - Westminster Confession
  - Heidelberg Catechism
  - Augsburg Confession
  - Creeds (Apostles', Nicene, Chalcedonian)

**Features:**
- Semantic search across entire library
- Topic-based navigation
- Author cross-referencing
- Historical timeline context
- Theological concept mapping

### Phase 4: Paid Service Launch (24-36 months)
**Goal:** Monetize as comprehensive Christian study platform

**Subscription Tiers:**

**Free Tier:**
- Greek & English New Testament
- Basic lexicon access
- Limited AI queries (10/day)
- Community features

**Scholar Tier ($9.99/month):**
- Full Greek & Hebrew Old Testament
- Complete lexicon access
- Unlimited AI queries
- 25 theological books
- Export features
- Personal notes & annotations

**Professional Tier ($19.99/month):**
- Everything in Scholar
- 100+ theological books
- Early Church Fathers library
- Advanced AI models (GPT-4, Claude)
- Syntax tree visualization
- Priority support
- Custom study plan generation

**Institution Tier ($99/month or custom):**
- Everything in Professional
- Multi-user access (5-100 seats)
- Administrative dashboard
- API access for research
- On-premises deployment option
- White-label capability
- Dedicated support

**Revenue Model:**
- Subscription-based (recurring monthly/annual)
- One-time purchases for specific book collections
- Custom enterprise deployments
- Academic institution licenses
- API access for third-party developers

**Target Market:**
- Seminary students and professors
- Pastors and ministry leaders
- Serious Bible students
- Christian scholars and researchers
- Churches and ministry organizations
- Christian universities and seminaries

**Competitive Advantages:**
- Local LLM option for privacy-conscious users
- Original language focus (Greek, Hebrew, Latin)
- AI-powered intelligent analysis
- Comprehensive theological library
- Open architecture for customization
- Fair pricing vs. Logos Bible Software ($$$)

## Project-Specific Value Proposition

### Technical Capabilities:
- **Document Processing:** Automated parsing and structuring of complex texts
- **Semantic Search:** Vector embeddings for intelligent text retrieval
- **Multilingual Support:** Greek language processing with lexicon integration
- **Hybrid AI:** Both local (Ollama) and cloud (Gemini) provider support
- **Specialized Knowledge:** Domain-specific AI for Biblical/theological analysis
- **Scalable Architecture:** Designed for high-volume text processing
- **Privacy Options:** Local LLM processing for sensitive research

### Business Capabilities:
- **Market Validation:** Functional MVP ready for beta testing
- **Scalable Infrastructure:** ChromaDB + provider abstraction supports growth
- **User Experience:** Comprehensive installer with guided setup
- **Support System:** Logging and debugging for issue resolution
- **Documentation:** Complete user guide with source attributions
- **Flexible Monetization:** Can start free and add paid tiers incrementally

## Technical Architecture

### Current Implementation:

**Data Sources:**
- Greek New Testament: SBLGNT (MorphGNT v6.12)
  - Source: https://github.com/morphgnt/sblgnt
  - 27 NT books with full morphological tagging
  - 7,957 verses indexed
- English Reference: World English Bible (WEB)
  - Source: https://github.com/TehShrike/world-english-bible
  - Public domain JSON format
  - 7,953 verses aligned with Greek
- Lexicon: Strong's Greek Lexicon
  - Public domain
  - G1-G5624 entries

**AI Providers:**
- **Ollama (Local):**
  - Default model: Mixtral 7B
  - Runs on user hardware
  - Requires: 8+ GB RAM, 10+ GB disk
  - 100% private, no cloud connection

- **Google Gemini (API):**
  - Model: Gemini Pro
  - Cloud-based inference
  - Requires: API key, internet
  - Free tier + paid options

**Vector Database:**
- ChromaDB persistent storage
- Sentence/verse-level embeddings
- Metadata filtering for verse lookup
- Semantic similarity search

**Processing Features:**
- Verse-by-verse storage with references
- English-Greek alignment
- Lexicon integration with Strong's numbers
- Conversation memory (10 recent exchanges)
- Context-aware AI responses

### System Requirements:

**Minimum (Gemini API):**
- Python 3.8+
- 4 GB RAM
- 2 GB disk space
- Internet connection

**Recommended (Ollama Local):**
- Python 3.8+
- 16 GB RAM
- 8 GB VRAM (GPU optional)
- 20 GB disk space

---

## Modular Reference Text Architecture ✅ COMPLETE

**Status:** Fully implemented as of January 18, 2026

### Overview

The parser now features a **modular reference text system** where clients can independently enable/disable scholarly Greek texts based on their needs (theological preferences, computational resources, privacy concerns).

### Design Principles

- ✅ **Independent** - Each text can be added/removed without affecting others
- ✅ **Configurable** - Enable/disable via environment variables or presets
- ✅ **Isolated** - Each has its own parser, data structure, and integration point
- ✅ **Optional** - System works with any combination of enabled texts

### Implemented Components

#### 1. Configuration System (`reference_config.py`)

**Environment Variables (.env):**
```bash
# Core lexicon (recommended)
ENABLE_THAYERS="true"

# Additional texts (optional)
ENABLE_MOULTON_MILLIGAN="true"
ENABLE_ROBERTSON_GRAMMAR="false"  # Quarantined - OCR issues
ENABLE_JOSEPHUS="true"
```

**Client Presets:**
- `academic_full`: All texts enabled (scholars, researchers)
- `basic`: Thayer's only (beginners, simple lookups)
- `linguistic_focus`: Lexicon + Grammar (language study)
- `historical_focus`: Lexicon + Josephus (historical context)
- `conservative_christian`: Biblical sources focus (excludes Josephus)

**Usage:**
```python
from reference_config import ReferenceTextConfig

print(ReferenceTextConfig.get_config_summary())
enabled = ReferenceTextConfig.get_enabled_texts()
```

#### 2. Moulton-Milligan Vocabulary Parser ✅

**File:** `reference_texts/parsers/moulton_milligan_parser.py`

**Results:**
- ✅ Parsed **5,311 Greek vocabulary entries**
- ✅ Linked **2,969 entries (56%)** to Strong's numbers
- ✅ Extracted papyri citations (e.g., "P Oxy III. 471")
- ✅ Extracted NT references and Greek usage examples

**What it provides:**
- Everyday Greek usage from 1st-century papyri (letters, contracts, receipts)
- Idiomatic expressions and colloquialisms
- Demonstrates "Biblical Greek" was actually common Koine Greek
- Cultural context for NT vocabulary

**Data:** `reference_texts/moulton_milligan/moulton_milligan_data.json`

#### 3. Josephus Works Parser ✅

**File:** `reference_texts/parsers/josephus_parser.py`

**Results:**
- ✅ Parsed **20 books** from "The Antiquities of the Jews"
- ✅ Extracted chapters with content previews
- ✅ Created topic index for NT-relevant subjects

**Topic Index:**
- **People:** Pilate (5), Herod (67), Felix (6), Festus (2), Agrippa (29)
- **Groups:** Pharisees (14), Sadducees (7), Essenes (1)
- **Places:** Jerusalem (133), Temple (127), Galilee (34), Judea (98)
- **Events:** Revolt (20), Famine (32), Festival (46)

**What it provides:**
- 1st-century historical and cultural context
- Jewish customs and practices under Roman rule
- Political climate and events surrounding NT period
- Background on people/places mentioned in NT

**Data:** `reference_texts/josephus/josephus_data.json`

#### 4. Robertson's Grammar Parser ⚠️ QUARANTINED

**File:** `reference_texts/parsers/robertson_grammar_parser.py`

**Status:** Parser created but **NOT ENABLED** due to severe OCR corruption in source text

**Issues:**
- OCR converted English → Greek-looking characters ("Beginning" → "Πορίδιηθηὺ")
- Makes keyword search unreliable
- Parser code is sound - just needs clean input text

**Recommendation:**
- Keep quarantined until higher-quality source obtained
- Can be activated later when better scan available
- Set `ENABLE_ROBERTSON_GRAMMAR="false"` in .env

#### 5. Enhanced Lexicon Helper ✅

**File:** `enhanced_lexicon_helper.py`

**Features:**
- Unified interface to all enabled reference texts
- Strong's number lookup across multiple sources
- Historical context search (Josephus)
- Grammar topic search (Robertson - when available)
- AI context builder for comprehensive answers

**Usage:**
```python
from enhanced_lexicon_helper import EnhancedLexiconHelper
from reference_config import ReferenceTextConfig

helper = EnhancedLexiconHelper(config=ReferenceTextConfig)

# Lookup across all enabled texts
results = helper.lookup_strongs("G25")
# Returns: {'thayers': {...}, 'moulton_milligan': {...}}

# Get historical context
context = helper.get_historical_context("Pilate")
# Returns: 5 mentions in Josephus with chapter references

# Build AI context
ai_context = helper.build_ai_context(
    strongs_numbers=["G25", "G2316"],
    keywords=["Pilate", "Jerusalem"]
)
```

### Data Statistics

**Processed:**
- **Thayer's Lexicon:** 5,624 Strong's entries with morphology
- **Moulton-Milligan:** 5,311 Greek words with papyri examples
- **Josephus:** 20 books, 100+ chapters indexed with topic index
- **Total source text:** ~25 MB of scholarly reference material

**Cross-linking:**
- 2,969 Moulton-Milligan entries linked to Strong's numbers (56%)
- Topic index with 15+ categories for Josephus
- All texts normalized to NFC Unicode for consistent Greek matching

### Use Cases

**Seminary Student (academic_full):**
- Thayer's definitions + Moulton-Milligan idioms + Josephus history
- Comprehensive research with all scholarly sources

**Church Bible Study Leader (basic):**
- Thayer's definitions only
- Simple word lookups without overwhelming detail

**Conservative Christian Ministry (custom):**
- Thayer's + Moulton-Milligan, but excludes Josephus (non-biblical)
- Respects theological preference for biblical sources only

**Linguistics Researcher (linguistic_focus):**
- Thayer's + Moulton-Milligan + Robertson's (when available)
- Language study without historical distractions

### File Structure

```
ai_gospel_parser/
├── reference_config.py              # Configuration system
├── enhanced_lexicon_helper.py       # Unified text interface
├── lexicon_helper.py                # Original Thayer's-only helper
├── enhanced_lexicon.json            # Thayer's data (25MB)
├── reference_texts/
│   ├── parsers/
│   │   ├── moulton_milligan_parser.py    # ✅ Working
│   │   ├── robertson_grammar_parser.py   # ⚠️ Quarantined
│   │   └── josephus_parser.py            # ✅ Working
│   ├── moulton_milligan/
│   │   ├── moulton_milligan_vocab.txt    # 5.2MB source
│   │   ├── moulton_milligan_data.json    # Parsed data
│   │   ├── metadata.json
│   │   └── README.md
│   ├── robertson_grammar/
│   │   ├── robertson_grammar.txt         # 6.1MB (corrupted OCR)
│   │   ├── robertson_grammar_topics.json # Basic index
│   │   └── README.md
│   └── josephus/
│       ├── josephus_whiston.txt          # 3.0MB source
│       ├── josephus_data.json            # Parsed data
│       ├── metadata.json
│       └── README.md
├── MODULAR_ARCHITECTURE.md          # Design documentation
└── MODULAR_INTEGRATION_COMPLETE.md  # Implementation summary
```

### Future Enhancements

**High Priority:**
- [ ] Obtain better Robertson's Grammar source (remove from quarantine)
- [ ] Integrate enhanced_lexicon_helper.py with gospel_parser_interlinear.py
- [ ] Add preset switcher in configuration

**Medium Priority:**
- [ ] Hebrew Old Testament lexicon (Brown-Driver-Briggs)
- [ ] Septuagint (LXX) integration
- [ ] BDAG lexicon (if licensing obtained)
- [ ] Louw-Nida semantic domains (if licensing obtained)

---

## Installation & Usage

### Quick Start:

**Option 1 - Installer (Recommended):**
```bash
python install.py
```
The installer will:
- Check system requirements
- Recommend AI provider (Ollama vs Gemini)
- Install dependencies
- Download WEB Bible
- Create desktop shortcuts
- Generate comprehensive logs

**Option 2 - Interlinear Parser (Already Installed):**
```bash
# Windows
run_interlinear.bat

# Linux/macOS
./run_interlinear.sh
```

**First-Time Setup:**
- System requirements check automatic
- Choose AI provider (guided setup)
- Download English Bible (automatic)
- Seed ChromaDB database (first run only)

**Example Usage:**
```
> John 3:16
--- John 3:16 ---
Greek:   Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον...
English: For God so loved the world...

> What does agape mean in this verse?
[AI analyzes Greek text only]

> quit
```

## Files & Documentation

### Core Files:
- `gospel_parser_interlinear.py` - Main program
- `ai_providers.py` - AI provider abstraction layer
- `system_checker.py` - Hardware requirements detection
- `install.py` - Universal installer with logging
- `download_web_bible.py` - WEB Bible downloader

### Documentation:
- `GETTING_STARTED.txt` - Comprehensive user guide
- `INTERLINEAR_README.md` - Technical documentation
- `GREEK_TEXT_VERIFICATION.md` - Source provenance and verification
- `QUICK_START.md` - Fast reference guide
- `install_log.txt` - Installation debugging log (generated)

### Configuration:
- `requirements.txt` - Python dependencies
- `.env` - AI provider configuration (user creates)
- `chroma_db_interlinear/` - Vector database storage
- `web_bible_json/` - English Bible JSON files

## Business Relevance & Demonstration

This project demonstrates the ability to:

### Technical Skills:
- Process and structure large document collections
- Implement semantic search with vector databases
- Handle multilingual/specialized text processing
- Design AI systems for domain-specific knowledge
- Build intelligent document analysis tools
- Create privacy-focused text processing pipelines
- Deploy local AI for sensitive/proprietary content
- Abstract multiple AI providers for flexibility

### Business Skills:
- Market research (biblical study tools market)
- Product roadmap planning (3-year vision)
- Monetization strategy (tiered subscriptions)
- User experience design (comprehensive installer)
- Documentation and support systems
- Competitive analysis (vs Logos, Accordance)
- Scalable architecture for future growth

### Portfolio Value:
- **For AI Services:** Shows real-world AI integration
- **For B2B Clients:** Demonstrates privacy-focused local LLMs
- **For SaaS Investors:** Clear path to monetization
- **For Academic Partners:** Serious scholarly tool

## Competitive Landscape

### Current Market:
- **Logos Bible Software:** $$$$ (hundreds to thousands)
  - Comprehensive but expensive
  - Desktop-only, heavy client
  - Proprietary ecosystem

- **Accordance Bible Software:** $$$ (similar to Logos)
  - Mac-focused
  - Expensive original language modules

- **BibleHub.com:** Free
  - Web-based, no AI
  - Basic interlinear
  - Limited depth

### Our Differentiators:
1. **AI-Powered Analysis:** Unique in the market
2. **Local LLM Option:** Privacy-focused alternative
3. **Fair Pricing:** Accessible to students ($10-20/mo vs $500+)
4. **Open Architecture:** Can integrate with other tools
5. **Modern Stack:** Web-ready, cloud-capable
6. **Original Languages:** Greek/Hebrew primary (not English)

## Development Roadmap Priority

### Immediate (Next 3 months):
- [ ] Beta testing with 50-100 users
- [ ] Bug fixes and UX improvements
- [ ] Web interface (Flask/FastAPI + React)
- [ ] Mobile-responsive design

### Near-term (3-6 months):
- [ ] Hebrew Old Testament integration
- [ ] Septuagint (Greek OT) completion
- [ ] Cross-reference system
- [ ] User accounts and cloud sync
- [ ] First paid tier launch (beta)

### Mid-term (6-12 months):
- [ ] Add 25 theological books
- [ ] Advanced search features
- [ ] Subscription billing system
- [ ] API access for developers
- [ ] Mobile apps (iOS/Android)

### Long-term (12-24 months):
- [ ] 100+ book library
- [ ] Custom AI training on theological texts
- [ ] Institutional licensing
- [ ] White-label solutions
- [ ] International expansion

## Contact & Support

**For Installation Issues:**
- Check `install_log.txt` for debugging
- Review `GETTING_STARTED.txt` for troubleshooting
- Report issues with full logs

**For Business Inquiries:**
- Interested beta testers
- Potential investors
- Academic partnerships
- Enterprise licensing

## License & Attribution

**Open Development Phase:**
- Currently free for research and education
- Will transition to paid service (see roadmap)
- Open source components remain credited

**Text Sources:**
- SBLGNT: CC-BY-SA (morphology), SBLGNT EULA (text)
- WEB Bible: Public Domain
- Strong's Lexicon: Public Domain

**Software Stack:**
- Python: PSF License
- ChromaDB: Apache 2.0
- Ollama: MIT License
- Google Gemini: Commercial API

---

**Last Updated:** January 18, 2026
**Version:** 3.0 (Modular Reference Text Architecture)
**Status:** Production Ready (Beta)

**Recent Updates:**
- ✅ **v3.0 (Jan 18, 2026):** Modular reference text system with Moulton-Milligan, Josephus, configurable presets
- ✅ **v2.0 (Jan 10, 2026):** Dual AI provider support (Ollama + Gemini)
- ✅ **v1.0:** Initial interlinear Greek-English parser with Thayer's lexicon
