#!/usr/bin/env python3
"""
AI Gospel Parser - Universal Installer
Guides user through setup with detailed logging for debugging.
"""

import os
import sys
import platform
import subprocess
import datetime
import json
from pathlib import Path

# --- LOGGING SETUP ---

LOG_FILE = "install_log.txt"
log_handle = None

def init_logging():
    """Initialize logging to file"""
    global log_handle
    log_handle = open(LOG_FILE, 'w', encoding='utf-8')
    log(f"AI Gospel Parser Installation")
    log(f"Date: {datetime.datetime.now()}")
    log(f"Platform: {platform.system()} {platform.release()}")
    log(f"Python: {sys.version}")
    log(f"Working Directory: {os.getcwd()}")
    log("=" * 60)

def log(message: str, also_print: bool = True):
    """Log message to file and optionally print"""
    if log_handle:
        log_handle.write(message + "\n")
        log_handle.flush()
    if also_print:
        print(message)

def log_error(message: str, exception: Exception = None):
    """Log error with details"""
    log(f"ERROR: {message}", also_print=True)
    if exception:
        log(f"  Exception: {type(exception).__name__}: {str(exception)}")
        import traceback
        log(f"  Traceback:\n{traceback.format_exc()}")

def finalize_logging():
    """Close log file"""
    if log_handle:
        log("=" * 60)
        log(f"Installation log saved to: {os.path.abspath(LOG_FILE)}")
        log_handle.close()

# --- UTILITY FUNCTIONS ---

