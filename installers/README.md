# AI Gospel Parser - Professional Distribution Installers

This directory contains production-ready installers for all major platforms, providing a true **one-click** installation experience for non-technical users.

## 📦 What's Included

### 🪟 Windows
- **VBScript Launcher** - Double-click to run (requires one UAC approval)
- **Inno Setup Script** - Compile to professional `.exe` installer
- **Batch Scripts** - Launch and stop scripts
- **Full Build Instructions**

### 🍎 macOS
- **Application Bundle** - Native `.app` that can be double-clicked
- **DMG Creator** - Script to create professional disk image
- **Auto-elevation** - Uses native macOS password dialog
- **Full Build Instructions**

### 🐧 Linux
- **Desktop File** - Double-clickable `.desktop` launcher
- **AppImage Script** - Create universal single-file executable
- **Auto-elevation** - Uses pkexec/sudo with native dialogs
- **Full Build Instructions**

---

## 🎯 Quick Start

### For Users (Download Pre-Built)

**Windows:**
1. Download `AI-Gospel-Parser-Setup-1.0.0.exe` from [Releases](https://github.com/Amazingninjas/ai_gospel_parser/releases)
2. Double-click the installer
3. Follow the prompts
4. Application launches automatically!

**macOS:**
1. Download `AI-Gospel-Parser-Installer-1.0.0.dmg` from [Releases](https://github.com/Amazingninjas/ai_gospel_parser/releases)
2. Open the DMG
3. Drag installer to Applications
4. Double-click from Applications
5. Enter password when prompted
6. Application launches automatically!

**Linux:**
1. Download `AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage` from [Releases](https://github.com/Amazingninjas/ai_gospel_parser/releases)
2. Make executable: `chmod +x AI-Gospel-Parser-Installer-*.AppImage`
3. Run: `./AI-Gospel-Parser-Installer-*.AppImage`
4. Enter password when prompted
5. Application launches automatically!

---

## 🔨 For Developers (Build Installers)

### Windows - Build Professional Installer

**Requirements:**
- [Inno Setup 6.x](https://jrsoftware.org/isinfo.php)
- Icon file (`icon.ico`) - 256x256 pixels

**Build Steps:**
```cmd
cd installers\windows

REM Option 1: Using Inno Setup IDE
REM Open installer.iss and press F9

REM Option 2: Command line
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

**Output:** `output/AI-Gospel-Parser-Setup-1.0.0.exe`

**Quick Alternative (No Compilation):**
- Just distribute `AI-Gospel-Parser-Installer.vbs` + `install-windows.ps1`
- Users double-click the `.vbs` file
- One UAC prompt, then automatic installation

📖 **Full Instructions:** [windows/BUILD-INSTRUCTIONS.md](windows/BUILD-INSTRUCTIONS.md)

---

### macOS - Build DMG Installer

**Requirements:**
- macOS 10.13+
- Xcode Command Line Tools
- Icon file (`AppIcon.icns`) - optional but recommended

**Build Steps:**
```bash
cd installers/macos

# Build DMG
./create-dmg.sh
```

**Output:** `AI-Gospel-Parser-Installer-1.0.0.dmg`

**The DMG Contains:**
- `AI Gospel Parser Installer.app` - Double-clickable installer
- `Applications` shortcut - For drag-and-drop installation
- `README.txt` - Installation instructions

📖 **Full Instructions:** [macos/BUILD-INSTRUCTIONS.md](macos/BUILD-INSTRUCTIONS.md)

---

### Linux - Build AppImage

**Requirements:**
- Linux (any distribution)
- [appimagetool](https://github.com/AppImage/AppImageKit/releases)
- FUSE library

**Build Steps:**
```bash
cd installers/linux

# Install appimagetool (first time only)
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool

# Build AppImage
./create-appimage.sh
```

**Output:** `AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage`

**Quick Alternative (No AppImage Build):**
- Just distribute the `.desktop` file + scripts as ZIP
- Users extract, mark as executable, and double-click

📖 **Full Instructions:** [linux/BUILD-INSTRUCTIONS.md](linux/BUILD-INSTRUCTIONS.md)

---

## 🎨 Customization

### Adding Icons

**Windows:**
- Create `windows/icon.ico` (256x256 pixels)
- Use: https://convertio.co/png-ico/

**macOS:**
- Create `macos/AppIcon.icns` (1024x1024 source)
- Use: https://cloudconvert.com/png-to-icns
- Or use `iconutil` (see macOS build instructions)

**Linux:**
- Create `linux/icon.png` (256x256 pixels)
- Automatically embedded by AppImage build script

### Branding

Edit these files to customize:
- **Version:** Update version numbers in all `.iss`, `.plist`, and script files
- **Publisher:** Change "Amazing Ninjas" to your name/organization
- **URLs:** Update GitHub repository URLs
- **Colors:** Modify terminal colors in scripts

---

## ✅ What Makes These "True One-Click"

### Before (Old Method):
❌ Open PowerShell as Admin
❌ Navigate to Downloads
❌ Type: `powershell -ExecutionPolicy Bypass -File .\install.ps1`
❌ Requires command-line knowledge

### After (New Method):
✅ Download installer
✅ Double-click
✅ (One password/UAC prompt)
✅ Everything else is automatic!

---

## 🧪 Testing Checklist

Before releasing, test on:

**Windows:**
- [ ] Fresh Windows 10 (no Docker)
- [ ] Fresh Windows 11 (no Docker)
- [ ] Windows with Docker already installed
- [ ] Test `.vbs` launcher
- [ ] Test compiled `.exe` installer

**macOS:**
- [ ] macOS 11 Big Sur
- [ ] macOS 12 Monterey
- [ ] macOS 13 Ventura
- [ ] Mac with Docker already installed
- [ ] Test unsigned `.app` (right-click → Open)
- [ ] Test DMG drag-and-drop

**Linux:**
- [ ] Ubuntu 22.04 LTS
- [ ] Fedora Workstation 39
- [ ] Linux Mint 21
- [ ] Arch Linux (rolling)
- [ ] Test `.desktop` file
- [ ] Test AppImage

---

## 📝 Code Signing (Optional but Recommended)

### Windows
- Get certificate from DigiCert, Sectigo, etc. (~$100-500/year)
- Use `signtool` to sign `.exe`
- Prevents SmartScreen warnings

### macOS
- Requires Apple Developer Account ($99/year)
- Use `codesign` and `notarytool`
- Prevents Gatekeeper warnings

### Linux
- No code signing required
- SHA256 checksum is sufficient

📖 **Signing Instructions:** See individual BUILD-INSTRUCTIONS.md files

---

## 🚀 Release Process

### 1. Build All Installers

```bash
# Windows (on Windows machine)
cd installers/windows
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

# macOS (on Mac)
cd installers/macos
./create-dmg.sh

# Linux (on any Linux)
cd installers/linux
./create-appimage.sh
```

### 2. Generate Checksums

```bash
# Windows
certutil -hashfile AI-Gospel-Parser-Setup-1.0.0.exe SHA256

# macOS
shasum -a 256 AI-Gospel-Parser-Installer-1.0.0.dmg

# Linux
sha256sum AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage
```

### 3. Create GitHub Release

```bash
gh release create v1.0.0 \
  windows/output/AI-Gospel-Parser-Setup-1.0.0.exe \
  macos/AI-Gospel-Parser-Installer-1.0.0.dmg \
  linux/AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage \
  --title "AI Gospel Parser v1.0.0" \
  --notes-file RELEASE_NOTES.md
```

### 4. Update README

Update the main project README with download links and installation instructions.

---

## 📊 Comparison with Old Installers

| Feature | Old (portable-installation/) | New (installers/) |
|---------|------------------------------|-------------------|
| **Windows** | Requires PowerShell as Admin + manual command | Double-click `.exe` or `.vbs` |
| **macOS** | Requires Terminal + curl command | Double-click `.app` from DMG |
| **Linux** | Requires Terminal + bash command | Double-click `.AppImage` or `.desktop` |
| **User Experience** | Technical users only | Anyone can install |
| **Professional Look** | Scripts in folder | Native installers |
| **Code Signing** | Not applicable | Supported |
| **Uninstall** | Manual docker-compose down | Native uninstaller (Windows) |

---

## 🐛 Troubleshooting

### Windows

**"Windows protected your PC"**
- Click "More info" → "Run anyway"
- Or get the installer code-signed

**"The installer failed"**
- Make sure Docker Desktop is running
- Check Windows Event Viewer for errors
- Try running `install-windows.ps1` manually

### macOS

**"App is damaged and can't be opened"**
- This is Gatekeeper blocking unsigned apps
- Right-click → Open (instead of double-clicking)
- Or: `xattr -cr "AI Gospel Parser Installer.app"`

**"Installation failed"**
- Check `/tmp/aigospel-install.log`
- Make sure you have internet connection
- Try running `install-macos.sh` manually in Terminal

### Linux

**"Permission denied"**
```bash
chmod +x AI-Gospel-Parser-Installer-*.AppImage
```

**"FUSE not found"**
```bash
# Ubuntu/Debian
sudo apt install fuse libfuse2

# Fedora
sudo dnf install fuse fuse-libs

# Arch
sudo pacman -S fuse2
```

---

## 📚 Additional Resources

- **Inno Setup Documentation:** https://jrsoftware.org/ishelp/
- **Apple Developer Docs:** https://developer.apple.com/documentation/
- **AppImage Documentation:** https://docs.appimage.org/
- **FreeDesktop Spec:** https://specifications.freedesktop.org/

---

## 🤝 Contributing

To improve these installers:

1. Test on different OS versions
2. Report issues with specific versions
3. Submit PRs with improvements
4. Add support for more Linux distributions
5. Improve error messages and logging

---

## 📄 License

These installer scripts are part of the AI Gospel Parser project and are licensed under the MIT License.

---

**Need Help?** Open an issue at: https://github.com/Amazingninjas/ai_gospel_parser/issues
