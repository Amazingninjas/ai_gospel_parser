# AI Gospel Parser

> A modern web application for studying the Greek New Testament with AI assistance

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Amazingninjas/ai_gospel_parser/releases)

**📹 [Watch Demo Video](#demo-video)** | **🚀 [Quick Start](#-quick-start-docker---recommended)** | **📖 [Documentation](#-documentation)**

## 📸 Screenshots

![Dashboard](https://via.placeholder.com/800x450?text=AI+Gospel+Parser+Dashboard)
*Interactive dashboard with verse lookup, lexicon, and AI chat*

![Greek Text Analysis](https://via.placeholder.com/800x450?text=Click+Greek+Words+for+Instant+Definitions)
*Click any Greek word to see Strong's lexicon entries with morphology*

## ✨ Features

- 🔍 **Verse Lookup** - Search all **13,551 Greek NT verses** (SBLGNT) with English translation (WEB)
- 📖 **Greek Lexicon** - Click any Greek word for instant definitions with **5,624 Strong's entries**
- 🤖 **AI Chat** - Real-time streaming responses with Ollama (local) or Gemini (cloud)
- 💬 **Conversation History** - Auto-saved chat history with SQLite persistence
- 📱 **Mobile Responsive** - Tab navigation optimized for phones, tablets, and desktops
- 🔐 **User Authentication** - Secure JWT-based login with bcrypt password hashing
- 🎨 **Enhanced Greek Fonts** - Beautiful typography with Noto Serif and Noto Sans
- 🐳 **Docker Ready** - One-command deployment with multi-stage builds

## 🚀 Quick Start (Docker - Recommended)

The fastest way to get started:

```bash
# 1. Clone the repository
git clone https://github.com/Amazingninjas/ai_gospel_parser.git
cd ai_gospel_parser

# 2. Configure environment
cp .env.docker .env
# Edit .env and set JWT_SECRET_KEY (see Configuration below)

# 3. Start Ollama (for local AI)
ollama serve
ollama pull mixtral

# 4. Start the application
docker-compose up -d

# 5. Open your browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

**That's it!** Register an account and start studying.

## 📋 Prerequisites

### Option 1: Docker (Easiest)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) or Docker Engine
- [Ollama](https://ollama.ai) (for local AI) **or** Gemini API key

### Option 2: Manual Installation
- Python 3.12 or higher
- Node.js 20.19 or higher
- Ollama (for local AI) **or** Gemini API key

## 🛠️ Installation

### Docker Installation (Recommended)

1. **Install Prerequisites**
   ```bash
   # Install Docker Desktop
   # Download from: https://www.docker.com/products/docker-desktop

   # Install Ollama
   # Download from: https://ollama.ai
   ```

2. **Clone and Configure**
   ```bash
   git clone https://github.com/Amazingninjas/ai_gospel_parser.git
   cd ai_gospel_parser

   # Copy environment file
   cp .env.docker .env

   # Generate a secure JWT secret key
   openssl rand -hex 32
   # Copy the output and set it as JWT_SECRET_KEY in .env
   ```

3. **Start Ollama**
   ```bash
   ollama serve
   ollama pull mixtral
   ```

4. **Launch Application**
   ```bash
   docker-compose up -d

   # View logs
   docker-compose logs -f

   # Check status
   docker-compose ps
   ```

5. **Access Application**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

### Manual Installation

See [QUICK_START.md](QUICK_START.md) for detailed manual installation instructions.

## ⚙️ Configuration

### Environment Variables

Edit `.env` file:

```env
# REQUIRED: Change this to a random secret key!
JWT_SECRET_KEY=your-random-secret-key-here

# AI Provider: "ollama" (local) or "gemini" (cloud)
AI_PROVIDER=ollama

# For local AI (Ollama)
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=mixtral

# For cloud AI (Gemini) - optional alternative
# AI_PROVIDER=gemini
# GEMINI_API_KEY=your-api-key-here
```

**⚠️ Security:** Always set a unique `JWT_SECRET_KEY` in production!

## 📖 Usage

1. **Register:** Create an account at http://localhost:3000
2. **Search:** Enter a verse reference like "John 3:16"
3. **Explore:** Click Greek words to see definitions
4. **Ask:** Chat with AI about the text

See [USER_GUIDE.md](USER_GUIDE.md) for complete usage instructions.

## 🏗️ Architecture

```
Frontend (React)  →  Backend (FastAPI)  →  AI (Ollama/Gemini)
     ↓                      ↓
  Port 3000            Port 8000
                           ↓
                   SQLite + ChromaDB
```

## 📁 Project Structure

```
ai_gospel_parser/
├── backend/                 # FastAPI backend
│   ├── main.py             # Entry point
│   ├── models/             # Database models
│   ├── routers/            # API endpoints (16 total)
│   ├── services/           # Business logic
│   └── tests/              # 21 integration tests
├── frontend/               # React frontend
│   └── src/
│       ├── components/     # UI components
│       ├── hooks/          # Custom React hooks
│       └── pages/          # Page components
└── docker-compose.yml      # Docker orchestration
```

## 🧪 Testing

```bash
# Backend tests (21 integration tests)
cd backend
pytest -v

# Frontend build test
cd frontend
npm run build
```

## 📊 API Documentation

Interactive API docs: http://localhost:8000/docs

**Key Endpoints:**
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login
- `GET /api/verses/{reference}` - Lookup verse
- `GET /api/lexicon/strongs/{number}` - Lexicon entry
- `WS /api/chat/stream` - AI chat
- `GET /api/conversations` - Chat history

## 🚢 Deployment

### Production Deployment

```bash
# On production server
git clone https://github.com/Amazingninjas/ai_gospel_parser.git
cd ai_gospel_parser

# Configure
cp .env.docker .env
nano .env  # Set JWT_SECRET_KEY and configure

# Deploy
docker-compose up -d
```

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for complete guide.

## 📚 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user guide
- **[QUICK_START.md](QUICK_START.md)** - Quick reference
- **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** - Deployment guide
- **[PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md)** - Performance tips
- **[MONITORING_GUIDE.md](MONITORING_GUIDE.md)** - Monitoring setup

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- SBLGNT - Greek New Testament text
- Strong's Concordance - Lexicon data
- World English Bible - English reference
- Ollama - Local LLM inference
- FastAPI & React - Framework technologies

## 💡 FAQ

**Q: Do I need Ollama?**
A: You can use Ollama (local, free) or Gemini (cloud, API key required).

**Q: How much RAM is needed?**
A: Minimum 4GB, recommended 8GB+ for Ollama.

**Q: Can I use this offline?**
A: Yes with Ollama! Everything runs locally.

**Q: Is it free?**
A: Yes! Ollama is free. Gemini has costs (~$0.01-0.05 per conversation).

## 📹 Demo Video

**Watch the full demo:** [AI Gospel Parser Demo](https://youtu.be/YOUR_VIDEO_ID)

*Coming soon! Video walkthrough showing verse lookup, lexicon, and AI chat features.*

## 📊 Project Stats

- **13,551** Greek NT verses (SBLGNT)
- **5,624** Strong's lexicon entries
- **16** API endpoints (15 REST + 1 WebSocket)
- **21** integration tests
- **9** React components
- **5** custom React hooks

## 📞 Support

- **Documentation:** See `docs/` folder
- **Issues:** [GitHub Issues](https://github.com/Amazingninjas/ai_gospel_parser/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Amazingninjas/ai_gospel_parser/discussions)

---

**Built with ❤️ for Greek New Testament study**
*Developed with Claude Sonnet 4.5*
