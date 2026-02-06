# Building the .exe Installer - Quick Guide

## Option 1: Build on Windows (5 minutes)

### Prerequisites
1. **Windows 10/11** machine
2. **Inno Setup 6** - Download: https://jrsoftware.org/isinfo.php

### Steps

1. **Install Inno Setup**
   - Download from https://jrsoftware.org/isinfo.php
   - Run the installer
   - Use default installation path: `C:\Program Files (x86)\Inno Setup 6\`

2. **Clone the repository** (if not already)
   ```powershell
   git clone https://github.com/Amazingninjas/ai_gospel_parser.git
   cd ai_gospel_parser
   ```

3. **Build the .exe**

   **Option A: Double-click (Easiest)**
   - Navigate to `installers\windows\`
   - Double-click `build-exe.bat`
   - Wait ~30 seconds
   - Done!

   **Option B: Command Line**
   ```powershell
   cd installers\windows
   .\build-exe.bat
   ```

   **Option C: Inno Setup IDE**
   - Open Inno Setup Compiler
   - File → Open → Select `installers\windows\installer.iss`
   - Build → Compile (or press F9)

4. **Find your .exe**
   ```
   Location: installers\windows\output\AI-Gospel-Parser-Setup-1.0.1.exe
   Size: ~3-5 KB (it's tiny because it downloads everything)
   ```

5. **Test it**
   - Double-click the .exe
   - Follow the installation wizard
   - Verify it installs correctly

6. **Upload to GitHub**
   - Go to: https://github.com/Amazingninjas/ai_gospel_parser/releases
   - Edit v1.0.1 release (or create new one)
   - Upload the .exe file
   - Update download links in README

---

## Option 2: GitHub Actions (Automated - Recommended)

The repository is already configured with GitHub Actions to build automatically!

### Trigger Manual Build

1. Go to: https://github.com/Amazingninjas/ai_gospel_parser/actions
2. Click "Build Windows Installer" workflow
3. Click "Run workflow" button
4. Wait ~2-3 minutes for build to complete
5. Download the artifact from the workflow run

### Automatic Build on Tag

When you create a version tag, it builds automatically:

```bash
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1
```

The .exe will be built and automatically attached to the GitHub release!

---

## Option 3: Build on Linux/Mac (using Wine)

If you don't have Windows, you can use Wine:

### Ubuntu/Debian
```bash
# Install Wine
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install wine wine32 wine64

# Install Inno Setup in Wine
wget https://jrsoftware.org/download.php/is.exe
wine is.exe

# Build
cd installers/windows
wine "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### macOS
```bash
# Install Wine via Homebrew
brew install --cask wine-stable

# Install Inno Setup
wine ~/Downloads/innosetup-6.exe

# Build
cd installers/windows
wine "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

---

## What the .exe Installer Does

When users run the .exe:

1. **Welcome screen** - Shows AI Gospel Parser logo and description
2. **License agreement** - MIT License
3. **Installation directory** - Default: `C:\Program Files\AI Gospel Parser`
4. **Select components** - Desktop shortcut (optional)
5. **Ready to install** - Summary screen
6. **Installation** - Copies files, creates shortcuts
7. **Docker check** - Verifies Docker Desktop is installed
   - If not installed: Opens Docker download page
8. **Run installer** - Optionally runs the PowerShell setup immediately
9. **Finish** - Shows completion message with shortcuts

### Files Installed

```
C:\Program Files\AI Gospel Parser\
├── install-windows.ps1    (PowerShell installer)
├── launch.bat             (Quick launch)
├── stop.bat               (Stop application)
├── docker-compose.yml     (Docker configuration)
├── .env                   (Environment variables)
└── README.md              (Documentation)
```

### Shortcuts Created

**Start Menu:**
- AI Gospel Parser (launches application)
- Stop AI Gospel Parser (stops containers)
- Open in Browser (opens http://localhost:3000)
- Uninstall

**Desktop:** (optional)
- AI Gospel Parser

---

## Troubleshooting

### "Inno Setup not found"

- Make sure you installed Inno Setup to the default location
- Or edit `build-exe.bat` line 13 to point to your installation

### "installer.iss not found"

- Make sure you're in the `installers\windows\` directory
- Run: `cd installers\windows` then try again

### Compilation errors

- Check that all file paths in `installer.iss` are correct
- Make sure `install-windows.ps1` exists two directories up
- Check the error messages in Inno Setup output

### .exe won't run

- The .exe is just an installer, not the application itself
- Right-click → Properties → Unblock (if downloaded from internet)
- Run as Administrator if needed

---

## After Building

### Test Locally
```powershell
# Run the installer
.\output\AI-Gospel-Parser-Setup-1.0.1.exe

# Test installation
# Should install to C:\Program Files\AI Gospel Parser
# Should create Start Menu shortcuts
# Should check for Docker
```

### Upload to GitHub
```bash
# Option 1: Using gh CLI
gh release upload v1.0.1 installers/windows/output/AI-Gospel-Parser-Setup-1.0.1.exe

# Option 2: Web interface
# Go to: https://github.com/Amazingninjas/ai_gospel_parser/releases
# Edit v1.0.1 release
# Drag and drop the .exe file
```

### Update README
```markdown
### Windows

[⬇️ Download AI-Gospel-Parser-Setup-1.0.1.exe](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.1/AI-Gospel-Parser-Setup-1.0.1.exe)

**How to install:**
1. Download the .exe
2. Double-click to run
3. Follow the installation wizard
4. Application launches automatically!
```

---

## Code Signing (Optional)

For production releases, sign the .exe to avoid Windows SmartScreen warnings:

```powershell
# Get a code signing certificate from DigiCert, Sectigo, etc.
# Cost: ~$100-500/year

# Sign the executable
signtool sign /f certificate.pfx /p password /tr http://timestamp.digicert.com /td sha256 /fd sha256 "output\AI-Gospel-Parser-Setup-1.0.1.exe"
```

---

## Summary

**Easiest method:** Use GitHub Actions (no Windows machine needed!)
**Fastest method:** Run `build-exe.bat` on Windows (30 seconds)
**Most control:** Use Inno Setup IDE (full customization)

**Result:** Professional Windows installer that users can trust and easily install!

---

**Ready to build?**

```bash
cd installers/windows
./build-exe.bat
```

Or just push to trigger GitHub Actions! 🚀
