## What's New in v3.5.0

### ✨ Major Features

- **10,382+ verses with comprehensive commentary** from Robertson's Word Pictures and Vincent's Word Studies
- **Clean HTML source integration** (28x improvement over OCR sources)
- **Complete New Testament coverage** across all 27 books
- **Dual AI provider support** - Choose between Ollama (local/private) or Google Gemini (cloud API)
- **Comprehensive installer** with automatic system requirements checking
- **Professional documentation** and user guides

### 📚 Commentary Coverage

- **Robertson's Word Pictures:** 5,142 verses with grammatical analysis (17 NT books)
- **Vincent's Word Studies:** 5,240 verses with word studies (all 27 NT books)
- **Thayer's Greek Lexicon:** 5,624 Strong's entries with definitions
- **Moulton-Milligan Vocabulary:** 5,311 papyri examples showing everyday Greek usage
- **Josephus' Antiquities:** Historical context for NT period

### 🚀 Installation

**Quick Start:**

1. Download the source code (ZIP or tar.gz) below
2. Extract the archive
3. Run the installer:
   ```bash
   python install.py
   ```

The installer will:
- Check system requirements
- Install Python dependencies
- Download English Bible reference
- Set up your AI provider (Ollama or Gemini)
- Create convenient launch scripts

### 📋 System Requirements

**Minimum (with Gemini API):**
- Python 3.8+
- 4 GB RAM
- 2 GB disk space
- Internet connection

**Recommended (with Local Ollama):**
- Python 3.8+
- 16 GB RAM (8 GB minimum)
- 20 GB disk space (for Mixtral model)
- GPU with 8+ GB VRAM (optional, improves speed)

### 📖 Documentation

- [Getting Started Guide](https://github.com/Amazingninjas/ai_gospel_parser/blob/main/GETTING_STARTED.txt) - Comprehensive setup and usage
- [Quick Start](https://github.com/Amazingninjas/ai_gospel_parser/blob/main/QUICK_START.md) - Fast reference
- [Greek Text Verification](https://github.com/Amazingninjas/ai_gospel_parser/blob/main/docs/GREEK_TEXT_VERIFICATION.md) - Source provenance
- [Vision & Roadmap](https://github.com/Amazingninjas/ai_gospel_parser/blob/main/docs/VISION.md) - Future plans

### 🎯 Use Cases

Perfect for:
- Seminary students studying Biblical Greek
- Pastors preparing sermons with original language insights
- Bible study leaders seeking deeper understanding
- Scholars researching New Testament texts
- Anyone wanting to study the NT in its original language

### 🐛 Bug Fixes

None - This is the initial production-ready release (beta)

### 🙏 Acknowledgments

**Data Sources:**
- [SBLGNT](http://sblgnt.com/) - Society of Biblical Literature Greek New Testament
- [MorphGNT](https://github.com/morphgnt/sblgnt) - Morphological tagging
- [World English Bible](https://github.com/TehShrike/world-english-bible) - English reference
- [CCEL](https://www.ccel.org/) - Robertson's Word Pictures (HTML)
- [StudyLight.org](https://www.studylight.org/) - Vincent's Word Studies (HTML)

**AI Providers:**
- [Ollama](https://ollama.ai) - Local LLM runtime
- [Google Gemini](https://ai.google.dev/) - Cloud AI API

---

**Status:** Production Ready (Beta)
**License:** MIT (software) + Public Domain (texts)
**Support:** [Open an issue](https://github.com/Amazingninjas/ai_gospel_parser/issues)

### 📊 Project Statistics

- Greek NT Verses: 7,957
- Commentary Verses: 10,382+
- Lexicon Entries: 5,624
- Papyri Examples: 5,311
- Historical References: 20 books of Josephus
