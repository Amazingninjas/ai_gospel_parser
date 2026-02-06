# Building the macOS Installer

This directory contains everything needed to create a professional macOS installer for AI Gospel Parser.

## Two Distribution Options

1. **Application Bundle (.app)** - Double-clickable installer
2. **DMG Image** - Professional disk image for distribution (Recommended)

---

## Option 1: Application Bundle (.app)

### What You Have

The `.app` bundle is already created in this directory:
```
AI Gospel Parser Installer.app/
  Contents/
    Info.plist           - App metadata
    MacOS/
      install-wrapper    - Executable script
    Resources/
      install-macos.sh   - Installation script
```

### How to Use

1. **Test it locally:**
   ```bash
   open "AI Gospel Parser Installer.app"
   ```
   - Double-click should work
   - Will request admin password
   - Runs installation automatically

2. **Distribute the .app:**
   - Zip it: `zip -r "AI-Gospel-Parser-Installer.zip" "AI Gospel Parser Installer.app"`
   - Users download, unzip, and double-click
   - Or create a DMG (see Option 2)

---

## Option 2: DMG Image (Recommended)

A DMG provides a professional installation experience with drag-and-drop.

### Quick Build

```bash
cd installers/macos
./create-dmg.sh
```

This creates: `AI-Gospel-Parser-Installer-1.0.0.dmg`

### What the DMG Contains

When users open the DMG:
- **AI Gospel Parser Installer.app** - The installer
- **Applications** - Shortcut to drag the app to
- **README.txt** - Installation instructions

### Manual DMG Creation (if script fails)

```bash
# Create temporary folder
mkdir dmg-temp
cp -R "AI Gospel Parser Installer.app" dmg-temp/
ln -s /Applications dmg-temp/Applications

# Create DMG
hdiutil create -volname "AI Gospel Parser Installer" \
  -srcfolder dmg-temp \
  -ov -format UDZO \
  AI-Gospel-Parser-Installer-1.0.0.dmg

# Clean up
rm -rf dmg-temp
```

---

## Adding an Icon

For a professional look, add an application icon.

### Step 1: Create Icon File

You need a 1024x1024 PNG image of your logo/icon.

**Convert to ICNS (macOS icon format):**

1. **Using online tool:**
   - Go to: https://cloudconvert.com/png-to-icns
   - Upload your PNG
   - Download the ICNS file

2. **Using iconutil (macOS built-in):**
   ```bash
   # Create icon set directory
   mkdir AppIcon.iconset

   # Create required sizes (use sips or ImageMagick)
   sips -z 16 16     icon.png --out AppIcon.iconset/icon_16x16.png
   sips -z 32 32     icon.png --out AppIcon.iconset/icon_16x16@2x.png
   sips -z 32 32     icon.png --out AppIcon.iconset/icon_32x32.png
   sips -z 64 64     icon.png --out AppIcon.iconset/icon_32x32@2x.png
   sips -z 128 128   icon.png --out AppIcon.iconset/icon_128x128.png
   sips -z 256 256   icon.png --out AppIcon.iconset/icon_128x128@2x.png
   sips -z 256 256   icon.png --out AppIcon.iconset/icon_256x256.png
   sips -z 512 512   icon.png --out AppIcon.iconset/icon_256x256@2x.png
   sips -z 512 512   icon.png --out AppIcon.iconset/icon_512x512.png
   sips -z 1024 1024 icon.png --out AppIcon.iconset/icon_512x512@2x.png

   # Convert to ICNS
   iconutil -c icns AppIcon.iconset
   ```

### Step 2: Add Icon to App

```bash
cp AppIcon.icns "AI Gospel Parser Installer.app/Contents/Resources/"
```

