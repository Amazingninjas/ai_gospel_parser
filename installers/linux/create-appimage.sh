#!/bin/bash
# ============================================================================
# AI Gospel Parser - Create AppImage (Linux Universal Installer)
# ============================================================================
# This creates a single-file executable that works on most Linux distributions
# ============================================================================

set -e

APP_NAME="AI-Gospel-Parser-Installer"
VERSION="1.0.0"
ARCH="x86_64"
APPIMAGE_NAME="${APP_NAME}-${VERSION}-${ARCH}.AppImage"

echo "============================================"
echo "  Creating AppImage for Linux"
echo "============================================"
echo ""

# Check for appimagetool
if ! command -v appimagetool &> /dev/null; then
    echo "appimagetool is not installed."
    echo ""
    echo "Download it from: https://github.com/AppImage/AppImageKit/releases"
    echo ""
    echo "Quick install:"
    echo "  wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    echo "  chmod +x appimagetool-x86_64.AppImage"
    echo "  sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
    echo ""
    exit 1
fi

# Create AppDir structure
echo "[1/6] Creating AppDir structure..."
APPDIR="${APP_NAME}.AppDir"
rm -rf "$APPDIR"

mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APPDIR/usr/share/metainfo"

# Copy scripts
echo "[2/6] Copying installation scripts..."
cp install-wrapper.sh "$APPDIR/usr/bin/"
cp install-linux.sh "$APPDIR/usr/bin/"
chmod +x "$APPDIR/usr/bin/"*.sh

# Create AppRun (entry point)
echo "[3/6] Creating AppRun entry point..."
cat > "$APPDIR/AppRun" <<'EOF'
#!/bin/bash
# AppImage entry point
SELF="$(readlink -f "$0")"
HERE="${SELF%/*}"
export PATH="${HERE}/usr/bin:${PATH}"

# Run in a terminal if not already in one
if [ -t 0 ]; then
    # Already in terminal
    exec bash "${HERE}/usr/bin/install-wrapper.sh"
else
    # Not in terminal, open one
    if command -v x-terminal-emulator &> /dev/null; then
        x-terminal-emulator -e bash "${HERE}/usr/bin/install-wrapper.sh"
    elif command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash "${HERE}/usr/bin/install-wrapper.sh"
    elif command -v konsole &> /dev/null; then
        konsole -e bash "${HERE}/usr/bin/install-wrapper.sh"
    elif command -v xterm &> /dev/null; then
        xterm -e bash "${HERE}/usr/bin/install-wrapper.sh"
    else
        # Fallback: try to run directly
        exec bash "${HERE}/usr/bin/install-wrapper.sh"
    fi
fi
EOF
chmod +x "$APPDIR/AppRun"

# Create desktop file
echo "[4/6] Creating desktop file..."
cat > "$APPDIR/ai-gospel-parser-installer.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AI Gospel Parser Installer
Comment=Install AI Gospel Parser - Greek NT Study Tool
Exec=AppRun
Icon=ai-gospel-parser-installer
Categories=Utility;System;
Terminal=true
EOF

cp "$APPDIR/ai-gospel-parser-installer.desktop" "$APPDIR/usr/share/applications/"

# Create icon (placeholder - replace with actual icon)
echo "[5/6] Creating icon..."
if [ -f "../../icon.png" ]; then
    cp "../../icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/ai-gospel-parser-installer.png"
    ln -sf "usr/share/icons/hicolor/256x256/apps/ai-gospel-parser-installer.png" "$APPDIR/ai-gospel-parser-installer.png"
else
    echo "  [WARN] No icon.png found. Creating placeholder..."
    # Create a simple placeholder icon
    convert -size 256x256 xc:blue \
        -gravity center \
        -pointsize 48 \
        -fill white \
        -annotate +0+0 "AI\nGospel" \
        "$APPDIR/ai-gospel-parser-installer.png" 2>/dev/null || echo "    Install ImageMagick to auto-generate icon"
fi

# Create AppStream metadata
cat > "$APPDIR/usr/share/metainfo/ai-gospel-parser-installer.appdata.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.amazingninjas.aigospelparser.installer</id>
  <metadata_license>MIT</metadata_license>
  <project_license>MIT</project_license>
  <name>AI Gospel Parser Installer</name>
  <summary>Install AI Gospel Parser - Greek New Testament Study Tool</summary>
  <description>
    <p>
      AI Gospel Parser is a web application for studying the Greek New Testament
      with AI-powered insights, lexicon lookups, and comprehensive reference texts.
    </p>
    <p>Features:</p>
    <ul>
      <li>13,551 Greek NT verses (SBLGNT)</li>
      <li>Strong's Greek Lexicon with morphology</li>
      <li>AI chat assistant for deeper study</li>
      <li>Multiple scholarly reference texts</li>
    </ul>
  </description>
  <url type="homepage">https://github.com/Amazingninjas/ai_gospel_parser</url>
  <developer_name>Amazing Ninjas</developer_name>
  <releases>
    <release version="1.0.0" date="2026-01-31"/>
  </releases>
</component>
EOF

# Build AppImage
echo "[6/6] Building AppImage..."
appimagetool "$APPDIR" "$APPIMAGE_NAME"

# Clean up
rm -rf "$APPDIR"

echo ""
echo "============================================"
echo "  AppImage CREATED SUCCESSFULLY!"
echo "============================================"
echo ""
echo "File: $APPIMAGE_NAME"
echo "Size: $(du -h "$APPIMAGE_NAME" | cut -f1)"
echo ""
echo "To test:"
echo "  chmod +x $APPIMAGE_NAME"
echo "  ./$APPIMAGE_NAME"
echo ""
echo "Users can now run this single file on any Linux distribution!"
echo ""

exit 0
