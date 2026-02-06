# Quick Publish Guide - v1.0.1

## 🚀 One Command to Publish

```bash
cd /home/justin/ai-projects/ai_gospel_parser/release/v1.0.1
./create-github-release.sh
```

That's it! The script will handle everything.

---

## 📋 What the Script Does

1. ✅ Creates git tag `v1.0.1`
2. ✅ Pushes tag to GitHub
3. ✅ Creates GitHub release
4. ✅ Uploads Windows installer (3.1 KB)
5. ✅ Uploads macOS installer (2.9 KB)
6. ✅ Uploads Linux installer (3.2 KB)
7. ✅ Uploads SHA256 checksums
8. ✅ Uses `RELEASE_NOTES.md` as description
9. ✅ Gives you the release URL

---

## 📦 Files That Will Be Published

```
✅ AI-Gospel-Parser-Windows-Installer-1.0.1.tar.gz
✅ AI-Gospel-Parser-macOS-Installer-1.0.1.tar.gz
✅ AI-Gospel-Parser-Linux-Installer-1.0.1.tar.gz
✅ SHA256SUMS.txt
```

---

## ✅ Pre-Flight Checklist

Before publishing, make sure:

- [ ] You're in the project root directory
- [ ] Git is clean (no uncommitted changes)
- [ ] You have GitHub CLI installed: `gh --version`
- [ ] You're authenticated: `gh auth status`
- [ ] You have push access to the repository

---

## 🐛 If Something Goes Wrong

### Script fails with "gh: command not found"

Install GitHub CLI:
```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Then authenticate
gh auth login
```

### Tag already exists

The script will ask if you want to delete and recreate. Type `y` to continue.

### Not authenticated with GitHub

Run:
```bash
gh auth login
```

### Permission denied

Make sure script is executable:
```bash
chmod +x create-github-release.sh
```

---

## 🎯 After Publishing

1. **Verify the release:**
   - Go to https://github.com/Amazingninjas/ai_gospel_parser/releases
   - Check that v1.0.1 is there
   - Test download links

2. **Announce:**
   - GitHub Discussions
   - Twitter/X
   - LinkedIn
   - Reddit (r/programming, r/opensource)
   - Your website

3. **Monitor:**
   - Watch for issues
   - Respond to questions
   - Collect feedback

---

## 📝 Manual Publish (If Script Fails)

If the automated script doesn't work, follow these steps:

### Step 1: Create and Push Tag
```bash
cd /home/justin/ai-projects/ai_gospel_parser
git tag -a v1.0.1 -m "Release v1.0.1 - Professional One-Click Installers"
git push origin v1.0.1
```

### Step 2: Create Release via Web

1. Go to: https://github.com/Amazingninjas/ai_gospel_parser/releases/new
2. Select tag: `v1.0.1`
3. Title: `AI Gospel Parser v1.0.1 - Professional One-Click Installers`
4. Description: Copy contents of `RELEASE_NOTES.md`

### Step 3: Upload Files

Drag and drop these files from `release/v1.0.1/`:
- AI-Gospel-Parser-Windows-Installer-1.0.1.tar.gz
- AI-Gospel-Parser-macOS-Installer-1.0.1.tar.gz
- AI-Gospel-Parser-Linux-Installer-1.0.1.tar.gz
- SHA256SUMS.txt

### Step 4: Publish

Click "Publish release"

---

## 🎉 Success!

Once published, users can download and install with just 2 clicks!

---

**Ready? Let's publish!**

```bash
cd /home/justin/ai-projects/ai_gospel_parser/release/v1.0.1
./create-github-release.sh
```

Good luck! 🚀