def run_command(cmd: list, description: str) -> bool:
    """Run command and log output"""
    log(f"\n[COMMAND] {description}")
    log(f"  Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.stdout:
            log(f"  Output: {result.stdout.strip()}", also_print=False)
        if result.stderr:
            log(f"  Stderr: {result.stderr.strip()}", also_print=False)

        if result.returncode == 0:
            log(f"  [OK] {description}")
            return True
        else:
            log(f"  [FAIL] {description} (exit code {result.returncode})")
            return False

    except subprocess.TimeoutExpired:
        log_error(f"Command timed out after 5 minutes: {description}")
        return False
    except Exception as e:
        log_error(f"Command failed: {description}", e)
        return False

def check_python_version() -> bool:
    """Check Python version"""
    log("\n[CHECK] Python Version")
    version = sys.version_info
    log(f"  Found: Python {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 8:
        log("  [OK] Python version is sufficient")
        return True
    else:
        log("  [FAIL] Python 3.8+ required")
        return False

def check_pip() -> bool:
    """Check if pip is available"""
    log("\n[CHECK] pip Package Manager")
    return run_command([sys.executable, "-m", "pip", "--version"], "Checking pip")

def create_venv() -> bool:
    """Create virtual environment"""
    log("\n[SETUP] Creating Virtual Environment")

    venv_path = "venv"
    if os.path.exists(venv_path):
        log(f"  Virtual environment already exists at: {venv_path}")
        return True

    return run_command([sys.executable, "-m", "venv", venv_path], "Creating venv")

def get_venv_python() -> str:
    """Get path to venv Python executable"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

def install_requirements() -> bool:
    """Install Python dependencies"""
    log("\n[SETUP] Installing Python Dependencies")

    if not os.path.exists("requirements.txt"):
        log("  [FAIL] requirements.txt not found")
        return False

    venv_python = get_venv_python()
    return run_command(
        [venv_python, "-m", "pip", "install", "-r", "requirements.txt"],
        "Installing dependencies"
    )

def download_web_bible() -> bool:
    """Download World English Bible"""
    log("\n[SETUP] Downloading World English Bible")

    if os.path.exists("web_bible_json") and len(os.listdir("web_bible_json")) > 20:
        log("  WEB Bible already downloaded")
        return True

    venv_python = get_venv_python()
    return run_command(
        [venv_python, "download_web_bible.py"],
        "Downloading WEB Bible JSON files"
    )

# --- SYSTEM CHECK ---

def run_system_check() -> dict:
    """Run system requirements check"""
    log("\n[CHECK] System Requirements")

    try:
        # Import and run system checker
        venv_python = get_venv_python()
        result = subprocess.run(
            [venv_python, "system_checker.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.stdout:
            log(result.stdout, also_print=True)

        # Parse recommendation from output
        if "CAN run Mixtral" in result.stdout:
            return {"recommendation": "mixtral", "capable": True}
        else:
            return {"recommendation": "gemini", "capable": False}

    except Exception as e:
        log_error("System check failed", e)
        return {"recommendation": "gemini", "capable": False}

# --- AI PROVIDER SETUP ---

def setup_ollama() -> bool:
    """Guide user through Ollama setup"""
    log("\n[SETUP] Ollama Configuration")

    print("\n" + "=" * 60)
    print("OLLAMA SETUP")
    print("=" * 60)
    print("\nOllama must be installed and running to use Mixtral 7B locally.")
    print("\nSteps:")
    print("1. Download Ollama from: https://ollama.ai")
    print("2. Install Ollama")
    print("3. Open a terminal and run: ollama serve")
    print("4. In another terminal, run: ollama pull mixtral")
    print()

    response = input("Have you completed these steps? (y/n): ").lower()

    if response == 'y':
        # Test Ollama connection
        log("  Testing Ollama connection...")
        try:
            import urllib.request
            urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
            log("  [OK] Ollama is running")
            return True
        except Exception as e:
            log_error("  Cannot connect to Ollama", e)
            print("\n  ERROR: Cannot connect to Ollama at http://localhost:11434")
            print("  Make sure 'ollama serve' is running in another terminal.")
            return False
    else:
        log("  User chose not to set up Ollama")
        return False

def setup_gemini() -> bool:
    """Guide user through Gemini API setup"""
    log("\n[SETUP] Google Gemini API Configuration")

    print("\n" + "=" * 60)
    print("GOOGLE GEMINI API SETUP")
    print("=" * 60)
    print("\nGemini API is a cloud-based alternative (no local hardware requirements).")
    print("\nSteps:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the API key")
    print()

    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()

    if api_key:
        # Save API key to .env file
        log(f"  Saving API key to .env file")
        try:
            with open(".env", "w") as f:
                f.write(f"GOOGLE_API_KEY={api_key}\n")
                f.write(f"AI_PROVIDER=gemini\n")
            log("  [OK] API key saved")
            return True
        except Exception as e:
            log_error("  Failed to save API key", e)
            return False
    else:
        log("  User chose not to set up Gemini")
        return False

def choose_ai_provider(system_check: dict) -> str:
    """Let user choose AI provider"""
    log("\n[SETUP] AI Provider Selection")

    print("\n" + "=" * 60)
    print("CHOOSE AI PROVIDER")
    print("=" * 60)

    if system_check["capable"]:
        print("\n✓ Your system CAN run Mixtral 7B locally")
        print("\nOptions:")
        print("1. Mixtral 7B (Local via Ollama) - Free, private, runs on your hardware")
        print("2. Google Gemini (API) - Requires Google account, cloud-based")
        print()
        choice = input("Choose provider (1 or 2): ").strip()

        if choice == "1":
            if setup_ollama():
                log("  Provider: Ollama (Mixtral 7B)")
                return "ollama"
            else:
                print("\nFalling back to Gemini...")
                if setup_gemini():
                    log("  Provider: Gemini (fallback)")
                    return "gemini"
        elif choice == "2":
            if setup_gemini():
                log("  Provider: Gemini")
                return "gemini"
    else:
        print("\n⚠ Your system may struggle with Mixtral 7B locally")
        print("\nRecommended: Google Gemini (API)")
        print("\nWould you like to set up Gemini?")
        print("(You can always switch to Ollama later if you upgrade your hardware)")
        print()

        response = input("Set up Gemini now? (y/n): ").lower()
        if response == 'y' and setup_gemini():
            log("  Provider: Gemini")
            return "gemini"

    log("  [FAIL] No AI provider configured")
    return None

# --- SHORTCUT CREATION ---

def create_shortcuts(provider: str):
    """Create desktop shortcuts"""
    log("\n[SETUP] Creating Shortcuts")

    try:
        desktop = Path.home() / "Desktop"
        if not desktop.exists():
            log("  Desktop folder not found, skipping shortcuts")
            return

        if platform.system() == "Windows":
            create_windows_shortcut(desktop, provider)
        elif platform.system() == "Darwin":
            create_mac_shortcut(desktop, provider)
        else:
            create_linux_shortcut(desktop, provider)

    except Exception as e:
        log_error("  Failed to create shortcuts", e)

def create_windows_shortcut(desktop: Path, provider: str):
    """Create Windows shortcut"""
    shortcut_path = desktop / "AI Gospel Parser.bat"

    script = f"""@echo off
cd /d "{os.getcwd()}"
call venv\\Scripts\\activate.bat
python gospel_parser_interlinear.py
pause
"""

    with open(shortcut_path, 'w') as f:
        f.write(script)

    log(f"  [OK] Created shortcut: {shortcut_path}")

def create_mac_shortcut(desktop: Path, provider: str):
    """Create macOS shortcut"""
    shortcut_path = desktop / "AI Gospel Parser.command"

    script = f"""#!/bin/bash
cd "{os.getcwd()}"
source venv/bin/activate
python3 gospel_parser_interlinear.py
"""

    with open(shortcut_path, 'w') as f:
        f.write(script)

    os.chmod(shortcut_path, 0o755)
    log(f"  [OK] Created shortcut: {shortcut_path}")

def create_linux_shortcut(desktop: Path, provider: str):
    """Create Linux desktop entry"""
    shortcut_path = desktop / "ai-gospel-parser.desktop"

    desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=AI Gospel Parser
Comment=Greek Bible Study with AI
Exec={os.getcwd()}/venv/bin/python {os.getcwd()}/gospel_parser_interlinear.py
Path={os.getcwd()}
Terminal=true
Icon=utilities-terminal
"""

    with open(shortcut_path, 'w') as f:
        f.write(desktop_entry)

    os.chmod(shortcut_path, 0o755)
    log(f"  [OK] Created shortcut: {shortcut_path}")

# --- MAIN INSTALLATION ---

def main():
    """Main installation flow"""
    init_logging()

    print("\n" + "=" * 60)
    print("AI GOSPEL PARSER - INSTALLATION")
    print("=" * 60)
    print("\nThis installer will:")
    print("1. Check your system requirements")
    print("2. Install Python dependencies")
    print("3. Download the World English Bible")
    print("4. Help you choose an AI provider (Ollama or Gemini)")
    print("5. Create desktop shortcuts")
    print(f"\nAll actions will be logged to: {LOG_FILE}")
    print("If you encounter issues, please share this log file.")
    print()

    input("Press Enter to continue...")

    # Step 1: Check Python
    if not check_python_version():
        log("\n[FAIL] Installation aborted: Python version too old")
        finalize_logging()
        return 1

    # Step 2: Check pip
    if not check_pip():
        log("\n[FAIL] Installation aborted: pip not available")
        finalize_logging()
        return 1

    # Step 3: Create venv
    if not create_venv():
        log("\n[FAIL] Installation aborted: Could not create virtual environment")
        finalize_logging()
        return 1

    # Step 4: Install dependencies
    if not install_requirements():
        log("\n[FAIL] Installation aborted: Could not install dependencies")
        finalize_logging()
        return 1

    # Step 5: Download WEB Bible
    if not download_web_bible():
        log("\n[FAIL] Installation aborted: Could not download WEB Bible")
        finalize_logging()
        return 1

    # Step 6: System check
    system_check = run_system_check()

    # Step 7: Choose and configure AI provider
    provider = choose_ai_provider(system_check)

    if not provider:
        print("\n" + "=" * 60)
        print("INSTALLATION INCOMPLETE")
        print("=" * 60)
        print("\nNo AI provider was configured.")
        print("You can run the installer again later to set up an AI provider.")
        log("\n[INCOMPLETE] No AI provider configured")
        finalize_logging()
        return 1

    # Step 8: Create shortcuts
    create_shortcuts(provider)

    # Step 9: Success!
    print("\n" + "=" * 60)
    print("INSTALLATION COMPLETE!")
    print("=" * 60)
    print(f"\n✓ AI Provider: {provider.upper()}")
    print(f"✓ Desktop shortcut created")
    print(f"✓ Installation log: {os.path.abspath(LOG_FILE)}")
    print("\nNext steps:")
    print("1. Read GETTING_STARTED.txt for usage instructions")
    print("2. Double-click the desktop shortcut to launch")
    print("3. Try a verse lookup: 'John 3:16'")
    print()

    log("\n[SUCCESS] Installation completed successfully")
    finalize_logging()
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("\n[ABORTED] Installation cancelled by user")
        finalize_logging()
        sys.exit(1)
    except Exception as e:
        log_error("Unexpected error during installation", e)
        finalize_logging()
        print(f"\nFATAL ERROR: {e}")
        print(f"Please check {LOG_FILE} for details")
        sys.exit(1)
