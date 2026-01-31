"""
AI Gospel Parser - FastAPI Backend
===================================
Main application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import database
from database import init_db

# Import routers
from routers import verses, lexicon, chat, auth, conversations

app = FastAPI(
    title="AI Gospel Parser API",
    description="REST API for Greek New Testament study with AI assistance",
    version="4.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup"""
    init_db()

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

# Mount routers
app.include_router(verses.router, prefix="/api/verses", tags=["verses"])
app.include_router(lexicon.router, prefix="/api/lexicon", tags=["lexicon"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
