#!/bin/bash
################################################################################
# AI Gospel Parser - Linux Bootstrap Installer
# This script checks for Python and installs it automatically if needed
################################################################################

echo "============================================================================"
echo "AI GOSPEL PARSER - LINUX INSTALLER"
echo "============================================================================"
echo ""
echo "This installer will:"
echo "  1. Check if Python is installed"
echo "  2. Install Python 3.12 if needed (via system package manager)"
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
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)' 2>/dev/null)
    if [ $? -eq 0 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
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
    echo "Python 3.8+ is required to run this application."
    echo ""

    # Detect Linux distribution
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    else
        DISTRO="unknown"
    fi

    echo "Detected distribution: $DISTRO" | tee -a "$LOG_FILE"
    echo ""

    # Determine package manager and Python package
    case "$DISTRO" in
        ubuntu|debian|linuxmint|pop)
            PKG_MANAGER="apt"
            PYTHON_PKG="python3 python3-pip python3-venv"
            UPDATE_CMD="sudo apt update"
            INSTALL_CMD="sudo apt install -y"
            ;;
        fedora|rhel|centos|rocky|almalinux)
            PKG_MANAGER="dnf"
            PYTHON_PKG="python3 python3-pip"
            UPDATE_CMD="sudo dnf check-update"
            INSTALL_CMD="sudo dnf install -y"
            ;;
        arch|manjaro)
            PKG_MANAGER="pacman"
            PYTHON_PKG="python python-pip"
            UPDATE_CMD="sudo pacman -Sy"
            INSTALL_CMD="sudo pacman -S --noconfirm"
            ;;
        opensuse|suse)
            PKG_MANAGER="zypper"
            PYTHON_PKG="python3 python3-pip"
            UPDATE_CMD="sudo zypper refresh"
            INSTALL_CMD="sudo zypper install -y"
            ;;
        *)
            echo "[!] Unknown distribution: $DISTRO" | tee -a "$LOG_FILE"
            echo ""
            echo "Please install Python 3.8+ manually:"
            echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
            echo "  - Fedora/RHEL: sudo dnf install python3 python3-pip"
            echo "  - Arch: sudo pacman -S python python-pip"
            echo ""
            echo "Then run this installer again."
            exit 1
            ;;
    esac

    echo "Will use package manager: $PKG_MANAGER" | tee -a "$LOG_FILE"
    echo "Python packages to install: $PYTHON_PKG" | tee -a "$LOG_FILE"
    echo ""
    echo "Commands to run:"
    echo "  $UPDATE_CMD"
    echo "  $INSTALL_CMD $PYTHON_PKG"
    echo ""
    read -p "Install Python now? (Y/N): " INSTALL_PYTHON

    if [[ ! "$INSTALL_PYTHON" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        echo ""
        echo "You can install Python manually with:"
        echo "  $INSTALL_CMD $PYTHON_PKG"
        echo ""
        echo "Then run this installer again."
        exit 1
    fi

    echo "" | tee -a "$LOG_FILE"
    echo "[2/4] Updating package manager..." | tee -a "$LOG_FILE"

    $UPDATE_CMD 2>&1 | tee -a "$LOG_FILE"

    echo "" | tee -a "$LOG_FILE"
    echo "[3/4] Installing Python..." | tee -a "$LOG_FILE"

    $INSTALL_CMD $PYTHON_PKG 2>&1 | tee -a "$LOG_FILE"

    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install Python" | tee -a "$LOG_FILE"
        echo "Please try installing manually:"
        echo "  $INSTALL_CMD $PYTHON_PKG"
        exit 1
    fi

    echo "[OK] Python installed successfully!" | tee -a "$LOG_FILE"

    # Check if Python is now available
    if command -v python3 &> /dev/null; then
        echo "[OK] Python is now available!" | tee -a "$LOG_FILE"
        python3 --version | tee -a "$LOG_FILE"
        PYTHON_CMD="python3"
    else
        echo "[ERROR] Python installation may have failed" | tee -a "$LOG_FILE"
        echo "Please check the error messages above"
        exit 1
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
echo "  2. Look for the desktop shortcut: 'ai-gospel-parser.desktop'"
echo "  3. Double-click the shortcut to launch (or run from terminal)"
echo ""
echo "Bootstrap log saved to: $LOG_FILE"
echo ""

exit 0
