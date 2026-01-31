# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-31

### Added
- **Full-stack web application** with React frontend and FastAPI backend
- **Docker deployment** with docker-compose orchestration
- **User authentication** with JWT tokens and bcrypt password hashing
- **Real-time AI chat** with WebSocket streaming (Ollama/Gemini)
- **Verse lookup** with Greek (SBLGNT) and English (WEB) text
- **Lexicon panel** with Strong's numbers and morphology
- **Conversation history** with SQLite persistence
- **Mobile-responsive design** with tab navigation
- **Smart auto-scroll** in chat that respects user scroll position
- **Protected routes** with authentication guards
- **Enhanced Greek font support** (Noto Serif, Noto Sans)

### Fixed
- bcrypt password length handling (72-byte limit with SHA256 pre-hashing)
- ChromaDB mount permissions in Docker
- WEB Bible path resolution in containers
- Ollama host connectivity from Docker (host.docker.internal)
- Layout shift from "Saving..." indicator
- Auto-scroll forcing users to bottom while reading

### Technical
- React 18 + TypeScript + Vite 7
- FastAPI + SQLAlchemy + ChromaDB
- TailwindCSS 3.4.1 for styling
- Docker multi-stage builds
- Nginx for production frontend serving
- Custom React hooks (useAuth, useWebSocket, useVerse, useLexicon)

## [0.1.0] - Previous CLI Version
- Command-line interface for verse analysis
- Greek text parsing with SBLGNT
- Strong's lexicon integration
- AI chat with Ollama
