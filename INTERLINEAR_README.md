# AI Gospel Parser - Interlinear Mode

## Overview

This enhanced version of the Gospel Parser provides **verse-by-verse access** to the Greek New Testament with AI-powered analysis. The system focuses exclusively on Greek text analysis, using verse references for navigation.

## Key Features

### 1. **Greek-Focused AI Analysis with English Reference**
- AI responds using ONLY the Greek text from SBLGNT
- English text (World English Bible) displayed side-by-side for reference
- English is stored in metadata but NOT sent to the AI for analysis
- Scholarly focus on Greek grammar, etymology, and word meanings
- Strong's numbers and lexicon integration
- Clean digital WEB format ensures accurate verse alignment

### 2. **Verse Reference System**
Look up any verse using standard Bible references:

```
> John 3:16
> Romans 8:28
> 1 John 4:8
> Matthew 5:1-10  (verse ranges supported)
```

Supported formats:
- Full book names: "John 3:16", "Romans 8:1"
- Numbered books: "1 Corinthians 13:4", "2 Timothy 3:16"
- Abbreviations: "Jn 3:16", "Rom 8:28", "1Co 13:4"
- Verse ranges: "John 1:1-5", "Romans 8:28-30"

### 3. **Interactive Query System**

**Direct Verse Lookup:**
```
> John 3:16

--- John 3:16 ---
Greek:   Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον, ὥστε τὸν υἱὸν τὸν
         μονογενῆ ἔδωκεν, ἵνα πᾶς ὁ πιστεύων εἰς αὐτὸν μὴ ἀπόληται
         ἀλλ' ἔχῃ ζωὴν αἰώνιον.
English: For God so loved the world, that he gave his only born Son,
         that whoever believes in him should not perish, but have
         eternal life.

Would you like AI analysis of this verse? (y/n):
```

**Contextual Questions:**
```
> What does the word agape mean in 1 John 4:8?
> Explain the grammar of John 1:1
> What is the significance of logos in John 1:14?
```

**Lexicon Queries:**
```
> Define Strong's G26
> What does pneuma mean?
> Show me Greek words for love
```

### 4. **Conversation Memory**
- AI remembers previous questions and context
- Follow-up questions reference earlier discussion
- Type `clear` to reset conversation history

## Quick Start

### First-Time Setup

1. **Download World English Bible:**
   ```bash
   cd ai_gospel_parser
   python download_web_bible.py
   ```
   This downloads clean JSON files of the New Testament (~2MB total).

2. **Start Ollama:**
   ```bash
   ollama serve
   ollama pull mixtral
   ```

### Run the Parser

**Windows:** Double-click `run_interlinear.bat`

**Linux/WSL:**
```bash
./run_interlinear.sh
```

**Manual:**
```bash
cd ai_gospel_parser
source venv/bin/activate  # or: venv\Scripts\activate on Windows
python gospel_parser_interlinear.py
```

## Prerequisites

1. **Ollama** must be running with mixtral model
2. **Python 3.12+** with virtual environment
3. **SBLGNT Data** (included in `sblgnt/` directory)
4. **World English Bible** (download with `download_web_bible.py`)

## How It Works

### Database Structure

Each verse is stored as a separate document in ChromaDB:

```python
{
  "text": "Ἐν ἀρχῇ ἦν ὁ λόγος...",  # Greek text (primary - AI sees this)
  "metadata": {
    "book": "John",
    "chapter": 1,
    "verse": 1,
    "reference": "John 1:1",
    "reference_id": "43-01-01",  # Numeric ID for lookup
    "source": "SBLGNT",
    "english_text": "In the beginning was the Word..."  # Hidden from AI
  }
}
```

**Key Architecture:**
- **text field** = Greek only (used for AI analysis and semantic search)
- **metadata.english_text** = English reference (displayed to user, hidden from AI)
- English never enters the AI's context window

### AI System Prompt

The AI is instructed to:
- ✅ Focus exclusively on Greek text
- ✅ Cite Greek words, grammar, and lexical definitions
- ✅ Use Strong's numbers when relevant
- ❌ NOT quote or analyze English text (unless explicitly requested)

