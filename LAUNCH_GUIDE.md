# 🚀 Launch Guide - AI Gospel Parser

Follow these steps to test and deploy your AI Gospel Parser for public sharing.

## Step 1: Test Docker Setup Locally (15 minutes)

### 1.1 Ensure Ollama is Running

```bash
# Start Ollama
ollama serve

# In another terminal, pull the model
ollama pull mixtral

# Verify it's working
ollama list
```

You should see `mixtral` in the list.

### 1.2 Configure Environment

```bash
cd /home/justin/ai-projects/ai_gospel_parser

# Copy environment template
cp .env.docker .env

# Generate a secure JWT secret
openssl rand -hex 32

# Edit .env and paste the secret as JWT_SECRET_KEY
nano .env
```

Make sure your `.env` looks like this:
```env
JWT_SECRET_KEY=<paste-your-generated-secret-here>
AI_PROVIDER=ollama
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=mixtral
```

### 1.3 Run the Launch Test

```bash
# Make sure you're in the project directory
cd /home/justin/ai-projects/ai_gospel_parser

# Run the test script
./test-launch.sh
```

**Expected output:**
- ✅ Backend health check shows "healthy"
- ✅ Frontend is responding
- ✅ All containers are running

### 1.4 Manual Testing

Open your browser and test everything:

1. **Open** http://localhost:3000

2. **Register** a new account
   - Email: test@example.com
   - Password: TestPassword123

3. **Search** for a verse
   - Enter: "John 3:16"
   - Click "Search"
   - ✅ Verify Greek and English text appears

4. **Test Lexicon**
   - Click any Greek word
   - ✅ Verify lexicon entry appears in right panel

5. **Test AI Chat**
   - Type: "What does agape mean in this verse?"
   - Click "Send"
   - ✅ Verify AI response streams in

6. **Test Mobile**
   - Resize browser to mobile size (or open on phone)
   - ✅ Verify tabs appear (Verse/Chat/Lexicon)
   - ✅ Verify tabs switch correctly

7. **Test Conversation History**
   - Click "📚 History" in chat panel
   - ✅ Verify your conversation appears
   - Send another message
   - ✅ Verify it saves

### 1.5 Check Logs

```bash
# View all logs
docker-compose logs

# Check for errors
docker-compose logs | grep -i error

# Follow logs in real-time
docker-compose logs -f
```

**✅ All tests passed?** Continue to Step 2.

**❌ Issues?** Check [PRE_LAUNCH_CHECKLIST.md](PRE_LAUNCH_CHECKLIST.md) troubleshooting section.

## Step 2: Prepare GitHub Repository (10 minutes)

### 2.1 Review What Will Be Committed

```bash
cd /home/justin/ai-projects/ai_gospel_parser

# See what's changed
git status

# See what's new
git add --dry-run .

# Review large files (should be none > 10MB)
find . -type f -size +10M -not -path "*/node_modules/*" -not -path "*/.git/*"
```

### 2.2 Check for Sensitive Data

```bash
# Check for API keys or secrets (should find NONE)
grep -r "sk-" --exclude-dir=node_modules --exclude-dir=.git --exclude="*.md" | grep -v ".env.docker"
grep -r "password.*=" --exclude-dir=node_modules --exclude-dir=.git --exclude="*.md" | grep -v ".env.docker"

# Verify .env is NOT being committed
git status | grep ".env$"
# Should show nothing (or ".env" in "Untracked files" section)
```

**⚠️ CRITICAL:** If you see actual secrets, DO NOT COMMIT. Remove them first.

### 2.3 Update README with Your Info

```bash
nano README.md
```

Find and replace these placeholders:
- `yourusername` → your actual GitHub username
- Add your repository URL
- Add any personal info you want

Save and exit (Ctrl+X, Y, Enter)

## Step 3: Commit and Push to GitHub (5 minutes)

### 3.1 Stage All Changes

```bash
cd /home/justin/ai-projects/ai_gospel_parser

# Stage everything
git add .

# Review what will be committed
git status

# Check the diff
git diff --cached --stat
```

### 3.2 Commit Changes

```bash
# Create commit for web UI release
git commit -m "Release v1.0.0: Complete web UI with Docker deployment

Features:
- Full-stack web application (FastAPI + React)
- User authentication with JWT
- Real-time AI chat with streaming responses
- Comprehensive Greek lexicon integration
- Mobile-responsive design
- Docker deployment ready
- 21 integration tests
- Complete documentation

See README.md for installation and usage instructions."
```

### 3.3 Create Release Tag

```bash
# Tag this version
git tag -a v1.0.0 -m "Version 1.0.0 - Initial public release with web UI"

# Verify tag
git tag -l
```

### 3.4 Push to GitHub

