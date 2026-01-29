# Creating Releases for AI Gospel Parser

This document explains how to create downloadable releases on GitHub for users.

## GitHub Releases Overview

GitHub Releases allow users to download specific versions of the software without cloning the entire repository. This is ideal for end-users who want a simple download.

## Creating a New Release

### 1. Tag the Current Version

```bash
# Make sure all changes are committed
git add -A
git commit -m "Prepare for release v3.5.0"

# Create an annotated tag
git tag -a v3.5.0 -m "Release v3.5.0 - Clean HTML Commentary Integration"

# Push the tag to GitHub
git push origin v3.5.0
```

### 2. Create Release on GitHub

1. Go to: https://github.com/Amazingninjas/ai_gospel_parser/releases
2. Click **"Draft a new release"**
3. Choose the tag you just created (v3.5.0)
4. Fill in the release details:

**Release Title:** `v3.5.0 - Production Ready with Commentary`

**Description:**
```markdown
## What's New in v3.5.0

### ✨ Major Features
- 10,382+ verses with comprehensive commentary (Robertson + Vincent)
- Clean HTML source integration (28x improvement over OCR)
- Complete New Testament coverage
- Dual AI provider support (Ollama + Gemini)

### 📚 Commentary Coverage
- Robertson's Word Pictures: 5,142 verses (17 NT books)
- Vincent's Word Studies: 5,240 verses (all 27 NT books)
- Thayer's Greek Lexicon: 5,624 Strong's entries
- Moulton-Milligan Vocabulary: 5,311 papyri examples

### 🚀 Installation
Download the installer for your platform and run it. The installer will:
- Check system requirements
- Install dependencies
- Download English Bible reference
- Set up AI provider (Ollama or Gemini)

### 📋 System Requirements
- Python 3.8+
- 4 GB RAM (Gemini API) or 16 GB RAM (Local Ollama)
- 2-20 GB disk space

### 📖 Documentation
- [Getting Started Guide](https://github.com/Amazingninjas/ai_gospel_parser/blob/main/GETTING_STARTED.txt)
- [Quick Start](https://github.com/Amazingninjas/ai_gospel_parser/blob/main/QUICK_START.md)

### 🐛 Bug Fixes
- None (initial clean release)

### 🙏 Acknowledgments
Data sources: SBLGNT, World English Bible, CCEL, StudyLight.org
```

5. **Attach Release Assets:**
   - Click "Attach binaries by dropping them here"
   - Upload pre-packaged installers (optional)
   - Or include instructions to clone the repo

### 3. Pre-package for Users (Optional)

Create a source distribution that users can download:

```bash
# Create a clean source package (excludes dev files)
git archive --format=zip --prefix=ai_gospel_parser-v3.5.0/ v3.5.0 -o ai_gospel_parser-v3.5.0-source.zip

# Create a tarball (for Linux/macOS users)
git archive --format=tar.gz --prefix=ai_gospel_parser-v3.5.0/ v3.5.0 -o ai_gospel_parser-v3.5.0-source.tar.gz
```

Upload these to the GitHub release.

### 4. Publish the Release

- Check "Set as the latest release"
- Click "Publish release"

## Release Checklist

Before creating a release:

- [ ] All code changes committed and pushed
- [ ] Tests passing (if applicable)
- [ ] Documentation updated (README, GETTING_STARTED.txt)
- [ ] Version number updated in code (if applicable)
- [ ] CHANGELOG or release notes prepared
- [ ] Security audit completed (.env not committed, no API keys)
- [ ] Large files excluded (.gitignore configured)
- [ ] Tag created with semantic version (vMAJOR.MINOR.PATCH)

## Versioning Scheme

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** (v4.0.0): Breaking changes, major features
- **MINOR** (v3.6.0): New features, backward compatible
- **PATCH** (v3.5.1): Bug fixes, backward compatible

**Current Version:** v3.5.0

**Next Versions:**
- v3.5.1 - Bug fixes only
- v3.6.0 - Hebrew OT integration (new feature)
- v4.0.0 - Paid tier launch (major change)

## Download Instructions for Users

Add this to README.md:

```markdown
### Download Latest Release

**Option 1: GitHub Release (Recommended)**
1. Go to [Releases](https://github.com/Amazingninjas/ai_gospel_parser/releases)
2. Download the latest version
3. Extract the archive
4. Run `python install.py`

**Option 2: Git Clone**
```bash
git clone https://github.com/Amazingninjas/ai_gospel_parser.git
cd ai_gospel_parser
python install.py
```
```

## Hotfix Releases

For critical bugs:

```bash
# Create hotfix branch from tag
git checkout -b hotfix-v3.5.1 v3.5.0

# Fix the bug
git commit -m "Fix critical bug in lexicon lookup"

# Tag the hotfix
git tag -a v3.5.1 -m "Hotfix: Fix lexicon lookup bug"

# Push hotfix
git push origin hotfix-v3.5.1
git push origin v3.5.1

# Create GitHub release for v3.5.1
```

## Release Automation (Future)

Consider GitHub Actions for automated releases:

```yaml
# .github/workflows/release.yml
name: Create Release
on:
  push:
    tags:
      - 'v*'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
```

---

**Last Updated:** January 29, 2026
