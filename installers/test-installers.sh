#!/bin/bash
# Test script to verify all installer files are properly structured

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "============================================"
echo "  Installer Structure Test"
echo "============================================"
echo ""

PASS=0
FAIL=0

test_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} File exists: $1"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} Missing file: $1"
        ((FAIL++))
        return 1
    fi
}

test_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✓${NC} Executable: $1"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} Not executable: $1"
        ((FAIL++))
        return 1
    fi
}

test_syntax() {
    if bash -n "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Valid syntax: $1"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} Syntax error: $1"
        ((FAIL++))
        return 1
    fi
}

echo -e "${CYAN}[1/3] Testing Windows Installers${NC}"
echo "-------------------------------------------"
cd installers/windows

test_file "AI-Gospel-Parser-Installer.vbs"
test_file "installer.iss"
test_file "launch.bat"
test_file "stop.bat"
test_file "post-install-info.txt"
test_file "BUILD-INSTRUCTIONS.md"

# Check if VBScript references install-windows.ps1
if grep -q "install-windows.ps1" AI-Gospel-Parser-Installer.vbs; then
    echo -e "${GREEN}✓${NC} VBScript references install-windows.ps1"
    ((PASS++))
else
    echo -e "${RED}✗${NC} VBScript missing reference to install-windows.ps1"
    ((FAIL++))
fi

# Check Inno Setup references
if grep -q "AppName" installer.iss && grep -q "AppVersion" installer.iss; then
    echo -e "${GREEN}✓${NC} Inno Setup has required metadata"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Inno Setup missing metadata"
    ((FAIL++))
fi

echo ""
echo -e "${CYAN}[2/3] Testing macOS Installers${NC}"
echo "-------------------------------------------"
cd ../macos

test_file "AI Gospel Parser Installer.app/Contents/Info.plist"
test_file "AI Gospel Parser Installer.app/Contents/MacOS/install-wrapper"
test_executable "AI Gospel Parser Installer.app/Contents/MacOS/install-wrapper"
test_file "AI Gospel Parser Installer.app/Contents/Resources/install-macos.sh"
test_executable "AI Gospel Parser Installer.app/Contents/Resources/install-macos.sh"
test_file "create-dmg.sh"
test_executable "create-dmg.sh"
test_file "BUILD-INSTRUCTIONS.md"

test_syntax "AI Gospel Parser Installer.app/Contents/MacOS/install-wrapper"
test_syntax "create-dmg.sh"

# Check if Info.plist has required keys
if grep -q "CFBundleExecutable" "AI Gospel Parser Installer.app/Contents/Info.plist"; then
    echo -e "${GREEN}✓${NC} Info.plist has CFBundleExecutable"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Info.plist missing CFBundleExecutable"
    ((FAIL++))
fi

echo ""
echo -e "${CYAN}[3/3] Testing Linux Installers${NC}"
echo "-------------------------------------------"
cd ../linux

test_file "ai-gospel-parser-installer.desktop"
test_file "install-wrapper.sh"
test_executable "install-wrapper.sh"
test_file "install-linux.sh"
test_executable "install-linux.sh"
test_file "create-appimage.sh"
test_executable "create-appimage.sh"
test_file "BUILD-INSTRUCTIONS.md"

test_syntax "install-wrapper.sh"
test_syntax "install-linux.sh"
test_syntax "create-appimage.sh"

# Check desktop file keys
if grep -q "^Exec=" ai-gospel-parser-installer.desktop && \
   grep -q "^Name=" ai-gospel-parser-installer.desktop && \
   grep -q "^Type=" ai-gospel-parser-installer.desktop; then
    echo -e "${GREEN}✓${NC} Desktop file has required keys"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Desktop file missing required keys"
    ((FAIL++))
fi

echo ""
echo "============================================"
echo "  Test Results"
echo "============================================"
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Installers are ready to use!"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    echo ""
    echo "Please fix the issues above before distributing."
    exit 1
fi
