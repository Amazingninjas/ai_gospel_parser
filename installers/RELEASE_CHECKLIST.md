# Release Checklist - Professional Installers

Use this checklist when preparing a new release with the professional installers.

## Pre-Release Tasks

### 1. Version Bump

Update version numbers in all files:

- [ ] `installers/windows/installer.iss` - Line 9: `#define MyAppVersion "1.0.0"`
- [ ] `installers/macos/AI Gospel Parser Installer.app/Contents/Info.plist` - Lines 29-32
- [ ] `installers/linux/create-appimage.sh` - Line 9: `VERSION="1.0.0"`
- [ ] `README.md` - Badge and download links
- [ ] `CHANGELOG.md` - Add new version section
- [ ] `docker-compose.yml` - Image tags (if applicable)

### 2. Update Documentation

- [ ] Review and update `README.md`
- [ ] Update `CHANGELOG.md` with all changes since last release
- [ ] Create/update `RELEASE_NOTES.md` for this version
- [ ] Update screenshots if UI changed
- [ ] Review all build instructions

### 3. Prepare Icons (if not done)

#### Windows
- [ ] Create `installers/windows/icon.ico` (256x256)
- [ ] Create `installers/windows/wizard-image.bmp` (164x314) - optional
- [ ] Create `installers/windows/wizard-small-image.bmp` (55x55) - optional

#### macOS
- [ ] Create `installers/macos/AppIcon.icns` (1024x1024 source)
- [ ] Add to `AI Gospel Parser Installer.app/Contents/Resources/`

#### Linux
- [ ] Create `installers/linux/icon.png` (256x256)

## Build Process

### Windows Installer

- [ ] Open Windows machine (or Windows VM)
- [ ] Install Inno Setup 6.x if not already installed
- [ ] Open `installers/windows/installer.iss` in Inno Setup
- [ ] Build → Compile (or F9)
- [ ] Verify output in `installers/windows/output/`
- [ ] Test the `.exe` installer:
  - [ ] On Windows 10
  - [ ] On Windows 11
  - [ ] With Docker already installed
  - [ ] Without Docker (should prompt to install)
- [ ] Note any warnings or errors
- [ ] (Optional) Code sign the executable

**Output:** `AI-Gospel-Parser-Setup-1.0.0.exe`

### macOS DMG

- [ ] Open macOS machine (or macOS VM)
- [ ] Ensure Xcode Command Line Tools installed
- [ ] Navigate to `installers/macos/`
- [ ] Run `./create-dmg.sh`
- [ ] Verify output DMG created
- [ ] Mount DMG and verify contents:
  - [ ] Installer.app present
  - [ ] Applications symlink works
  - [ ] README.txt present
- [ ] Test the installer:
  - [ ] On macOS 11 Big Sur
  - [ ] On macOS 12 Monterey
  - [ ] On macOS 13 Ventura or later
  - [ ] Right-click → Open (for unsigned)
- [ ] (Optional) Code sign and notarize

**Output:** `AI-Gospel-Parser-Installer-1.0.0.dmg`

### Linux AppImage

- [ ] Open Linux machine (Ubuntu recommended)
- [ ] Ensure `appimagetool` is installed
- [ ] Navigate to `installers/linux/`
- [ ] Run `./create-appimage.sh`
- [ ] Verify AppImage created
- [ ] Test the AppImage:
  - [ ] On Ubuntu 22.04 LTS
  - [ ] On Fedora Workstation
  - [ ] On Linux Mint
  - [ ] On Arch Linux
  - [ ] With and without Docker installed
- [ ] Verify file permissions (should be executable)

**Output:** `AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage`

## Generate Checksums

### Windows
```cmd
cd installers\windows\output
certutil -hashfile AI-Gospel-Parser-Setup-1.0.0.exe SHA256 > AI-Gospel-Parser-Setup-1.0.0.exe.sha256
```

- [ ] SHA256 checksum generated

### macOS
```bash
cd installers/macos
shasum -a 256 AI-Gospel-Parser-Installer-1.0.0.dmg > AI-Gospel-Parser-Installer-1.0.0.dmg.sha256
```

- [ ] SHA256 checksum generated

### Linux
```bash
cd installers/linux
sha256sum AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage > AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage.sha256
```

- [ ] SHA256 checksum generated

## Create GitHub Release

### Prepare Release Files

Copy all files to a `release/` directory:

```bash
mkdir -p release/v1.0.0

# Windows
cp installers/windows/output/AI-Gospel-Parser-Setup-1.0.0.exe release/v1.0.0/
cp installers/windows/output/AI-Gospel-Parser-Setup-1.0.0.exe.sha256 release/v1.0.0/

# macOS
cp installers/macos/AI-Gospel-Parser-Installer-1.0.0.dmg release/v1.0.0/
cp installers/macos/AI-Gospel-Parser-Installer-1.0.0.dmg.sha256 release/v1.0.0/

# Linux
cp installers/linux/AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage release/v1.0.0/
cp installers/linux/AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage.sha256 release/v1.0.0/
```

- [ ] All release files in `release/v1.0.0/`

### Create Git Tag

