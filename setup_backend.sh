#!/bin/bash
# Quick setup script for AI Gospel Parser backend

set -e  # Exit on error

echo "🚀 Setting up AI Gospel Parser Backend..."

# Create backend directory structure
echo "📁 Creating directory structure..."
mkdir -p backend/{routers,services,models,schemas,data}

# Create __init__.py files for Python packages
touch backend/__init__.py
touch backend/routers/__init__.py
touch backend/services/__init__.py
touch backend/models/__init__.py
touch backend/schemas/__init__.py

# Create main files
echo "📝 Creating main Python files..."

# main.py
cat > backend/main.py << 'EOF'
"""
AI Gospel Parser - FastAPI Backend
===================================
Main application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers (will be created in tasks)
# from routers import verses, lexicon, chat, auth

app = FastAPI(
    title="AI Gospel Parser API",
    description="REST API for Greek New Testament study with AI assistance",
    version="4.0.0"
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "AI Gospel Parser API",
        "version": "4.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_provider": "configured",  # TODO: Check actual status
        "database": "connected"  # TODO: Check actual DB connection
    }

# Mount routers (uncomment as you create them)
# app.include_router(verses.router, prefix="/api/verses", tags=["verses"])
# app.include_router(lexicon.router, prefix="/api/lexicon", tags=["lexicon"])
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
EOF

# config.py
cat > backend/config.py << 'EOF'
"""
Configuration Management
========================
Loads environment variables and application settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    """Application settings from environment variables"""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    BACKEND_ROOT = Path(__file__).parent
    DATA_DIR = BACKEND_ROOT / "data"

    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DATA_DIR}/gospel_parser.db"
    )

    # Security
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "your-secret-key-change-in-production-use-openssl-rand-hex-32"
    )
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_DAYS = 7

    # AI Provider
    AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama").lower()
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mixtral")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

    # Existing resources (reuse from CLI version)
    CHROMA_DB_PATH = str(PROJECT_ROOT / "chroma_db_interlinear")
    SBLGNT_PATH = str(PROJECT_ROOT / "sblgnt")
    LEXICON_PATH = str(PROJECT_ROOT / "strongsgreek.xml")
    WEB_BIBLE_PATH = str(PROJECT_ROOT / "web_bible_json")
    ENHANCED_LEXICON_PATH = str(PROJECT_ROOT / "enhanced_lexicon.json")

    # Reference texts
    THAYERS_ENABLED = os.getenv("ENABLE_THAYERS", "true").lower() == "true"
    MOULTON_MILLIGAN_ENABLED = os.getenv("ENABLE_MOULTON_MILLIGAN", "true").lower() == "true"
    ROBERTSON_GRAMMAR_ENABLED = os.getenv("ENABLE_ROBERTSON_GRAMMAR", "true").lower() == "true"
    JOSEPHUS_ENABLED = os.getenv("ENABLE_JOSEPHUS", "true").lower() == "true"
    ROBERTSON_WORD_PICTURES_ENABLED = os.getenv("ENABLE_ROBERTSON_WORD_PICTURES", "true").lower() == "true"
    VINCENT_WORD_STUDIES_ENABLED = os.getenv("ENABLE_VINCENT_WORD_STUDIES", "true").lower() == "true"

settings = Settings()

# Ensure data directory exists
settings.DATA_DIR.mkdir(exist_ok=True)
EOF

# database.py
cat > backend/database.py << 'EOF'
"""
Database Configuration
======================
SQLAlchemy setup for user accounts and conversation history.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create SQLite engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Dependency to get database session.

    Usage in FastAPI:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    # Import models here to avoid circular imports
    # from models import user, conversation

    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
EOF

# requirements.txt
cat > backend/requirements.txt << 'EOF'
# FastAPI and server
fastapi==0.109.2
uvicorn[standard]==0.27.1
python-multipart==0.0.9

# Database
sqlalchemy==2.0.27
alembic==1.13.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# WebSocket support
websockets==12.0

# Environment variables
python-dotenv==1.0.1

# Existing dependencies (from CLI version)
chromadb>=1.1.1
requests>=2.31.0

# Testing (optional for now)
pytest==8.0.0
pytest-asyncio==0.23.4
httpx==0.26.0
EOF

# Create .env file
echo "🔐 Creating .env file..."
cat > backend/.env << 'EOF'
# Database
DATABASE_URL=sqlite:///./data/gospel_parser.db

# Security (CHANGE THIS IN PRODUCTION!)
JWT_SECRET_KEY=please-change-this-to-a-random-string-use-openssl-rand-hex-32

# AI Provider (ollama or gemini)
AI_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mixtral
GEMINI_API_KEY=

# Reference Texts
ENABLE_THAYERS=true
ENABLE_MOULTON_MILLIGAN=true
ENABLE_ROBERTSON_GRAMMAR=true
ENABLE_JOSEPHUS=true
ENABLE_ROBERTSON_WORD_PICTURES=true
ENABLE_VINCENT_WORD_STUDIES=true
EOF

# Create .gitignore
echo "📝 Creating .gitignore..."
cat > backend/.gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
venv_backend/
ENV/
env/

# Database
*.db
*.sqlite
*.sqlite3
data/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
logs/
EOF

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
cd backend
python3 -m venv venv_backend

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate virtual environment:"
echo "      cd backend && source venv_backend/bin/activate"
echo ""
echo "   2. Install dependencies:"
echo "      pip install -r requirements.txt"
echo ""
echo "   3. Run the server:"
echo "      uvicorn main:app --reload"
echo ""
echo "   4. Visit API docs:"
echo "      http://localhost:8000/docs"
echo ""
echo "🚀 Ready to start Task #2 (Create verse lookup service)!"
