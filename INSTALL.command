#!/bin/bash
################################################################################
# AI Gospel Parser - macOS Bootstrap Installer
# This script checks for Python and installs it automatically if needed
################################################################################

echo "============================================================================"
echo "AI GOSPEL PARSER - macOS INSTALLER"
echo "============================================================================"
echo ""
echo "This installer will:"
echo "  1. Check if Python is installed"
echo "  2. Install Python 3.12 if needed (via Homebrew or official installer)"
echo "  3. Run the main installation script"
echo ""
read -p "Press Enter to continue, or Ctrl+C to cancel..."

# Change to script directory
cd "$(dirname "$0")"

# Create logs directory
mkdir -p install_logs
LOG_FILE="install_logs/bootstrap_$(date +%Y%m%d_%H%M%S).log"

echo "" | tee -a "$LOG_FILE"
echo "[1/4] Checking for Python installation..." | tee -a "$LOG_FILE"

# Check if Python 3 is installed
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "[OK] Python is already installed!" | tee -a "$LOG_FILE"
    echo "$PYTHON_VERSION" | tee -a "$LOG_FILE"

    # Check if version is 3.8+
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    if [ "$PYTHON_MINOR" -ge 8 ]; then
        echo "[OK] Python version is sufficient (3.8+)" | tee -a "$LOG_FILE"
        PYTHON_CMD="python3"
    else
        echo "[!] Python version is too old. Need 3.8+" | tee -a "$LOG_FILE"
        PYTHON_CMD=""
    fi
else
    echo "[!] Python 3 is not installed." | tee -a "$LOG_FILE"
    PYTHON_CMD=""
fi

# If Python is not suitable, install it
if [ -z "$PYTHON_CMD" ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "============================================================================"
    echo "PYTHON INSTALLATION REQUIRED"
    echo "============================================================================"
    echo ""
    echo "Python 3.12 is required to run this application."
    echo ""
    echo "Installation method:"
    echo "  1. Homebrew (recommended if you have it)"
    echo "  2. Official Python installer (automatic download)"
    echo ""

    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "[OK] Homebrew is installed"
        echo ""
        read -p "Install Python via Homebrew? (Y/N): " USE_BREW

        if [[ "$USE_BREW" =~ ^[Yy]$ ]]; then
            echo "" | tee -a "$LOG_FILE"
            echo "[2/4] Installing Python via Homebrew..." | tee -a "$LOG_FILE"

            brew install python@3.12 2>&1 | tee -a "$LOG_FILE"

            if [ $? -ne 0 ]; then
                echo "[ERROR] Failed to install Python via Homebrew" | tee -a "$LOG_FILE"
                exit 1
            fi

            echo "[OK] Python installed successfully!" | tee -a "$LOG_FILE"
            PYTHON_CMD="python3"
        fi
    fi

    # If not using Homebrew, download official installer
    if [ -z "$PYTHON_CMD" ]; then
        echo "" | tee -a "$LOG_FILE"
        echo "Homebrew not available or not selected."
        echo "Downloading official Python installer..."
        echo ""
        read -p "Continue with official installer? (Y/N): " USE_OFFICIAL

        if [[ ! "$USE_OFFICIAL" =~ ^[Yy]$ ]]; then
            echo "Installation cancelled."
            echo ""
            echo "You can install Python manually from: https://www.python.org/downloads/"
            echo "Then run this installer again."
            exit 1
        fi

        echo "" | tee -a "$LOG_FILE"
        echo "[2/4] Downloading Python 3.12..." | tee -a "$LOG_FILE"

        PYTHON_URL="https://www.python.org/ftp/python/3.12.0/python-3.12.0-macos11.pkg"
        PYTHON_INSTALLER="/tmp/python-3.12.0-macos11.pkg"

        echo "Downloading from: $PYTHON_URL" | tee -a "$LOG_FILE"
        curl -L "$PYTHON_URL" -o "$PYTHON_INSTALLER" 2>&1 | tee -a "$LOG_FILE"

        if [ $? -ne 0 ]; then
            echo "[ERROR] Failed to download Python installer" | tee -a "$LOG_FILE"
            echo "Please install Python manually from: https://www.python.org/downloads/"
            exit 1
        fi

        echo "[OK] Python installer downloaded!" | tee -a "$LOG_FILE"
        echo "" | tee -a "$LOG_FILE"

        echo "[3/4] Installing Python 3.12..." | tee -a "$LOG_FILE"
        echo "This will open the installer. Please follow the prompts."
        echo ""

        # Open the installer
        open "$PYTHON_INSTALLER"

        echo "Waiting for installation to complete..."
        echo "Press Enter after you've finished installing Python..."
        read -p ""

        # Clean up
        rm -f "$PYTHON_INSTALLER"

        # Check if Python is now available
        if command -v python3 &> /dev/null; then
            echo "[OK] Python is now available!" | tee -a "$LOG_FILE"
            python3 --version | tee -a "$LOG_FILE"
            PYTHON_CMD="python3"
        else
            echo "[ERROR] Python installation may have failed" | tee -a "$LOG_FILE"
            echo "Please restart your terminal and try again"
            exit 1
        fi
    fi
fi

echo "" | tee -a "$LOG_FILE"
echo "[4/4] Running AI Gospel Parser installer..." | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Run the main installer
$PYTHON_CMD install.py

if [ $? -ne 0 ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "[ERROR] Installation failed. Check install_log.txt for details." | tee -a "$LOG_FILE"
    echo "Bootstrap log saved to: $LOG_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

echo "" | tee -a "$LOG_FILE"
echo "============================================================================"
echo "INSTALLATION COMPLETE!"
echo "============================================================================"
echo ""
echo "Next steps:"
echo "  1. Read GETTING_STARTED.txt for usage instructions"
echo "  2. Look for the desktop shortcut: 'AI Gospel Parser.command'"
echo "  3. Double-click the shortcut to launch"
echo ""
echo "Bootstrap log saved to: $LOG_FILE"
echo ""

exit 0
