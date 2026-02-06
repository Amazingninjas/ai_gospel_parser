# Creating Icons for AI Gospel Parser Installers

This guide shows how to create or convert icons for all three platforms.

## 📐 Icon Requirements

| Platform | Format | Sizes Needed | File Name |
|----------|--------|--------------|-----------|
| **Windows** | ICO | 16, 32, 48, 64, 128, 256 | `icon.ico` |
| **macOS** | ICNS | 16-1024 (multiple) | `AppIcon.icns` |
| **Linux** | PNG | 256x256 | `icon.png` |

## 🎨 Design Guidelines

### Recommended Icon Design:
- **Theme:** Greek text, book, or cross symbol
- **Colors:** Blue/Gold (traditional biblical scholarship colors)
- **Style:** Simple, recognizable at small sizes
- **Background:** Transparent or solid color

### Simple Concept:
```
┌─────────────┐
│  📖  AI     │  Greek letters (α β γ) with a book
│  α β        │  Simple, clean, professional
│  Gospel     │
└─────────────┘
```

---

## Method 1: Using Online Converters (Easiest)

### Step 1: Create a Source Image (1024x1024 PNG)

**Option A: Use Canva (Free)**
1. Go to https://www.canva.com
2. Create custom size: 1024x1024 pixels
3. Design your icon:
   - Add Greek letters (α, β, γ, Ω)
   - Add book or scroll icon
   - Add text "AI Gospel Parser" (small)
4. Download as PNG with transparent background

**Option B: Use GIMP (Free, Open Source)**
1. Download GIMP: https://www.gimp.org
2. File → New → 1024x1024 pixels
3. Design your icon
4. File → Export As → icon-source.png

**Option C: Use Figma (Free)**
1. Go to https://www.figma.com
2. Create 1024x1024 frame
3. Design icon
4. Export as PNG

### Step 2: Convert to All Formats

**For Windows (.ico):**
- Go to: https://convertio.co/png-ico/
- Upload your 1024x1024 PNG
- Select multi-size ICO output
- Download as `icon.ico`
- Place in `installers/windows/icon.ico`

**For macOS (.icns):**
- Go to: https://cloudconvert.com/png-to-icns
- Upload your 1024x1024 PNG
- Download as `AppIcon.icns`
- Place in `installers/macos/AppIcon.icns`

**For Linux (.png):**
- Resize your image to 256x256
- Save as `icon.png`
- Place in `installers/linux/icon.png`

---

## Method 2: Using Command Line Tools

### Prerequisites

**Install ImageMagick:**
```bash
# Ubuntu/Debian
sudo apt install imagemagick

# macOS
brew install imagemagick

# Windows
choco install imagemagick
```

### Create All Icons from One Source

```bash
cd installers/icons

# Assuming you have icon-source.png (1024x1024)

# Create Windows ICO (multi-size)
convert icon-source.png \
  -define icon:auto-resize=256,128,64,48,32,16 \
  ../windows/icon.ico

# Create macOS ICNS
# First create iconset directory
mkdir AppIcon.iconset

# Generate all required sizes
convert icon-source.png -resize 16x16     AppIcon.iconset/icon_16x16.png
convert icon-source.png -resize 32x32     AppIcon.iconset/icon_16x16@2x.png
convert icon-source.png -resize 32x32     AppIcon.iconset/icon_32x32.png
convert icon-source.png -resize 64x64     AppIcon.iconset/icon_32x32@2x.png
convert icon-source.png -resize 128x128   AppIcon.iconset/icon_128x128.png
convert icon-source.png -resize 256x256   AppIcon.iconset/icon_128x128@2x.png
convert icon-source.png -resize 256x256   AppIcon.iconset/icon_256x256.png
convert icon-source.png -resize 512x512   AppIcon.iconset/icon_256x256@2x.png
convert icon-source.png -resize 512x512   AppIcon.iconset/icon_512x512.png
convert icon-source.png -resize 1024x1024 AppIcon.iconset/icon_512x512@2x.png

# Convert to ICNS (macOS only)
iconutil -c icns AppIcon.iconset -o ../macos/AppIcon.icns

# Create Linux PNG
convert icon-source.png -resize 256x256 ../linux/icon.png

echo "All icons created!"
```

---

## Method 3: Using Existing Icons

### Find Free Icons

**Sources for Free Icons:**
1. **Flaticon** - https://www.flaticon.com
   - Search: "book", "bible", "scroll", "greek"
   - License: Free with attribution

