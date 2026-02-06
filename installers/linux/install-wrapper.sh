#!/bin/bash
# ============================================================================
# AI Gospel Parser - Linux Installer Wrapper
# ============================================================================
# This wrapper can be executed by double-clicking the .desktop file
# It handles privilege elevation and runs the installation
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_SCRIPT="$SCRIPT_DIR/install-linux.sh"

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "============================================"
echo "  AI GOSPEL PARSER - INSTALLER"
echo "============================================"
echo ""

# Check if install script exists
if [ ! -f "$INSTALL_SCRIPT" ]; then
    echo -e "${RED}Error: Could not find install-linux.sh${NC}"
    echo "Expected location: $INSTALL_SCRIPT"
    exit 1
fi

# Show welcome message
echo -e "${CYAN}This installer will:${NC}"
echo "  • Check and install Docker (if needed)"
echo "  • Check and install Git (if needed)"
echo "  • Download AI Gospel Parser"
echo "  • Start the application"
echo ""
echo -e "${YELLOW}Installation may take 10-15 minutes.${NC}"
echo ""

# Prompt user to continue
read -p "Continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

echo ""

# Check for required privilege escalation tools
if command -v pkexec &> /dev/null; then
    # Use pkexec (PolicyKit) - graphical password prompt
    echo -e "${GREEN}[INFO]${NC} Using PolicyKit for authentication..."
    pkexec bash "$INSTALL_SCRIPT"
elif command -v sudo &> /dev/null; then
    # Fallback to sudo
    echo -e "${GREEN}[INFO]${NC} Using sudo for authentication..."
    sudo bash "$INSTALL_SCRIPT"
else
    # No privilege escalation available, try running directly
    echo -e "${YELLOW}[WARN]${NC} No privilege escalation tool found."
    echo -e "${YELLOW}[WARN]${NC} Attempting to run without root (may fail)..."
    bash "$INSTALL_SCRIPT"
fi

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo -e "  ${GREEN}INSTALLATION COMPLETE!${NC}"
    echo "============================================"
    echo ""
    echo "Opening browser in 3 seconds..."
    sleep 3

    # Try to open browser
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:3000" &
    elif command -v gnome-open &> /dev/null; then
        gnome-open "http://localhost:3000" &
    elif command -v kde-open &> /dev/null; then
        kde-open "http://localhost:3000" &
    else
        echo ""
        echo "Please open your browser to: http://localhost:3000"
    fi

    echo ""
    echo -e "${CYAN}Application URLs:${NC}"
    echo "  Frontend: http://localhost:3000"
    echo "  API Docs: http://localhost:8000/docs"
    echo ""
else
    echo ""
    echo "============================================"
    echo -e "  ${RED}INSTALLATION FAILED${NC}"
    echo "============================================"
    echo ""
    echo "Check the error messages above for details."
    echo ""
    echo "Common issues:"
    echo "  • Docker not installed or not running"
    echo "  • No internet connection"
    echo "  • Port 3000 or 8000 already in use"
    echo ""
    echo "For help, visit:"
    echo "  https://github.com/Amazingninjas/ai_gospel_parser/issues"
    echo ""
    exit 1
fi

exit 0
