#!/bin/bash
# Commit and release v1.0.0

set -e  # Exit on error

echo "=== AI Gospel Parser v1.0.0 Release ==="
echo ""

# 1. Stage all changes
echo "1. Staging all changes..."
git add .
echo "   ✅ Changes staged"

# 2. Show what will be committed
echo ""
echo "2. Files to be committed:"
git status --short
echo ""

# 3. Ask for confirmation
read -p "Proceed with commit? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Aborted."
    exit 1
fi

# 4. Commit
echo ""
echo "3. Creating commit..."
git commit -m "Release v1.0.0: Full-stack web application with Docker deployment

- Complete React + TypeScript frontend with real-time AI chat
- FastAPI backend with authentication and WebSocket support
- Docker deployment with docker-compose
- Smart auto-scroll, conversation history, mobile responsive
- Fixed bcrypt, ChromaDB, Ollama connectivity issues

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
echo "   ✅ Commit created"

# 5. Tag the release
echo ""
echo "4. Creating release tag..."
git tag -a v1.0.0 -m "AI Gospel Parser v1.0.0 - Full Web Application"
echo "   ✅ Tag v1.0.0 created"

# 6. Show git log
echo ""
echo "5. Latest commit:"
git log -1 --oneline
echo ""

# 7. Ask to push
read -p "Push to GitHub? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Commit and tag created locally. Push manually with:"
    echo "  git push origin main"
    echo "  git push origin v1.0.0"
    exit 0
fi

# 8. Push to GitHub
echo ""
echo "6. Pushing to GitHub..."
git push origin main
echo "   ✅ Pushed to main"

echo ""
echo "7. Pushing tag..."
git push origin v1.0.0
echo "   ✅ Pushed tag v1.0.0"

# 9. Create GitHub release (if gh CLI is available)
echo ""
if command -v gh &> /dev/null; then
    read -p "Create GitHub release? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "8. Creating GitHub release..."
        gh release create v1.0.0 \
            --title "v1.0.0 - Full Web Application" \
            --notes-file RELEASE_DESCRIPTION.md
        echo "   ✅ GitHub release created!"
    fi
else
    echo "ℹ️  gh CLI not installed. Create release manually at:"
    echo "   https://github.com/YOUR_USERNAME/ai_gospel_parser/releases/new?tag=v1.0.0"
fi

echo ""
echo "=== 🎉 Release Complete! ==="
echo ""
echo "View your release:"
echo "  https://github.com/YOUR_USERNAME/ai_gospel_parser/releases/tag/v1.0.0"
echo ""
