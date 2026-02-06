#!/bin/bash
# ============================================================================
# AI Gospel Parser - Create macOS DMG Installer
# ============================================================================
# This script creates a distributable DMG file containing the .app installer
# ============================================================================

set -e

APP_NAME="AI Gospel Parser Installer"
DMG_NAME="AI-Gospel-Parser-Installer-1.0.0"
APP_PATH="AI Gospel Parser Installer.app"
DMG_TEMP="dmg-temp"

echo "============================================"
echo "  Creating macOS DMG Installer"
echo "============================================"
echo ""

# Check if app exists
if [ ! -d "$APP_PATH" ]; then
    echo "Error: Could not find '$APP_PATH'"
    echo "Make sure you're in the installers/macos directory"
    exit 1
fi

# Clean up any previous DMG files
echo "[1/5] Cleaning up previous builds..."
rm -rf "$DMG_TEMP"
rm -f "$DMG_NAME.dmg"
rm -f "$DMG_NAME-compressed.dmg"

# Create temporary DMG directory
echo "[2/5] Creating temporary DMG directory..."
mkdir -p "$DMG_TEMP"

# Copy app to temp directory
echo "[3/5] Copying application..."
cp -R "$APP_PATH" "$DMG_TEMP/"

# Create symbolic link to Applications folder
echo "[4/5] Creating Applications folder link..."
ln -s /Applications "$DMG_TEMP/Applications"

# Add README
cat > "$DMG_TEMP/README.txt" <<EOF
AI GOSPEL PARSER - INSTALLATION

QUICK START:
============
1. Drag "AI Gospel Parser Installer.app" to the Applications folder
2. Open Applications and double-click "AI Gospel Parser Installer"
3. Enter your password when prompted
4. Wait for installation to complete (10-15 minutes)
5. Browser opens automatically to http://localhost:3000

WHAT IT INSTALLS:
=================
• Docker Desktop (if not already installed)
• Git (if not already installed)
• AI Gospel Parser application

SYSTEM REQUIREMENTS:
====================
• macOS 10.13 (High Sierra) or later
• 8GB RAM minimum (16GB recommended)
• 10GB free disk space
• Internet connection

SUPPORT:
========
GitHub: https://github.com/Amazingninjas/ai_gospel_parser
Issues: https://github.com/Amazingninjas/ai_gospel_parser/issues
EOF

# Create DMG
echo "[5/5] Creating DMG image..."
hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_TEMP" -ov -format UDZO "$DMG_NAME.dmg"

# Clean up
echo "Cleaning up temporary files..."
rm -rf "$DMG_TEMP"

echo ""
echo "============================================"
echo "  DMG CREATED SUCCESSFULLY!"
echo "============================================"
echo ""
echo "File: $DMG_NAME.dmg"
echo "Size: $(du -h "$DMG_NAME.dmg" | cut -f1)"
echo ""
echo "You can now distribute this DMG file!"
echo ""

# Show in Finder
if command -v open &> /dev/null; then
    open .
fi

exit 0
