# AI Gospel Parser

**A comprehensive Biblical Greek text analysis system with AI-powered study capabilities**

[![License](https://img.shields.io/badge/License-Mixed-blue.svg)](#license)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#installation)

---

## 📖 Overview

AI Gospel Parser is a powerful tool for studying the Greek New Testament with integrated AI assistance. It combines original Greek texts, English translations, comprehensive lexicons, and scholarly commentaries into an intelligent study environment.

**Perfect for:**
- Seminary students studying Biblical Greek
- Pastors preparing sermons
- Bible study leaders seeking deeper insights
- Anyone wanting to understand the New Testament in its original language

---

## ✨ Key Features

### 📜 **Complete Greek New Testament**
- **SBLGNT Text** with full morphological tagging (7,957 verses)
- **World English Bible** for parallel English reference
- Verse-by-verse navigation through all 27 NT books

### 🔍 **Comprehensive Lexicons & Commentaries**
- **Thayer's Greek Lexicon** (5,624 Strong's entries)
- **Moulton-Milligan Vocabulary** (5,311 papyri examples)
- **Robertson's Word Pictures** (5,142 verses with grammatical analysis)
- **Vincent's Word Studies** (5,240 verses with word studies)
- **Josephus' Antiquities** for historical context

### 🤖 **Dual AI Provider Support**
- **Ollama (Local):** 100% private, runs on your hardware, no API costs
- **Google Gemini (API):** Cloud-based, no local hardware requirements

### 🎯 **Intelligent Analysis**
- Ask questions about Greek grammar, word meanings, and theological concepts
- AI analyzes original Greek text (not English translations)
- Context-aware responses using lexicons and commentaries
- Conversation memory for follow-up questions

---

## 🚀 Quick Start

### Installation

**Download the latest release:**
1. Go to [Releases](https://github.com/Amazingninjas/ai_gospel_parser/releases)
2. Download the installer for your platform
3. Run the installer - it handles everything automatically

**Or install manually:**
```bash
# Clone the repository
git clone https://github.com/Amazingninjas/ai_gospel_parser.git
cd ai_gospel_parser

# Run the installer
python install.py
```

The installer will:
- Check system requirements
- Install Python dependencies
- Download the English Bible reference
- Set up your AI provider (Ollama or Gemini)
- Create convenient launch scripts

### Running the Program

**Windows:**
```bash
run_interlinear.bat
```

**macOS/Linux:**
```bash
./run_interlinear.sh
```

**Or run directly:**
```bash
python gospel_parser_interlinear.py
```

---

## 💡 Usage Examples

```
> John 3:16
--- John 3:16 ---
Greek:   Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον...
English: For God so loved the world...

> What does agape mean in this verse?
[AI provides detailed analysis of ἀγαπάω including:
 - Grammatical form (aorist active indicative)
 - Lexical definition from Thayer's
 - Cultural context from Moulton-Milligan
 - Theological insights from Robertson & Vincent]

> How does this differ from phileo love?
[AI explains the distinction using lexicon data]

> quit
```

---

## 📋 System Requirements

### Minimum (with Gemini API):
- **Python:** 3.8 or higher
- **RAM:** 4 GB
- **Disk:** 2 GB free space
- **Internet:** Required for Gemini API

### Recommended (with Local Ollama):
- **Python:** 3.8 or higher
- **RAM:** 16 GB (8 GB minimum)
- **Disk:** 20 GB free space (for Mixtral model)
- **GPU:** 8+ GB VRAM (optional, improves speed)
- **Internet:** One-time model download

---

## 🔧 Configuration

### AI Provider Setup

**Option 1: Ollama (Local, Private, Free)**

1. Install Ollama: https://ollama.ai
2. Download model: `ollama pull mixtral`
3. Configure `.env`:
   ```bash
   AI_PROVIDER=ollama
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=mixtral
   ```

**Option 2: Google Gemini (Cloud API)**

1. Get API key: https://makersuite.google.com/app/apikey
2. Configure `.env`:
   ```bash
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_api_key_here
   ```

See [GETTING_STARTED.txt](GETTING_STARTED.txt) for detailed configuration options.

---

## 📚 Documentation

- **[GETTING_STARTED.txt](GETTING_STARTED.txt)** - Comprehensive user guide
- **[QUICK_START.md](QUICK_START.md)** - Fast reference guide
- **[docs/GREEK_TEXT_VERIFICATION.md](docs/GREEK_TEXT_VERIFICATION.md)** - Source text provenance
- **[docs/INTERLINEAR_README.md](docs/INTERLINEAR_README.md)** - Technical documentation

---

## 🗺️ Roadmap

### Current Status: Production Ready (v3.5)
- ✅ Complete Greek New Testament with morphology
- ✅ Dual AI provider support (Ollama + Gemini)
- ✅ 10,382+ verses with commentary
- ✅ Comprehensive installer system

### Future Enhancements
- [ ] Web interface (browser-based UI)
- [ ] Hebrew Old Testament integration
- [ ] Septuagint (Greek OT) support
- [ ] Cross-reference linking
- [ ] Export to PDF/HTML
- [ ] Mobile apps

See [Vision & Roadmap](docs/VISION.md) for long-term plans.

---

## 📄 License

This project uses multiple licenses for different components:

### Software (Python Code)
- **MIT License** - See [LICENSE](LICENSE) for details

### Text Sources
- **SBLGNT:** [SBLGNT EULA](http://sblgnt.com/license/) (text) + CC-BY-SA (morphology)
- **World English Bible:** Public Domain
- **Thayer's Lexicon:** Public Domain
- **Robertson's Word Pictures:** Public Domain
- **Vincent's Word Studies:** Public Domain
- **Josephus' Antiquities:** Public Domain

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

**Areas needing help:**
- Hebrew text integration
- Web UI development
- Additional commentary sources
- Translation improvements

---

## 💬 Support

**Found a bug?** [Open an issue](https://github.com/Amazingninjas/ai_gospel_parser/issues)

**Have questions?** Check [GETTING_STARTED.txt](GETTING_STARTED.txt) or open a discussion

**Want to contribute?** See contributing guidelines above

---

## 🙏 Acknowledgments

**Data Sources:**
- [SBLGNT](http://sblgnt.com/) - Society of Biblical Literature Greek New Testament
- [MorphGNT](https://github.com/morphgnt/sblgnt) - Morphological tagging
- [World English Bible](https://github.com/TehShrike/world-english-bible) - English reference text
- [Christian Classics Ethereal Library](https://www.ccel.org/) - Robertson's Word Pictures
- [StudyLight.org](https://www.studylight.org/) - Vincent's Word Studies

**AI Providers:**
- [Ollama](https://ollama.ai) - Local LLM runtime
- [Google Gemini](https://ai.google.dev/) - Cloud AI service

---

## 📊 Project Statistics

- **Greek NT Verses:** 7,957
- **Lexicon Entries:** 5,624 (Strong's numbers)
- **Commentary Verses:** 10,382+
- **Historical References:** 20 books of Josephus
- **Papyri Examples:** 5,311 (Moulton-Milligan)

---

**Made with ❤️ for Biblical Greek students worldwide**
