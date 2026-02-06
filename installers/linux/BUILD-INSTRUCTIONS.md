# Building the Linux Installer

This directory contains files to create a double-clickable Linux installer and an AppImage for universal distribution.

## Two Distribution Options

1. **Desktop File (.desktop)** - Double-clickable launcher (simplest)
2. **AppImage** - Universal single-file executable (recommended)

---

## Option 1: Desktop File (Simplest)

### What You Have

The `.desktop` file provides a double-clickable installer for Linux file managers.

**Files:**
- `ai-gospel-parser-installer.desktop` - Desktop entry file
- `install-wrapper.sh` - Wrapper that handles sudo/pkexec
- `install-linux.sh` - Main installation script

### How to Use

#### For Users (Distribution Method):

1. **Package as ZIP:**
   ```bash
   cd installers/linux
   zip -r AI-Gospel-Parser-Installer-Linux.zip \
     ai-gospel-parser-installer.desktop \
     install-wrapper.sh \
     install-linux.sh
   ```

2. **User instructions:**
   - Download and extract the ZIP
   - Right-click `ai-gospel-parser-installer.desktop`
   - Select "Allow Launching" or "Mark as Executable"
   - Double-click to run

#### For Developers (System-Wide Install):

```bash
# Install to system
sudo cp ai-gospel-parser-installer.desktop /usr/share/applications/
sudo cp install-wrapper.sh /usr/local/bin/
sudo cp install-linux.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/install-wrapper.sh
sudo chmod +x /usr/local/bin/install-linux.sh

# Update desktop database
sudo update-desktop-database
```

Users can then find "AI Gospel Parser Installer" in their application menu.

---

## Option 2: AppImage (Recommended)

AppImage creates a single executable file that works on most Linux distributions without installation.

### Prerequisites

1. **appimagetool** - Tool to build AppImages

   ```bash
   # Download
   wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage

   # Make executable
   chmod +x appimagetool-x86_64.AppImage

   # Install system-wide (optional)
   sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
   ```

2. **FUSE** (for running AppImages)

   ```bash
   # Ubuntu/Debian
   sudo apt install fuse libfuse2

   # Fedora
   sudo dnf install fuse fuse-libs

   # Arch
   sudo pacman -S fuse2
   ```

### Build AppImage

```bash
cd installers/linux
./create-appimage.sh
```

This creates: `AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage`

### What Users Get

A single file they can:
1. Download
2. `chmod +x AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage`
3. Double-click or run: `./AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage`

No installation needed, works everywhere!

---

## Adding an Icon

For a professional appearance, add an icon.

### Create Icon

You need a 256x256 PNG file of your logo.

#### Using ImageMagick (if you have SVG):

```bash
convert -density 300 -background none logo.svg -resize 256x256 icon.png
```

#### Using Inkscape (if you have SVG):

```bash
inkscape --export-png=icon.png --export-width=256 --export-height=256 logo.svg
```

### Add to Desktop File

The icon is already referenced in the `.desktop` file:
```desktop
Icon=ai-gospel-parser
```

For system-wide installation:
```bash
sudo cp icon.png /usr/share/icons/hicolor/256x256/apps/ai-gospel-parser.png
sudo gtk-update-icon-cache /usr/share/icons/hicolor/
```

For AppImage, the icon is embedded automatically by the build script.

---

## Distribution

### Option A: Distribute Desktop File + Scripts

**Package as ZIP:**
```bash
cd installers/linux
zip -r AI-Gospel-Parser-Installer-Linux.zip \
  ai-gospel-parser-installer.desktop \
  install-wrapper.sh \
  install-linux.sh \
  README-INSTALLATION.txt
```

Create `README-INSTALLATION.txt`:
```
AI GOSPEL PARSER - LINUX INSTALLATION

1. Extract this ZIP file
2. Right-click: ai-gospel-parser-installer.desktop
3. Select: "Allow Launching" or "Properties" → "Permissions" → "Allow executing as program"
4. Double-click to run the installer
5. Enter your password when prompted
6. Wait 10-15 minutes
7. Browser opens automatically!

Requires:
• Ubuntu 18.04+ / Debian 10+ / Fedora 32+ / Arch Linux
• 8GB RAM (16GB recommended)
• 10GB free disk space
• Internet connection

Support: https://github.com/Amazingninjas/ai_gospel_parser
```

### Option B: Distribute AppImage (Recommended)

Just distribute the single `.AppImage` file!

