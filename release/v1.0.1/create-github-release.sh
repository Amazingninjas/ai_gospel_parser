#!/bin/bash
# Create GitHub release with installers

set -e

VERSION="1.0.1"
RELEASE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  Creating GitHub Release v${VERSION}"
echo "============================================"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed"
    echo ""
    echo "Install it from: https://cli.github.com"
    echo ""
    echo "Quick install:"
    echo "  # Ubuntu/Debian"
    echo "  sudo apt install gh"
    echo ""
    echo "  # macOS"
    echo "  brew install gh"
    echo ""
    echo "  # Windows"
    echo "  winget install GitHub.cli"
    echo ""
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub"
    echo ""
    echo "Run: gh auth login"
    echo ""
    exit 1
fi

# Check if we're in a git repo
if ! git rev-parse --git-dir &> /dev/null; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Check if tag exists
if git rev-parse "v${VERSION}" &> /dev/null 2>&1; then
    echo "Warning: Tag v${VERSION} already exists"
    echo ""
    read -p "Delete and recreate? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "v${VERSION}"
        git push origin ":refs/tags/v${VERSION}" 2>/dev/null || true
    else
        echo "Aborting."
        exit 1
    fi
fi

# Create tag
echo "[1/3] Creating git tag..."
git tag -a "v${VERSION}" -m "Release v${VERSION} - Professional One-Click Installers"
git push origin "v${VERSION}"
echo "✓ Tag created and pushed"
echo ""

# Create release
echo "[2/3] Creating GitHub release..."
cd "$RELEASE_DIR"

gh release create "v${VERSION}" \
  --title "AI Gospel Parser v${VERSION} - Professional One-Click Installers" \
  --notes-file RELEASE_NOTES.md \
  AI-Gospel-Parser-Windows-Installer-${VERSION}.tar.gz \
  AI-Gospel-Parser-macOS-Installer-${VERSION}.tar.gz \
  AI-Gospel-Parser-Linux-Installer-${VERSION}.tar.gz \
  SHA256SUMS.txt

echo "✓ Release created with all installer packages"
echo ""

# Get release URL
RELEASE_URL=$(gh release view "v${VERSION}" --json url -q .url)

echo "[3/3] Release published!"
echo ""
echo "============================================"
echo "  Release v${VERSION} Published!"
echo "============================================"
echo ""
echo "Release URL: $RELEASE_URL"
echo ""
echo "Next steps:"
echo "  1. Update README.md download links (if not done)"
echo "  2. Announce on social media"
echo "  3. Post in GitHub Discussions"
echo "  4. Update project website"
echo ""
echo "Congratulations! 🎉"