```bash
git add .
git commit -m "Release v1.0.0 with professional installers"
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main
git push origin v1.0.0
```

- [ ] Code committed
- [ ] Tag created and pushed

### Create GitHub Release

#### Option 1: Using GitHub CLI

```bash
gh release create v1.0.0 \
  release/v1.0.0/AI-Gospel-Parser-Setup-1.0.0.exe \
  release/v1.0.0/AI-Gospel-Parser-Setup-1.0.0.exe.sha256 \
  release/v1.0.0/AI-Gospel-Parser-Installer-1.0.0.dmg \
  release/v1.0.0/AI-Gospel-Parser-Installer-1.0.0.dmg.sha256 \
  release/v1.0.0/AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage \
  release/v1.0.0/AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage.sha256 \
  --title "AI Gospel Parser v1.0.0 - Professional Installers" \
  --notes-file RELEASE_NOTES.md
```

- [ ] Release created via CLI

#### Option 2: Using GitHub Web Interface

1. Go to: https://github.com/Amazingninjas/ai_gospel_parser/releases/new
2. Tag: `v1.0.0`
3. Release title: `AI Gospel Parser v1.0.0 - Professional Installers`
4. Description: Paste contents of `RELEASE_NOTES.md`
5. Attach files:
   - [ ] `AI-Gospel-Parser-Setup-1.0.0.exe`
   - [ ] `AI-Gospel-Parser-Setup-1.0.0.exe.sha256`
   - [ ] `AI-Gospel-Parser-Installer-1.0.0.dmg`
   - [ ] `AI-Gospel-Parser-Installer-1.0.0.dmg.sha256`
   - [ ] `AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage`
   - [ ] `AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage.sha256`
6. Click "Publish release"

- [ ] Release published on GitHub

## Update Documentation

### Update Main README.md

Update download links to point to new release:

```markdown
## 🎯 One-Click Installer (Easiest)

### Windows

[⬇️ Download AI-Gospel-Parser-Setup-1.0.0.exe](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.0/AI-Gospel-Parser-Setup-1.0.0.exe)

**How to install:**
1. Download the installer
2. Double-click to run
3. Follow the prompts
4. Application launches automatically!

### macOS

[⬇️ Download AI-Gospel-Parser-Installer-1.0.0.dmg](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.0/AI-Gospel-Parser-Installer-1.0.0.dmg)

**How to install:**
1. Download and open the DMG
2. Drag installer to Applications
3. Double-click from Applications
4. Enter password when prompted
5. Application launches automatically!

### Linux

[⬇️ Download AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.0/AI-Gospel-Parser-Installer-1.0.0-x86_64.AppImage)

**How to install:**
1. Download the AppImage
2. Make executable: `chmod +x AI-Gospel-Parser-Installer-*.AppImage`
3. Run: `./AI-Gospel-Parser-Installer-*.AppImage`
4. Enter password when prompted
5. Application launches automatically!
```

- [ ] README.md updated with new download links
- [ ] Version badge updated
- [ ] Screenshots updated (if needed)

### Portable Installation Directory

Update `portable-installation/README.txt` and `START-HERE.txt` to mention the new professional installers:

- [ ] Add note about professional installers being available
- [ ] Link to GitHub releases page

## Announcement & Marketing

### Social Media Posts

Prepare announcements for:

- [ ] Twitter/X
- [ ] LinkedIn
- [ ] Reddit (r/programming, r/linux, r/opensource)
- [ ] Hacker News (Show HN)
- [ ] Product Hunt (if applicable)

**Example Post:**
```
🎉 AI Gospel Parser v1.0.0 is now available!

✅ True one-click installers for Windows, macOS, and Linux
✅ 13,551 Greek NT verses with AI-powered analysis
✅ Strong's Lexicon with morphology
✅ Real-time AI chat assistant

Download: https://github.com/Amazingninjas/ai_gospel_parser/releases

#OpenSource #Bible #GreekNT #AI
```

### Update Project Website (if applicable)

- [ ] Update homepage with new version
- [ ] Update download page
- [ ] Add release announcement blog post

## Post-Release Monitoring

### First 24 Hours

- [ ] Monitor GitHub issues for bug reports
- [ ] Check GitHub Discussions for questions
- [ ] Watch download statistics
- [ ] Test installers on clean machines (if reports come in)

### First Week

- [ ] Respond to all issues and questions
- [ ] Create FAQ based on common questions
- [ ] Consider hotfix release if critical bugs found
- [ ] Thank contributors and users

## Rollback Plan (If Needed)

If critical issues are discovered:

1. [ ] Add warning to release notes
2. [ ] Create issue tracking the problem
3. [ ] Prepare hotfix
4. [ ] Release v1.0.1 with fix
5. [ ] Update download links to new version

## Archive

After release is stable:

- [ ] Archive release files locally
- [ ] Document lessons learned
- [ ] Update this checklist for next release
- [ ] Celebrate! 🎉

---

## Notes for Next Release

Use this section to document improvements for the next release cycle:

-
-
-

---

**Release Manager:** ___________________
**Release Date:** ___________________
**Release Version:** v1.0.0