The icon will automatically be used (it's referenced in Info.plist).

---

## Code Signing (Optional but Recommended)

Signing prevents Gatekeeper warnings ("unidentified developer").

### Prerequisites

1. **Apple Developer Account** ($99/year)
2. **Developer ID Application Certificate**
   - Get from: https://developer.apple.com/account/resources/certificates/add

### Sign the App

```bash
# Sign the app bundle
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  "AI Gospel Parser Installer.app"

# Verify signature
codesign --verify --verbose "AI Gospel Parser Installer.app"
spctl -a -t exec -vv "AI Gospel Parser Installer.app"
```

### Sign the DMG

```bash
codesign --force --sign "Developer ID Application: Your Name (TEAM_ID)" \
  AI-Gospel-Parser-Installer-1.0.0.dmg
```

### Notarize (macOS 10.15+)

Required for modern macOS versions:

```bash
# Create app-specific password in Apple ID account
# Submit for notarization
xcrun notarytool submit AI-Gospel-Parser-Installer-1.0.0.dmg \
  --apple-id "your@email.com" \
  --password "app-specific-password" \
  --team-id "TEAM_ID" \
  --wait

# Staple the notarization
xcrun stapler staple AI-Gospel-Parser-Installer-1.0.0.dmg
```

---

## Testing

### Test Locally (Before Distribution)

1. **Test the .app directly:**
   ```bash
   open "AI Gospel Parser Installer.app"
   ```
   - Should open and request password
   - Should run installation
   - Check for errors

2. **Test the DMG:**
   ```bash
   open AI-Gospel-Parser-Installer-1.0.0.dmg
   ```
   - Should mount as a volume
   - Drag to Applications should work
   - Double-click from Applications should work

### Test on Clean Mac

Ideally test on a fresh macOS installation:

1. Create a VM (VMware Fusion, Parallels, or UTM)
2. Install macOS (10.13+ recommended)
3. **Do NOT** install Docker or Git beforehand
4. Copy the DMG to the VM
5. Open and run the installer
6. Verify it:
   - Detects missing Docker/Git
   - Installs dependencies
   - Clones repository
   - Starts application
   - Opens browser automatically

### Test Gatekeeper (if not signed)

```bash
# Simulate what users will see
xattr -d com.apple.quarantine "AI Gospel Parser Installer.app"
```

Users will need to:
1. Right-click the app
2. Select "Open"
3. Click "Open" in the security dialog

---

## Distribution

### Upload to GitHub Releases

```bash
# Create release
gh release create v1.0.0 \
  AI-Gospel-Parser-Installer-1.0.0.dmg \
  --title "AI Gospel Parser v1.0.0" \
  --notes "One-click macOS installer"

# Or upload manually via web interface
```

### Provide SHA256 Checksum

```bash
shasum -a 256 AI-Gospel-Parser-Installer-1.0.0.dmg
```

Include this in release notes so users can verify integrity.

### Update README

Add download link and instructions:

```markdown
### macOS

[⬇️ Download AI-Gospel-Parser-Installer-1.0.0.dmg](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.0/AI-Gospel-Parser-Installer-1.0.0.dmg)

**How to install:**
1. Download the DMG file
2. Open it and drag the installer to Applications
3. Open Applications and double-click "AI Gospel Parser Installer"
4. Enter your password when prompted
5. Wait 10-15 minutes for installation
6. Browser opens automatically!
```

---

## Troubleshooting

### "App is damaged and can't be opened"

This is Gatekeeper blocking unsigned apps.

**Solution for users:**
```bash
xattr -cr "/Applications/AI Gospel Parser Installer.app"
```

Or right-click → Open

**Solution for you:** Sign and notarize the app.

### "install-wrapper" is not executable

```bash
chmod +x "AI Gospel Parser Installer.app/Contents/MacOS/install-wrapper"
chmod +x "AI Gospel Parser Installer.app/Contents/Resources/install-macos.sh"
```

### DMG creation fails

Make sure you have Xcode Command Line Tools:
```bash
xcode-select --install
```

### Icon doesn't show

- Make sure `AppIcon.icns` is in `Contents/Resources/`
- Make sure `Info.plist` references it correctly
- Try clearing icon cache: `sudo rm -rf /Library/Caches/com.apple.iconservices.store`

---

## Advanced: Custom DMG Background

For a really professional DMG:

1. **Create background image** (600x400 pixels)
2. **Mount DMG in read-write mode:**
   ```bash
   hdiutil convert AI-Gospel-Parser-Installer-1.0.0.dmg -format UDRW -o temp.dmg
   hdiutil attach temp.dmg
   ```

3. **Customize appearance:**
   - Open the mounted volume
   - View → Show View Options
   - Drag background image into .background folder
   - Set icon size, arrange icons
   - Close window

4. **Convert back to read-only:**
   ```bash
   hdiutil detach /Volumes/AI\ Gospel\ Parser\ Installer
   hdiutil convert temp.dmg -format UDZO -o AI-Gospel-Parser-Installer-1.0.0.dmg
   rm temp.dmg
   ```

---

## Support

For issues with the installer:

1. Check `/tmp/aigospel-install.log` for errors
2. Check Console.app for system logs
3. Verify Docker Desktop is installed and running
4. Try running the installation script manually:
   ```bash
   bash "AI Gospel Parser Installer.app/Contents/Resources/install-macos.sh"
   ```

## Resources

- Apple Developer Documentation: https://developer.apple.com/documentation/
- Code Signing Guide: https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/
- Notarization Guide: https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution
- DMG Canvas (GUI tool): https://www.araelium.com/dmgcanvas