2. **Icons8** - https://icons8.com
   - Search: "book", "education", "bible"
   - Free tier available

3. **Font Awesome** - https://fontawesome.com
   - Many free icons available
   - Can be exported as PNG

4. **The Noun Project** - https://thenounproject.com
   - Search: "bible", "book", "scroll"
   - Free with attribution

### Example: Using Font Awesome

```bash
# Download Font Awesome (free version)
# Use their icon library to export a book/bible icon
# Export as 1024x1024 PNG
# Follow conversion steps above
```

---

## Method 4: Simple Text-Based Icon (Quick & Easy)

If you need something immediately, create a simple text-based icon:

```bash
cd installers/icons

# Create simple colored icon with ImageMagick
convert -size 256x256 xc:#3B82F6 \
  -gravity center \
  -pointsize 72 \
  -fill white \
  -font Helvetica-Bold \
  -annotate +0-20 "AI" \
  -pointsize 48 \
  -annotate +0+30 "Gospel" \
  icon-simple.png

# Convert to all formats
convert icon-simple.png -define icon:auto-resize=256,128,64,48,32,16 ../windows/icon.ico
convert icon-simple.png -resize 256x256 ../linux/icon.png
```

For macOS ICNS, use the online converter or follow the iconset steps above.

---

## Quick Template: SVG Icon (Scalable)

Save this as `icon-template.svg`:

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="256" height="256" rx="32" fill="#3B82F6"/>

  <!-- Book shape -->
  <rect x="64" y="64" width="128" height="144" rx="8" fill="white"/>
  <rect x="64" y="64" width="16" height="144" fill="#1E40AF"/>

  <!-- Greek letters -->
  <text x="128" y="140" font-family="Arial, sans-serif" font-size="48"
        text-anchor="middle" fill="#1E40AF" font-weight="bold">
    αβ
  </text>

  <!-- AI label -->
  <text x="128" y="240" font-family="Arial, sans-serif" font-size="24"
        text-anchor="middle" fill="white" font-weight="bold">
    AI Gospel
  </text>
</svg>
```

Convert SVG to PNG:
```bash
# Using Inkscape
inkscape icon-template.svg --export-filename=icon-source.png --export-width=1024

# Using ImageMagick
convert -density 300 -background none icon-template.svg -resize 1024x1024 icon-source.png
```

---

## Installation After Creating Icons

### Windows
```bash
cp icon.ico installers/windows/
```
The Inno Setup script will automatically use it.

### macOS
```bash
cp AppIcon.icns "installers/macos/AI Gospel Parser Installer.app/Contents/Resources/"
```
The Info.plist already references it.

### Linux
```bash
cp icon.png installers/linux/
```
The AppImage build script will automatically embed it.

---

## Verification

### Check Windows ICO
```bash
file installers/windows/icon.ico
# Should show: MS Windows icon resource - 6 images
```

### Check macOS ICNS
```bash
file installers/macos/AppIcon.icns
# Should show: Mac OS X icon
```

### Check Linux PNG
```bash
identify installers/linux/icon.png
# Should show: PNG 256x256
```

---

## Professional Icon Design Services

If you want a professional icon:

1. **Fiverr** - $5-50 for icon design
2. **99designs** - Icon design contests
3. **DesignCrowd** - Crowdsource icon designs
4. **Upwork** - Hire a designer

---

## Quick Start (Recommended)

**If you need icons NOW:**

1. Go to https://www.canva.com
2. Create 1024x1024 design
3. Add Greek letters (Α Β Ω) and book emoji 📖
4. Download as PNG
5. Go to https://convertio.co/png-ico/ → Convert to ICO
6. Go to https://cloudconvert.com/png-to-icns → Convert to ICNS
7. Resize to 256x256 for PNG
8. Copy files to installer directories
9. Rebuild installers

**Total time:** 10-15 minutes

---

## Need Help?

- **ImageMagick Docs:** https://imagemagick.org/
- **Inkscape Docs:** https://inkscape.org/doc/
- **Icon Design Tutorial:** https://www.designcontest.com/blog/how-to-design-an-icon/

---

## Placeholder Until Real Icons

For testing, the installers will work without icons:
- Windows: Shows default application icon
- macOS: Shows generic document icon
- Linux: Uses system default icon

But adding custom icons makes it look much more professional!
