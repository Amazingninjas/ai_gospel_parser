================================================================================
AI GOSPEL PARSER - INSTALLATION INSTRUCTIONS
================================================================================

Welcome! This tool helps you study the Greek New Testament with AI-powered
analysis.

================================================================================
QUICK START (NON-TECHNICAL USERS)
================================================================================

STEP 1: DOUBLE-CLICK THE INSTALLER FOR YOUR SYSTEM
---------------------------------------------------

Windows:
  → Double-click: INSTALL.bat

macOS:
  → Double-click: INSTALL.command
  (If it says "unidentified developer", right-click and choose "Open")

Linux:
  → Double-click: INSTALL.sh
  (Or run in terminal: ./INSTALL.sh)

STEP 2: FOLLOW THE PROMPTS
---------------------------

The installer will:
  ✓ Check if Python is installed
  ✓ Install Python automatically if needed (with your permission)
  ✓ Install all required software
  ✓ Download the English Bible text
  ✓ Help you choose an AI provider (local or cloud)
  ✓ Create a desktop shortcut

STEP 3: LAUNCH THE PROGRAM
---------------------------

After installation, double-click the desktop shortcut:
  "AI Gospel Parser"

STEP 4: TRY IT OUT
------------------

Type a Bible verse reference:
  > John 3:16

Or ask a question:
  > What does agape mean?

Type 'quit' to exit.

================================================================================
TECHNICAL USERS
================================================================================

If you already have Python 3.8+ installed, you can run the installer directly:

  python install.py

Or manually set up the environment:

  python -m venv venv
  venv/Scripts/activate     (Windows)
  source venv/bin/activate  (macOS/Linux)
  pip install -r requirements.txt
  python download_web_bible.py
  python gospel_parser_interlinear.py

================================================================================
WHAT GETS INSTALLED
================================================================================

Software:
  - Python 3.12 (if not already installed)
  - Required Python libraries (ChromaDB, AI providers, etc.)
  - World English Bible (English reference text)

AI Provider (you choose):
  - Ollama (local AI, runs on your computer)
  - OR Google Gemini (cloud AI, requires API key)

Storage:
  - Greek New Testament database (~100 MB)
  - English Bible text (~2 MB)
  - Installation logs (for debugging)

================================================================================
SYSTEM REQUIREMENTS
================================================================================

Minimum (using Google Gemini API):
  - 4 GB RAM
  - 2 GB free disk space
  - Internet connection
  - Google API key (free tier available)

Recommended (using Ollama local AI):
  - 16 GB RAM
  - 20 GB free disk space
  - 8 GB VRAM (GPU optional but recommended)

The installer will check your system and recommend the best option.

================================================================================
AFTER INSTALLATION
================================================================================

1. READ THE USER GUIDE:
   Open: GETTING_STARTED.txt
   (Comprehensive documentation with all features)

2. LAUNCH THE PROGRAM:
   Double-click the desktop shortcut

3. TRY THESE COMMANDS:
   > John 3:16              (Look up a verse)
   > What does agape mean?  (Ask about Greek words)
   > quit                   (Exit the program)

================================================================================
TROUBLESHOOTING
================================================================================

If installation fails:
  1. Check the log file: install_logs/bootstrap_[date].log
  2. Read GETTING_STARTED.txt (troubleshooting section)
  3. Make sure you have administrator/sudo privileges
  4. Try running the installer again

If the program won't start:
  - For Ollama: Make sure Ollama is running (ollama serve)
  - For Gemini: Check your API key in the .env file

For more help:
  - Full documentation: GETTING_STARTED.txt
  - Technical details: INTERLINEAR_README.md

================================================================================
ABOUT THE TEXTS
================================================================================

Greek Text:
  - Source: MorphGNT SBLGNT v6.12
  - Editor: Michael W. Holmes
  - Organization: Society of Biblical Literature
  - All 27 New Testament books with morphological tagging

English Text:
  - Source: World English Bible (WEB)
  - Public domain, modern English
  - Used for reference only (AI analyzes Greek)

Both texts are freely available for research and education.

Full source attributions in: GETTING_STARTED.txt

================================================================================
PRIVACY & DATA
================================================================================

Ollama (Local AI):
  - Runs entirely on your computer
  - No data sent to the cloud
  - 100% private

Google Gemini (Cloud AI):
  - Sends queries to Google servers
  - Review Google's privacy policy
  - Free tier + paid options

You choose which AI provider to use during installation.

================================================================================
SUPPORT
================================================================================

If you need help:
  1. Check GETTING_STARTED.txt (comprehensive guide)
  2. Look at your install log (install_logs/ folder)
  3. Make sure Python 3.8+ is installed (python --version)

For installation issues, include:
  - Your operating system
  - The bootstrap log file
  - The install_log.txt file
  - Any error messages

================================================================================
ENJOY YOUR STUDY!
================================================================================

This tool is designed to help you engage with the Greek New Testament in a
scholarly and rigorous way. The AI focuses exclusively on the original Greek
text, with English provided only for reference.

May your study be fruitful!

================================================================================