```bash
# Push changes
git push origin main

# Push tag
git push origin v1.0.0
```

## Step 4: Create GitHub Release (5 minutes)

### 4.1 Go to GitHub

1. Navigate to https://github.com/yourusername/ai_gospel_parser
2. Click "Releases" (right sidebar)
3. Click "Create a new release"

### 4.2 Fill Release Information

**Tag:** v1.0.0 (should be in dropdown)

**Title:** AI Gospel Parser v1.0.0 - Web UI Release

**Description:**
```markdown
# 🎉 AI Gospel Parser v1.0.0

The AI Gospel Parser is now available as a complete web application!

## ✨ What's New

- **Full Web Interface** - Modern React frontend with mobile support
- **User Authentication** - Secure JWT-based login
- **Real-time AI Chat** - Streaming responses with verse context
- **Greek Lexicon** - Click any Greek word for instant definitions
- **Conversation History** - Auto-saved chat sessions
- **Docker Deployment** - One-command setup
- **Comprehensive Documentation** - Complete user and deployment guides

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/ai_gospel_parser.git
cd ai_gospel_parser
cp .env.docker .env
# Edit .env and set JWT_SECRET_KEY
docker-compose up -d
```

Open http://localhost:3000 and start studying!

## 📖 Documentation

- [User Guide](USER_GUIDE.md) - How to use the application
- [Quick Start](QUICK_START.md) - Installation instructions
- [Docker Deployment](DOCKER_DEPLOYMENT.md) - Production deployment

## 🙏 Acknowledgments

Special thanks to all contributors and the open-source community!

## 📊 Stats

- 16 API endpoints
- 21 integration tests
- 25/25 roadmap tasks complete
- Mobile-responsive design
- Full Docker support

---

**First time using AI Gospel Parser?** See the [User Guide](USER_GUIDE.md)!
```

**Click:** "Publish release"

## Step 5: Make Repository Public (if not already)

### 5.1 Check Repository Visibility

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Scroll to "Danger Zone"
4. Check if it says "Change repository visibility"

### 5.2 Make Public (if private)

1. Click "Change visibility"
2. Select "Make public"
3. Type repository name to confirm
4. Click "I understand, make this repository public"

**⚠️ WARNING:** Once public, anyone can see your code. Make sure no secrets are committed!

## Step 6: Share with the World! (Ongoing)

### 6.1 Announcement Options

- Share GitHub link on social media
- Post in relevant communities:
  - Biblical Greek forums
  - Seminary student groups
  - Bible study communities
  - AI/tech communities
  - Reddit: r/AncientGreek, r/Christianity, r/selfhosted

### 6.2 Sample Announcement

```
🎉 Excited to share AI Gospel Parser v1.0!

A free, open-source web app for studying the Greek New Testament with AI assistance.

✨ Features:
• Search all 27 NT books in original Greek
• Click any Greek word for instant lexicon definitions
• Ask AI questions about grammar, theology, and meanings
• Auto-saved conversation history
• Mobile-responsive design
• One-command Docker deployment

Perfect for seminary students, pastors, and anyone interested in Biblical Greek!

🔗 https://github.com/yourusername/ai_gospel_parser
📖 Free & open source (MIT license)

#BiblicalGreek #BibleStudy #OpenSource #AI
```

### 6.3 Monitoring After Launch

**First 24 Hours:**
- Check GitHub Issues every few hours
- Respond to questions promptly
- Fix critical bugs quickly
- Monitor server resources (if deployed publicly)

**First Week:**
- Update FAQ based on common questions
- Address bug reports
- Thank early users and contributors
- Consider adding requested features to roadmap

## Step 7: Optional - Deploy to Public Server

If you want others to use it without installing:

### Option 1: DigitalOcean/AWS/etc.

1. Create a droplet/instance (4GB+ RAM recommended)
2. Install Docker
3. Clone your repository
4. Configure `.env`
5. Run `docker-compose up -d`
6. Point domain to server IP
7. Set up SSL with Let's Encrypt

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for details.

### Option 2: Fly.io (Free tier available)

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
flyctl launch
```

## 🎊 Congratulations!

Your AI Gospel Parser is now live and ready for the world to use!

## 📊 Success Metrics

Track these to measure success:
- ⭐ GitHub stars
- 🐛 Issues opened (and resolved!)
- 👥 Successful installations
- 💬 Community engagement
- 🔄 Pull requests

## 🆘 Need Help?

- **Technical Issues:** [GitHub Issues](https://github.com/yourusername/ai_gospel_parser/issues)
- **Questions:** [GitHub Discussions](https://github.com/yourusername/ai_gospel_parser/discussions)
- **Documentation:** See docs/ folder

---

**You've got this! 🚀**
