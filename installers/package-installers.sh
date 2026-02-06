#!/bin/bash
# Package ready-to-use installers for immediate distribution

set -e

VERSION="1.0.1"
RELEASE_DIR="release/v${VERSION}"

echo "============================================"
echo "  Packaging Installers for v${VERSION}"
echo "============================================"
echo ""

# Create release directory
mkdir -p "$RELEASE_DIR"

# Windows - Create tar.gz
echo "[1/3] Packaging Windows installer..."
tar -czf "$RELEASE_DIR/AI-Gospel-Parser-Windows-Installer-${VERSION}.tar.gz" \
  -C installers/windows AI-Gospel-Parser-Installer.vbs launch.bat stop.bat \
  -C ../../portable-installation install-windows.ps1
echo "✓ Windows package created"

# macOS - Create tar.gz
echo "[2/3] Packaging macOS installer..."
tar -czf "$RELEASE_DIR/AI-Gospel-Parser-macOS-Installer-${VERSION}.tar.gz" \
  -C installers/macos "AI Gospel Parser Installer.app"
echo "✓ macOS package created"

# Linux - Create tar.gz
echo "[3/3] Packaging Linux installer..."
tar -czf "$RELEASE_DIR/AI-Gospel-Parser-Linux-Installer-${VERSION}.tar.gz" \
  -C installers/linux \
  ai-gospel-parser-installer.desktop \
  install-wrapper.sh \
  install-linux.sh
echo "✓ Linux package created"

echo ""
echo "============================================"
echo "  Packages Created"
echo "============================================"
echo ""
ls -lh "$RELEASE_DIR"/*.tar.gz
echo ""

# Generate checksums
echo "Generating SHA256 checksums..."
cd "$RELEASE_DIR"
sha256sum *.tar.gz > SHA256SUMS.txt
echo "✓ Checksums generated"
echo ""

cat SHA256SUMS.txt
echo ""
echo "============================================"
echo "Release files ready at: $RELEASE_DIR"
echo "============================================"
