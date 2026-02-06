# Building the Windows Installer

This directory contains the Inno Setup script to create a professional Windows installer for AI Gospel Parser.

## Prerequisites

1. **Inno Setup 6.x** - Download from: https://jrsoftware.org/isinfo.php
   - Install with default options
   - Add to PATH (optional but recommended)

2. **Icon File** - Create or provide `icon.ico` (256x256 pixels recommended)
   - Use an online converter if you have a PNG: https://convertio.co/png-ico/

3. **Wizard Images** (Optional but professional looking):
   - `wizard-image.bmp` - 164x314 pixels (left side of installer)
   - `wizard-small-image.bmp` - 55x55 pixels (top corner)

## Quick Build

### Option 1: Using Inno Setup IDE (Easiest)

1. Open Inno Setup Compiler
2. File → Open → Select `installer.iss`
3. Build → Compile (or press F9)
4. The installer will be created in `output/AI-Gospel-Parser-Setup-1.0.0.exe`

### Option 2: Command Line

```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

The compiled installer will be in: `output/AI-Gospel-Parser-Setup-1.0.0.exe`

## Creating Icon Files

If you don't have icon files yet:

### From PNG/SVG:

1. **Online Method:**
   - Go to: https://convertio.co/png-ico/
   - Upload your logo (PNG or SVG)
   - Convert to ICO with multiple sizes (16, 32, 48, 64, 128, 256)
   - Download and save as `icon.ico`

2. **Using GIMP (Free):**
   - Open your PNG in GIMP
   - File → Export As
   - Change filename to `icon.ico`
   - Check "Compressed (PNG)" in the dialog
   - Export

### Creating Wizard Images:

1. **wizard-image.bmp** (164x314 pixels):
   - Create a 164x314 pixel image in any image editor
   - Use your brand colors/theme
   - Can include logo and product name
   - Save as 24-bit BMP

2. **wizard-small-image.bmp** (55x55 pixels):
   - Create a 55x55 pixel square image
   - Usually your app icon or logo
   - Save as 24-bit BMP

**Quick method:** Use placeholder images from Inno Setup:
```
C:\Program Files (x86)\Inno Setup 6\WizModernImage.bmp
C:\Program Files (x86)\Inno Setup 6\WizModernSmallImage.bmp
```

## What the Installer Does

The generated installer:

1. ✅ Checks for Docker Desktop (required)
2. ✅ Installs to `C:\Program Files\AI Gospel Parser`
3. ✅ Creates Start Menu shortcuts
4. ✅ Creates Desktop shortcut (optional)
5. ✅ Runs the setup script (installs Git, clones repo, starts app)
6. ✅ Opens browser to http://localhost:3000
7. ✅ Provides easy uninstall

## Customization

Edit `installer.iss` to customize:

- **Version:** Line 9: `#define MyAppVersion "1.0.0"`
- **Publisher:** Line 10: `#define MyAppPublisher "Your Name"`
- **Installation path:** Line 19: `DefaultDirName={autopf}\{#MyAppName}`
- **Shortcuts:** Lines 85-94: Add/remove shortcuts

## Code Signing (Optional but Recommended)

For production distribution, sign your installer:

1. **Get a Code Signing Certificate:**
   - DigiCert, Sectigo, or other trusted CA
   - ~$100-500/year

2. **Sign the installer:**

```cmd
signtool sign /f "your-certificate.pfx" /p "password" /tr http://timestamp.digicert.com /td sha256 /fd sha256 "output\AI-Gospel-Parser-Setup-1.0.0.exe"
```

This prevents Windows SmartScreen warnings.

## Testing the Installer

### Test on Clean Windows VM:

1. Create a Windows 10/11 VM (VirtualBox, VMware, or Hyper-V)
2. **Do NOT** install Docker beforehand
3. Run the installer
4. Verify it detects missing Docker and provides download link
5. Install Docker, restart VM
6. Run installer again
7. Verify it completes installation successfully
8. Test launching the application

### Test Uninstall:

1. Use "Add or Remove Programs"
2. Verify Docker containers are stopped
3. Verify files are removed
4. Verify shortcuts are removed

## Troubleshooting

**Error: "Cannot find LICENSE file"**
- Make sure you're in the root directory of the repo
- LICENSE file must exist two levels up (`..\..\LICENSE`)

**Error: "Cannot find icon.ico"**
- Create or download an icon file
- Place in the `installers/windows/` directory
- Or comment out the icon lines in `installer.iss`

**Error: "Docker check failed"**
- This is intentional if Docker isn't installed
- The installer will prompt user to install Docker first

**Installer shows "Unknown Publisher"**
- This is expected for unsigned installers
- Get a code signing certificate to remove this warning

## Distribution

Once built, distribute the installer:

1. **GitHub Releases:**
   ```bash
   gh release create v1.0.0 output/AI-Gospel-Parser-Setup-1.0.0.exe
   ```

2. **Direct Download:**
   - Upload to your website
   - Provide SHA256 checksum for verification:
   ```cmd
   certutil -hashfile output\AI-Gospel-Parser-Setup-1.0.0.exe SHA256
   ```

3. **Update README.md:**
   - Add download link
   - Include installation instructions
   - Note system requirements (Docker Desktop required)

## Support

If users report issues:

1. Check `%TEMP%\Setup Log *.txt` (Inno Setup creates this automatically)
2. Check Docker Desktop is running
3. Check firewall/antivirus isn't blocking
4. Try "Run as Administrator"

## Additional Resources

- Inno Setup Documentation: https://jrsoftware.org/ishelp/
- Inno Setup Examples: `C:\Program Files (x86)\Inno Setup 6\Examples\`
- Icon generators: https://redketchup.io/icon-converter
