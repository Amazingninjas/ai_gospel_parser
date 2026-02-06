# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - Unreleased

### Fixed
- **Windows installer launcher bug**: Fixed launch.bat and stop.bat to run docker-compose from the correct directory (%USERPROFILE%\Documents\ai_gospel_parser) instead of Program Files installation directory
- **Docker Compose warning**: Removed deprecated `version: '3.8'` field from docker-compose.yml

## [1.0.1] - 2026-02-06

### Added
- **Professional Windows installer** (.exe) with Inno Setup
- **Smart launcher scripts** that check Docker status and start only if needed
- **Start Menu shortcuts** for easy access
- **macOS and Linux installers** with native formats (.app, .desktop)
- **Complete installer documentation** covering all platforms

### Fixed
- **PowerShell script syntax** - replaced Unicode symbols with ASCII for compatibility
- **Line endings** - converted to CRLF for Windows batch files

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
