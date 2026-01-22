# AI Gospel Parser - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Download English Reference Text (One-Time)

```bash
cd ai_gospel_parser
python download_web_bible.py
```

**What this does:**
- Downloads 27 NT books from World English Bible (WEB)
- Clean JSON format, ~2MB total
- Public domain, no copyright restrictions
- Takes about 2 minutes

### Step 2: Start Ollama

```bash
# In a separate terminal
ollama serve

# Make sure mixtral model is pulled
ollama pull mixtral
```

### Step 3: Run the Parser

**Option A - Windows (Double-click):**
```
run_interlinear.bat
```

**Option B - Linux/WSL:**
```bash
./run_interlinear.sh
```

**Option C - Manual:**
```bash
source venv/bin/activate
python gospel_parser_interlinear.py
```

---

## 📖 How to Use

### Look Up Verses

```
> John 3:16
> Romans 8:28
> 1 John 4:8
> Matthew 5:1-10  (verse ranges work too)
```

**Output:**
```
--- John 3:16 ---
Greek:   Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον...
English: For God so loved the world, that he gave...

Would you like AI analysis? (y/n):
```

### Ask Questions

```
> What does agape mean in 1 John 4:8?
> Explain the grammar of John 1:1
> Define Strong's G26
> What's the difference between agape and phileo?
```

**AI responds using ONLY Greek text.**

### Commands

- `quit` - Exit the program
- `clear` - Clear conversation history
- Any Bible reference - Look up that verse
- Any question - AI analyzes Greek context

---

## 🔑 Key Feature

**English is displayed for YOUR reference, but the AI sees and analyzes ONLY the Greek text.**

This ensures:
- ✅ Scholarly rigor (Greek-first analysis)
- ✅ You can verify you found the right verse
- ✅ Educational: compare translations
- ✅ Navigation: use familiar English references

---

## 🧪 Test the Integration

```bash
python test_english_integration.py
```

This verifies:
- ✓ WEB Bible loaded correctly (7,953 verses)
- ✓ All 27 NT books present
- ✓ Verses align properly with Greek

---

## 📁 Files Created

```
ai_gospel_parser/
├── web_bible_json/              # English NT (downloaded)
│   ├── 40-matthew.json
│   ├── 41-mark.json
│   └── ...
├── chroma_db_interlinear/       # Vector database (auto-created)
├── gospel_parser_interlinear.py # Main program
├── download_web_bible.py        # WEB downloader
├── test_english_integration.py  # Integration test
└── run_interlinear.bat/sh       # Launchers
```

---

## ❓ Common Questions

**Q: Does the AI use the English text for analysis?**
A: No. English is in metadata only. The AI receives ONLY Greek text.

**Q: Why World English Bible?**
A: Cleanest digital format (JSON), public domain, good enough for reference.

**Q: What if I don't want English displayed?**
A: Currently it displays alongside Greek. A future enhancement could add a display mode toggle.

**Q: Can I use a different English translation?**
A: Yes, but you'd need to modify the parser to use a different source.

**Q: How long does seeding take?**
A: First run: 2-5 minutes (8,000+ verses). Subsequent runs skip seeding.

---

## 🎯 Example Session

```
> John 1:1

--- John 1:1 ---
Greek:   Ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν...
English: In the beginning was the Word, and the Word was with God...

Would you like AI analysis? (y/n): y

...thinking...

The verse begins with Ἐν ἀρχῇ (en archē), meaning "in the beginning."
The subject ὁ λόγος (ho logos) is emphatic through word order placement.
The verb ἦν (ēn) is the imperfect of εἰμί (eimi), indicating continuous
existence. The phrase καὶ ὁ λόγος ἦν πρὸς τὸν θεόν uses πρὸς (pros) with
the accusative to express intimate relationship...

> What does logos mean?

...thinking...

λόγος (logos, G3056) is a rich Greek term meaning "word," "reason,"
"speech," or "divine expression." In Johannine theology...
```

---

## 🐛 Troubleshooting

**"web_bible_json/ not found"**
```bash
python download_web_bible.py
```

**"Cannot connect to Ollama"**
```bash
ollama serve  # In a separate terminal
```

**"Verse not found"**
- Check spelling: "1 John" not "1John"
- Ensure verse exists: "John 1:100" doesn't exist

---

## 📚 More Information

- **Full Documentation:** `INTERLINEAR_README.md`
- **English Architecture:** See "How It Works" section
- **Business Context:** `CLAUDE.md` (project goals)

---

**Ready? Start with Step 1 above!**
