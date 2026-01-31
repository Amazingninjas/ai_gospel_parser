# AI Gospel Parser v1.0.0 - Full Web Application

🎉 **Major Release:** Complete transformation from CLI tool to full-stack web application!

## 🌟 What's New

### Web Application
- **Modern React Frontend** - TypeScript + Vite 7 + TailwindCSS 3.4.1
- **FastAPI Backend** - RESTful API + WebSocket streaming
- **User Authentication** - Secure JWT tokens with bcrypt password hashing
- **Real-time AI Chat** - Streaming responses via WebSocket with Ollama/Gemini
- **Conversation History** - Save and resume conversations in SQLite database

### Features
- ✅ **Verse Lookup** - Search Greek NT (SBLGNT) with English (WEB) translation
- ✅ **Interactive Greek Text** - Click words to see lexicon entries instantly
- ✅ **Strong's Lexicon** - Complete morphology, definitions, and cross-references
- ✅ **AI Biblical Scholar** - Ask questions about Greek words, grammar, and theology
- ✅ **Smart Chat Interface** - Auto-scroll that respects your scroll position
- ✅ **Mobile Responsive** - Tab navigation optimized for small screens
- ✅ **Enhanced Greek Fonts** - Noto Serif and Noto Sans for beautiful Greek typography

### Docker Deployment
- 🐳 **One-Command Setup** - `docker-compose up -d` and you're running
- 🔒 **Isolated Containers** - Backend (FastAPI) and Frontend (Nginx) separation
- 📦 **Multi-stage Builds** - Optimized image sizes
- 🔄 **Health Checks** - Automatic monitoring and recovery
- 💾 **Volume Persistence** - Data and conversations survive restarts

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (with WSL2 on Windows)
- Ollama with mixtral model: `ollama pull mixtral`

### Launch
```bash
# Clone the repository
git clone https://github.com/yourusername/ai_gospel_parser.git
cd ai_gospel_parser

# Start all services
docker-compose up -d

# Open in browser
open http://localhost:3000
```

### Test
```bash
# Run automated tests
./test-docker.sh
```

## 📚 Documentation
- **Quick Start**: [GET_STARTED_WEB_UI.md](GET_STARTED_WEB_UI.md)
- **Full Roadmap**: [WEB_UI_ROADMAP.md](WEB_UI_ROADMAP.md)
- **API Documentation**: http://localhost:8000/docs (when running)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## 🐛 Bug Fixes
- Fixed bcrypt 72-byte password limit with SHA256 pre-hashing
- Fixed ChromaDB tenant connection in Docker containers
- Fixed WEB Bible path resolution for English text
- Fixed Ollama connectivity from Docker using host.docker.internal
- Fixed layout shift from "Saving..." indicator
- Fixed auto-scroll forcing users to bottom while reading history

## 📊 Stats
- **25/25 Tasks Complete** (100%)
- **16 API Endpoints** (15 REST + 1 WebSocket)
- **9 React Components** (Dashboard, Chat, Verse, Lexicon, Auth)
- **5 Custom Hooks** (useAuth, useWebSocket, useVerse, useLexicon, useConversation)
- **13,551 NT Verses** indexed in ChromaDB
- **5,624 Greek Lexicon Entries** with full morphology

## 🙏 Acknowledgments
Built with Claude Sonnet 4.5 for analyzing Greek New Testament text with modern AI technology.

## 📝 License
MIT License - See [LICENSE](LICENSE) for details

---

**Previous Version**: CLI interface (v0.1.0)
