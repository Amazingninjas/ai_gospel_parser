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

    # Email settings for password reset
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")
    
    # Frontend URL
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Existing resources (reuse from CLI version)
    # In Docker: mounted to /project (entire project root)
    # In local dev: in project root (PROJECT_ROOT)
    # Check for /project first (Docker), fall back to PROJECT_ROOT (local dev)
    DOCKER_PROJECT_ROOT = Path("/project")
    _project_base = DOCKER_PROJECT_ROOT if DOCKER_PROJECT_ROOT.exists() else PROJECT_ROOT

    CHROMA_DB_PATH = str(_project_base / "chroma_db_interlinear")
    SBLGNT_PATH = str(_project_base / "sblgnt")
    LEXICON_PATH = str(_project_base / "strongsgreek.xml")
    WEB_BIBLE_PATH = str(_project_base / "web_bible_json")
    ENHANCED_LEXICON_PATH = str(_project_base / "enhanced_lexicon.json")

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