## Example Queries

### Verse Lookup
```
> John 1:1
--- John 1:1 ---
Greek: Ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν, καὶ θεὸς ἦν ὁ λόγος.

Would you like AI analysis? (y/n): y

[AI provides Greek grammar and word analysis]
```

### Word Study
```
> What does logos mean in John 1:1?

[AI searches context including John 1:1 and provides Greek etymology,
 usage, and theological significance based on the Greek text]
```

### Grammar Question
```
> Explain the word order in John 3:16

[AI analyzes Greek word order: Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον]
```

### Lexicon Lookup
```
> Define G26

[AI retrieves Strong's G26 (ἀγάπη) from lexicon and explains usage]
```

## Supported Books

**Full New Testament Coverage:**
- Gospels: Matthew, Mark, Luke, John
- History: Acts
- Pauline Epistles: Romans through Philemon
- General Epistles: Hebrews through Jude
- Prophecy: Revelation

## Commands

- `quit` - Exit the program
- `clear` - Clear conversation history
- `[Book Chapter:Verse]` - Look up a specific verse
- Any question - AI searches Greek text context and responds

## Database Location

- **Interlinear DB:** `chroma_db_interlinear/`
- **Original DB:** `chroma_db/` (from original parser)

Both databases are kept separate to preserve your existing data.

## Future Enhancements

Planned features:
- [ ] English text integration (optional reference mode)
- [ ] Morphological analysis per word
- [ ] Cross-reference system
- [ ] Parallel passage comparison
- [ ] Export to interlinear format (HTML/PDF)
- [ ] Multiple Greek text versions (Byzantine, Textus Receptus)

## Philosophy

This tool is designed for **serious Greek Bible study**. The AI is instructed to treat the Greek text as primary and authoritative. English is provided purely as a reference for verse identification and navigation.

### Why World English Bible (WEB)?

We chose WEB for its:
- **Clean digital format** (JSON with proper verse alignment)
- **Public domain** status (no copyright restrictions)
- **Modern readability** (contemporary English)
- **Reference quality** (sufficient for navigation)

Since the AI analyzes only Greek, the English translation quality does not affect scholarly rigor. In fact, differences between the WEB and Greek can serve as teaching moments about translation challenges and theological nuances.

## Troubleshooting

### "Verse not found"
- Check spelling of book name
- Ensure chapter and verse exist (e.g., John 3:36 exists, but John 3:100 does not)
- Try full book name: "1 John" not "1John"

### "Cannot connect to Ollama"
```bash
# Start Ollama in a separate terminal
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### "Database seeding takes too long"
- First run seeds ~8,000 verses from SBLGNT
- Subsequent runs skip seeding (database persists)
- Takes 2-5 minutes on first run

## Technical Details

- **Language:** Python 3.12+
- **Vector DB:** ChromaDB (persistent storage)
- **LLM:** Ollama (mixtral model)
- **Greek Text:** SBLGNT (Society of Biblical Literature Greek New Testament)
- **English Text:** World English Bible (WEB) from GitHub (TehShrike/world-english-bible)
- **Lexicon:** Strong's Greek Lexicon (Thayer's)
- **Download Script:** `download_web_bible.py` (fetches WEB JSON files)

## Comparison to Original Parser

| Feature | Original | Interlinear |
|---------|----------|-------------|
| Verse References | ❌ No | ✅ Yes (John 3:16) |
| Direct Verse Lookup | ❌ No | ✅ Yes |
| Greek Focus | ⚠️ Mixed | ✅ Exclusive |
| Verse-by-Verse Storage | ❌ Sentence-based | ✅ Verse-based |
| Conversation Memory | ✅ Yes | ✅ Yes |
| Strong's Lexicon | ✅ Yes | ✅ Yes |

## License

This tool uses public domain texts:
- SBLGNT: Public domain
- Strong's Greek Lexicon: Public domain
- Parser code: Use as needed for study and research
