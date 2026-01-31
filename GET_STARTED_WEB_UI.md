# Get Started: AI Gospel Parser Web UI

**Status:** Ready to build! 🚀
**Timeline:** 8-10 weeks to beta launch
**Current Phase:** Week 1 - Backend Foundation

---

## 🎯 Your 4 Focus Areas

You've committed to tackling these recommendations in order:

1. **Web Interface** (8-10 weeks) - **STARTING NOW**
2. **Grammatical Search** (1-2 weeks) - After web UI MVP
3. **Cross-Reference System** (2-3 weeks) - After grammatical search
4. **Comparative Analysis** (2-3 weeks) - Critical vs Byzantine texts (NEW!)

This document focuses on #1: Web Interface.

---

## 📚 Resources Created

I've set up everything you need to get started:

1. **WEB_UI_ROADMAP.md** - Complete 25-task roadmap with week-by-week breakdown
2. **setup_backend.sh** - Automated script to bootstrap FastAPI backend
3. **Task List** - 25 tasks tracked in your task system

**View all tasks:**
```bash
# List all tasks
claude /tasks
```

---

## ⚡ Quick Start (10 Minutes)

### **Step 1: Run the Setup Script**

```bash
cd /home/justin/ai-projects/ai_gospel_parser
./setup_backend.sh
```

This creates:
- ✅ `backend/` directory with FastAPI structure
- ✅ `backend/main.py` - FastAPI app skeleton
- ✅ `backend/config.py` - Configuration management
- ✅ `backend/database.py` - SQLAlchemy setup
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/.env` - Environment variables
- ✅ `backend/venv_backend/` - Python virtual environment

### **Step 2: Install Dependencies**

```bash
cd backend
source venv_backend/bin/activate
pip install -r requirements.txt
```

This installs:
- FastAPI + Uvicorn (web server)
- SQLAlchemy (database ORM)
- python-jose (JWT authentication)
- passlib (password hashing)
- websockets (for AI streaming)
- ChromaDB (already have, reusing)

### **Step 3: Run the Backend**

```bash
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### **Step 4: Test the API**

Visit in browser:
- **API Documentation:** http://localhost:8000/docs (interactive Swagger UI)
- **Health Check:** http://localhost:8000/api/health
- **Root:** http://localhost:8000/

You should see:
```json
{
  "name": "AI Gospel Parser API",
  "version": "4.0.0",
  "status": "running",
  "docs": "/docs"
}
```

**✅ Task #1 Complete!** Backend skeleton is running.

---

## 🎯 Today's Work: Tasks #2-3 (Verse & Lexicon APIs)

Now that the backend is running, let's add the first real functionality.

### **Task #2: Create Verse Lookup Service**

**Goal:** Make the existing `gospel_parser_interlinear.py` logic available via REST API.

**What you're building:**
- `GET /api/verses/John%203:16` → returns Greek + English verse
- `GET /api/verses/64/3/16` → same, but with numeric book code
- `GET /api/books` → list of all 27 NT books

**Implementation Steps:**

1. **Create verse service** (`backend/services/verse_service.py`):
   - Import existing code: `sys.path.append('..')` to access `gospel_parser_interlinear.py`
   - Wrap `parse_verse_reference()` and `lookup_verse()` functions
   - Initialize ChromaDB client (singleton pattern)
   - Add caching for frequent verses (John 3:16, Romans 3:23, etc.)

2. **Create Pydantic schemas** (`backend/schemas/verse.py`):
   ```python
   from pydantic import BaseModel

   class VerseResponse(BaseModel):
       greek_text: str
       english_text: str
       book: str
       chapter: int
       verse: int
       reference: str  # "John 3:16"
       reference_id: str  # "64-03-16"

   class BookInfo(BaseModel):
       name: str
       code: int
       abbreviations: list[str]
   ```

3. **Create router** (`backend/routers/verses.py`):
   ```python
   from fastapi import APIRouter, HTTPException
   from services.verse_service import VerseService
   from schemas.verse import VerseResponse, BookInfo

   router = APIRouter()
   verse_service = VerseService()

   @router.get("/{reference}", response_model=VerseResponse)
   async def get_verse(reference: str):
       """Lookup verse by reference (e.g., 'John 3:16')"""
       # Parse reference
       # Call verse_service.lookup()
       # Return VerseResponse
       pass

   @router.get("/books", response_model=list[BookInfo])
   async def list_books():
       """Get list of all NT books"""
       pass
   ```

4. **Mount router in main.py**:
   ```python
   from routers import verses
   app.include_router(verses.router, prefix="/api/verses", tags=["verses"])
   ```

5. **Test**:
   ```bash
   curl http://localhost:8000/api/verses/John%203:16
   ```

**Expected Response:**
```json
{
  "greek_text": "Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον...",
  "english_text": "For God so loved the world...",
  "book": "John",
  "chapter": 3,
  "verse": 16,
  "reference": "John 3:16",
  "reference_id": "64-03-16"
}
```

---

### **Task #3: Create Lexicon Lookup Service**

**Goal:** Make lexicon lookups available via REST API.

**What you're building:**
- `GET /api/lexicon/strongs/G25` → ἀγαπάω definition
- `GET /api/lexicon/greek/ἀγαπάω` → same lookup by Greek word
- `GET /api/lexicon/search?q=love` → full-text search

**Implementation Steps:**

1. **Create lexicon service** (`backend/services/lexicon_service.py`):
   - Load `enhanced_lexicon.json` on startup (singleton)
   - Wrap lookups from `lexicon_helper.py` or parse JSON directly
   - Add in-memory cache (LRU cache for 100 most-used entries)