**Upload to GitHub Releases:**
```bash
gh release create v1.0.0 \
  AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage \
  --title "AI Gospel Parser v1.0.0" \
  --notes "Universal Linux installer (AppImage)"
```

**Provide SHA256 checksum:**
```bash
sha256sum AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage > AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage.sha256
```

### Update README

```markdown
### Linux

[⬇️ Download AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.0/AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage)

**How to install:**
1. Download the AppImage
2. Make it executable: `chmod +x AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage`
3. Run it: `./AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage`
4. Enter your password when prompted
5. Wait 10-15 minutes
6. Browser opens automatically!

**Requirements:** Ubuntu 18.04+, Debian 10+, Fedora 32+, or any recent Linux distribution
```

---

## Testing

### Test Desktop File

```bash
cd installers/linux

# Mark as executable
chmod +x ai-gospel-parser-installer.desktop
chmod +x install-wrapper.sh
chmod +x install-linux.sh

# Run from terminal
./ai-gospel-parser-installer.desktop
```

Or test by double-clicking in your file manager (Nautilus, Dolphin, Thunar, etc.)

### Test AppImage

```bash
chmod +x AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage
./AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage
```

### Test on Different Distributions

Ideally test on multiple distributions:

- **Ubuntu 22.04 LTS** (most common)
- **Fedora Workstation** (RHEL-based testing)
- **Arch Linux** (rolling release testing)
- **Linux Mint** (Ubuntu-based with Cinnamon)
- **Debian 12** (stable base)

Use VirtualBox, VMware, or QEMU/KVM for testing.

### Test Without Docker

Test the installer detects and installs Docker:

1. Create fresh VM without Docker
2. Run installer
3. Verify it installs Docker automatically
4. Verify application starts correctly

---

## Advanced: Snap Package

For even wider distribution, create a Snap:

### Create snapcraft.yaml

```yaml
name: ai-gospel-parser
version: '1.0.0'
summary: Greek New Testament Study Tool
description: |
  AI Gospel Parser is a web application for studying the Greek New Testament
  with AI-powered insights, lexicon lookups, and comprehensive reference texts.

base: core22
confinement: strict
grade: stable

apps:
  ai-gospel-parser:
    command: bin/launch.sh
    plugs:
      - network
      - network-bind
      - docker

parts:
  installer:
    plugin: dump
    source: .
    organize:
      install-linux.sh: bin/install-linux.sh
      launch.sh: bin/launch.sh
```

### Build and Publish

```bash
snapcraft
snapcraft login
snapcraft upload ai-gospel-parser_1.0.0_amd64.snap --release=stable
```

Users can then install with:
```bash
sudo snap install ai-gospel-parser
```

---

## Troubleshooting

### "Permission denied" when running .desktop file

```bash
chmod +x ai-gospel-parser-installer.desktop
gio set ai-gospel-parser-installer.desktop metadata::trusted true
```

### pkexec not found

Install PolicyKit:
```bash
# Ubuntu/Debian
sudo apt install policykit-1

# Fedora
sudo dnf install polkit

# Arch
sudo pacman -S polkit
```

### AppImage won't run

```bash
# Make sure FUSE is installed
sudo apt install fuse libfuse2  # Ubuntu/Debian

# Or extract and run directly
./AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
```

### Icon doesn't show

```bash
# Update icon cache
sudo gtk-update-icon-cache /usr/share/icons/hicolor/
xdg-icon-resource forceupdate

# Or place icon in .local
cp icon.png ~/.local/share/icons/hicolor/256x256/apps/ai-gospel-parser.png
```

---

## Desktop Entry Specification

The `.desktop` file follows the FreeDesktop.org standard:
- Spec: https://specifications.freedesktop.org/desktop-entry-spec/latest/
- Icon Theme Spec: https://specifications.freedesktop.org/icon-theme-spec/latest/

**Categories reference:**
- Utility - Utility applications
- System - System tools
- Development - Development tools
- Education - Educational software

---

## Support

For installer issues:

1. Check terminal output for error messages
2. Verify Docker is installed: `docker --version`
3. Verify Docker is running: `docker info`
4. Check logs: `docker-compose logs`
5. Try manual installation:
   ```bash
   bash install-linux.sh
   ```

## Resources

- AppImage documentation: https://docs.appimage.org/
- Desktop Entry spec: https://specifications.freedesktop.org/desktop-entry-spec/latest/
- Snap documentation: https://snapcraft.io/docs
- Flatpak documentation: https://docs.flatpak.org/
