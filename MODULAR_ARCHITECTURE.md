# Modular Reference Text Architecture

**Design Goal:** Independent, configurable reference texts that clients can enable/disable

---

## 🏗️ Architecture Overview

### Core Principle: **Plug-and-Play Modules**

Each reference text is:
- ✅ **Independent** - Can be added/removed without affecting others
- ✅ **Configurable** - Enable/disable via environment variables
- ✅ **Isolated** - Has its own parser, data structure, and integration point
- ✅ **Optional** - System works with any combination of texts

---

## 📦 Module Structure

### Each Reference Text Has:

```
reference_texts/
  ├── [text_name]/
  │   ├── [raw_text_file]         # Original source text
  │   ├── metadata.json            # Source attribution
  │   ├── README.md                # Description & usage
  │   └── [parsed_data].json       # Structured data (optional)
  └── parsers/
      └── [text_name]_parser.py    # Independent parser module
```

### Parser Module Interface:

Each parser implements a standard interface:

```python
class ReferenceTextParser:
    def __init__(self, file_path: str):
        """Initialize parser with source file."""

    def parse(self) -> dict:
        """Parse text and return structured data."""

    def is_available(self) -> bool:
        """Check if source files exist."""

    def get_info(self) -> dict:
        """Return metadata about this text."""
```

---

## ⚙️ Configuration System

### Environment Variables (.env):

```bash
# Core lexicon (recommended)
ENABLE_THAYERS="true"

# Additional texts (optional)
ENABLE_MOULTON_MILLIGAN="true"
ENABLE_ROBERTSON_GRAMMAR="true"
ENABLE_JOSEPHUS="true"

# Future commercial texts
ENABLE_BDAG="false"            # Requires license
ENABLE_LOUW_NIDA="false"       # Requires license
```

### Client Presets:

Instead of individual flags, use presets:

```bash
# In .env file:
REFERENCE_PRESET="academic_full"

# Available presets:
# - academic_full: All texts enabled
# - basic: Thayer's only
# - linguistic_focus: Lexicon + Grammar
# - historical_focus: Lexicon + Josephus
# - conservative_christian: Biblical sources only
```

---

## 🔌 Integration Points

### 1. Lexicon Helper (lexicon_helper.py)

```python
class EnhancedLexicon:
    def __init__(self, config: ReferenceTextConfig):
        self.thayers = None
        self.moulton_milligan = None
        self.robertson = None
        self.josephus = None

        # Load only enabled texts
        if config.THAYERS_ENABLED:
            self.thayers = ThayersLexicon()
        if config.MOULTON_MILLIGAN_ENABLED:
            self.moulton_milligan = MoultonMilliganParser()
        # ... etc

    def lookup(self, strongs_id: str) -> dict:
        """Aggregate data from all enabled sources."""
        result = {}

        if self.thayers:
            result['thayers'] = self.thayers.lookup(strongs_id)
        if self.moulton_milligan:
            result['moulton_milligan'] = self.moulton_milligan.lookup(strongs_id)
        # ... etc

        return result
```

### 2. AI Context Builder

```python
def build_ai_context(strongs_numbers: List[str], config: ReferenceTextConfig) -> str:
    """Build context from enabled texts only."""
    context_parts = []

    if config.THAYERS_ENABLED:
        context_parts.append(build_thayers_context(strongs_numbers))

    if config.MOULTON_MILLIGAN_ENABLED:
        context_parts.append(build_moulton_milligan_context(strongs_numbers))

    if config.ROBERTSON_GRAMMAR_ENABLED:
        context_parts.append(build_robertson_context(strongs_numbers))

    if config.JOSEPHUS_ENABLED:
        context_parts.append(build_josephus_context(strongs_numbers))

    return "\n\n".join(filter(None, context_parts))
```

---

## 📚 Current Modules

### Module 1: Thayer's Greek Lexicon ✅ INTEGRATED

**Status:** Fully integrated
**File:** `lexicon_helper.py` (already modular)
**Data:** `enhanced_lexicon.json`
**Config:** `ENABLE_THAYERS`

**Provides:**
- Strong's number definitions
- Etymology
- Cross-references
- NT morphology statistics

**Integration:** Core lexicon, loaded by default

---

### Module 2: Moulton-Milligan Vocabulary 🚧 NEXT

**Status:** Downloaded, needs parser
**File:** `reference_texts/moulton_milligan/moulton_milligan_vocab.txt`
**Parser:** `reference_texts/parsers/moulton_milligan_parser.py` (TO CREATE)
**Data:** `moulton_milligan_data.json` (TO CREATE)
**Config:** `ENABLE_MOULTON_MILLIGAN`

**Will Provide:**
- Papyri usage examples (everyday Greek)
- Idiomatic expressions
- Cultural context
- Non-literary sources

**Integration Point:** Add to lexicon lookup as separate section

---

### Module 3: Robertson's Grammar 🚧 PENDING

**Status:** Downloaded, needs parser
**File:** `reference_texts/robertson_grammar/robertson_grammar.txt`
**Parser:** `reference_texts/parsers/robertson_grammar_parser.py` (TO CREATE)
**Data:** `robertson_grammar_index.json` (TO CREATE)
**Config:** `ENABLE_ROBERTSON_GRAMMAR`

**Will Provide:**
- Syntax rules
- Grammatical explanations
- Example usages
- Cross-references by topic

**Integration Point:** Grammar hints based on morphology codes

---

### Module 4: Josephus Works 🚧 PENDING