2. **Create schemas** (`backend/schemas/lexicon.py`):
   ```python
   class LexiconEntry(BaseModel):
       strongs: str  # "G25"
       lemma: str  # "ἀγαπάω"
       transliteration: str  # "agapaō"
       part_of_speech: str
       definition: str
       morphology: dict | None
       cross_refs: list[str] | None
   ```

3. **Create router** (`backend/routers/lexicon.py`)

4. **Mount router in main.py**

5. **Test**:
   ```bash
   curl http://localhost:8000/api/lexicon/strongs/G25
   ```

---

## 📅 This Week's Goals (Week 1)

By end of Friday (Feb 7):
- ✅ Task #1: Backend setup (DONE today!)
- ✅ Task #2: Verse lookup API (complete this today or tomorrow)
- ✅ Task #3: Lexicon lookup API (complete by Wed/Thu)
- ✅ Task #4: AI chat WebSocket (complete by Fri)
- 🚧 Task #5-6: Database + Auth (start if time permits, or next week)

**Daily Commitment:** 2-3 hours/day → ~10-15 hours/week

---

## 🔧 Development Workflow

### **Morning Routine (15 min):**
1. Start Ollama (if using local AI):
   ```bash
   ollama serve
   ```

2. Start backend:
   ```bash
   cd backend
   source venv_backend/bin/activate
   uvicorn main:app --reload
   ```

3. Check API health: http://localhost:8000/api/health

4. Review today's task in task list:
   ```bash
   claude /tasks
   ```

### **Coding Session:**
1. Pick next task (in order: #2, #3, #4, etc.)
2. Read task description carefully
3. Create files, write code
4. Test with curl or http://localhost:8000/docs
5. Commit when working:
   ```bash
   git add .
   git commit -m "Complete Task #2: Add verse lookup API"
   ```

### **End of Day (10 min):**
1. Update task status:
   ```bash
   # Mark completed task
   claude "mark task 2 as completed"
   ```

2. Commit and push:
   ```bash
   git push origin main
   ```

3. Note tomorrow's task

---

## 🛠️ Helpful Commands

**Backend:**
```bash
# Start server with auto-reload
uvicorn main:app --reload

# Different port
uvicorn main:app --reload --port 8080

# With logs
uvicorn main:app --reload --log-level debug

# Install new dependency
pip install package-name
pip freeze > requirements.txt
```

**Testing API:**
```bash
# GET request
curl http://localhost:8000/api/verses/John%203:16

# Pretty JSON output
curl http://localhost:8000/api/verses/John%203:16 | jq

# POST request (later, for auth)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret"}'
```

**Git:**
```bash
# Create feature branch
git checkout -b feature/verse-api

# Check status
git status

# Commit
git add .
git commit -m "Add verse lookup with ChromaDB integration"

# Push
git push origin feature/verse-api

# Merge to main (when done)
git checkout main
git merge feature/verse-api
```

---

## 📖 API Documentation

FastAPI auto-generates **interactive API docs**:
- **Swagger UI:** http://localhost:8000/docs (try endpoints in browser!)
- **ReDoc:** http://localhost:8000/redoc (alternative format)

These update automatically as you add endpoints.

---

## 🚨 Troubleshooting

**"Module not found" errors:**
```bash
# Make sure you're in virtual environment
source venv_backend/bin/activate

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall if needed
pip install -r requirements.txt
```

**"Port already in use":**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8080
```

**ChromaDB errors:**
```bash
# Make sure ChromaDB exists from CLI version
ls -la chroma_db_interlinear/

# If missing, run CLI version once to seed it
python gospel_parser_interlinear.py
```

**Ollama not responding:**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve

# Check model is downloaded
ollama list
```

---

## 📚 Learning Resources

**FastAPI:**
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- WebSocket guide: https://fastapi.tiangolo.com/advanced/websockets/
- Dependency injection: https://fastapi.tiangolo.com/tutorial/dependencies/

**SQLAlchemy:**
- ORM tutorial: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- Relationships: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

**Pydantic:**
- Models: https://docs.pydantic.dev/latest/concepts/models/
- Validation: https://docs.pydantic.dev/latest/concepts/validators/

---

## 🎯 Success Checklist (Week 1)

By end of this week, you should have:
- [x] Backend running on http://localhost:8000
- [ ] Verse lookup API working (`GET /api/verses/{reference}`)
- [ ] Lexicon lookup API working (`GET /api/lexicon/strongs/{number}`)
- [ ] WebSocket AI chat (basic streaming)
- [ ] API documentation visible at /docs
- [ ] All code committed to git

**When you complete these 4 tasks, you'll have a working backend API!**

The frontend work starts Week 3, so you have time to perfect the backend first.

---

## 💬 Getting Help

**Stuck on a task?**
1. Check task description for implementation hints
2. Review WEB_UI_ROADMAP.md for architecture details
3. Ask me: "I'm stuck on Task #2, how do I integrate ChromaDB?"

**Want to change approach?**
1. Open discussion: "Should we use PostgreSQL instead of SQLite?"
2. I can update tasks and roadmap

**Need to prioritize differently?**
1. Tell me: "Let's skip auth (Task #6) for now and do AI chat first"
2. I can reorder tasks

---

## 🚀 Let's Start!

**Your immediate action (next 30 minutes):**

1. Run setup script:
   ```bash
   cd /home/justin/ai-projects/ai_gospel_parser
   ./setup_backend.sh
   ```

2. Start backend:
   ```bash
   cd backend
   source venv_backend/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. Visit http://localhost:8000/docs

4. Tell me when you're ready for Task #2!

**LET'S BUILD THIS! 🔥**