**Status:** Downloaded, needs parser
**File:** `reference_texts/josephus/josephus_whiston.txt`
**Parser:** `reference_texts/parsers/josephus_parser.py` (TO CREATE)
**Data:** `josephus_index.json` (TO CREATE)
**Config:** `ENABLE_JOSEPHUS`

**Will Provide:**
- Historical context
- Cultural practices
- 1st-century Jewish customs
- Events and places

**Integration Point:** Historical notes when relevant terms detected

---

## 🔄 Data Flow

### At Startup:

```
1. Load reference_config.py
2. Check which texts are enabled
3. Load only enabled parsers
4. Build combined lexicon
5. Report what's available to user
```

### During Query:

```
1. Extract Greek words / Strong's numbers
2. Query enabled text sources in parallel
3. Aggregate results
4. Format for AI context
5. Inject into AI prompt
```

### Response Attribution:

```
AI should cite sources:
- "According to Thayer's lexicon..."
- "Moulton-Milligan notes from papyri examples..."
- "Robertson's Grammar explains..."
- "Josephus records in Antiquities..."
```

---

## 🎯 Client Use Cases

### Use Case 1: Seminary Student (Academic Full)

**Config:**
```bash
REFERENCE_PRESET="academic_full"
```

**Gets:**
- Thayer's definitions
- Moulton-Milligan idioms
- Robertson's grammar rules
- Josephus historical context

**Use:** Comprehensive research

---

### Use Case 2: Church Bible Study Leader (Basic)

**Config:**
```bash
REFERENCE_PRESET="basic"
```

**Gets:**
- Thayer's definitions only

**Use:** Simple word lookups, not overwhelming

---

### Use Case 3: Linguistics Researcher (Linguistic Focus)

**Config:**
```bash
REFERENCE_PRESET="linguistic_focus"
```

**Gets:**
- Thayer's definitions
- Moulton-Milligan usage examples
- Robertson's grammatical analysis

**Use:** Language study without historical distractions

---

### Use Case 4: Conservative Christian Ministry (Custom)

**Config:**
```bash
ENABLE_THAYERS="true"
ENABLE_MOULTON_MILLIGAN="true"
ENABLE_ROBERTSON_GRAMMAR="true"
ENABLE_JOSEPHUS="false"  # Prefers biblical sources only
```

**Gets:**
- Thayer's + Moulton-Milligan + Robertson
- No Josephus (non-biblical source)

**Use:** Theologically conservative research

---

## 🛠️ Implementation Checklist

### Phase 1: Configuration System ✅ DONE
- [x] Create reference_config.py
- [x] Define enable/disable flags
- [x] Create client presets
- [x] Add validation

### Phase 2: Moulton-Milligan Integration 🚧 IN PROGRESS
- [ ] Create parser module
- [ ] Extract lexical entries
- [ ] Link to Strong's numbers
- [ ] Add to lexicon_helper
- [ ] Update AI context builder

### Phase 3: Robertson's Grammar Integration
- [ ] Create parser module
- [ ] Index by grammatical topics
- [ ] Link to morphology codes
- [ ] Add to lexicon_helper
- [ ] Update AI context builder

### Phase 4: Josephus Integration
- [ ] Create parser module
- [ ] Extract historical references
- [ ] Build topic index
- [ ] Add to lexicon_helper
- [ ] Update AI context builder

### Phase 5: Testing & Documentation
- [ ] Test all combinations
- [ ] Test each preset
- [ ] Update user documentation
- [ ] Create configuration guide

---

## 📊 Performance Considerations

### Load Time:

- **Basic** (Thayer's only): <1 second
- **Academic Full** (all 4): ~3-5 seconds (estimated)
- **Memory**: ~50-100MB total (all texts)

### Optimization Strategies:

1. **Lazy Loading** - Load texts only when first accessed
2. **Caching** - Cache parsed data to JSON for faster startup
3. **Indexing** - Pre-build indices for common queries
4. **Compression** - Compress large text files (gzip)

---

## 🔐 Licensing & Attribution

### Public Domain Texts:
- Thayer's (1889)
- Moulton-Milligan (1914-1929)
- Robertson's Grammar (1914)
- Josephus (Whiston translation, 1737)

**No restrictions** - Free to use, modify, distribute

### Future Commercial Texts:
- BDAG (copyrighted) - Requires license
- Louw-Nida (copyrighted) - Requires license

**Modular design allows:**
- Free version: Public domain texts only
- Premium version: Add commercial texts with proper licensing

---

## 📈 Future Extensibility

### Easy to Add:

- Hebrew lexicon (BDB)
- Septuagint (LXX)
- Vulgate (Latin)
- Church Fathers texts
- Modern commentaries
- Custom research notes

### Just create:
1. New parser module
2. Add config flag
3. Integrate into lexicon_helper
4. Update AI context builder

**No changes to core system required!**

---

## ✅ Benefits of Modular Design

### For Developers:
- Easy to add new texts
- Easy to test individual components
- Easy to maintain and debug
- Clear separation of concerns

### For Clients:
- Choose only what they need
- Reduce memory/load time
- Respect theological preferences
- Control costs (if using licensed texts)

### For Business:
- Free tier (public domain only)
- Premium tiers (add commercial texts)
- Custom configurations per client
- Easy to demonstrate value (enable/disable to show difference)

---

**Status:** Architecture designed, configuration system complete
**Next:** Implement parsers for Moulton-Milligan, Robertson, Josephus
