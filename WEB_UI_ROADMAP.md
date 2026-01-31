# AI Gospel Parser - Web UI Implementation Roadmap

**Goal:** Transform CLI tool into modern web application with React frontend + FastAPI backend

**Timeline:** 8-10 weeks
**Start Date:** 2026-01-30
**Target Launch:** April 2026 (Beta)

---

## 📊 Task Overview

**Total Tasks:** 25
- Backend Foundation: 6 tasks (Weeks 1-2)
- Frontend Core: 6 tasks (Weeks 3-5)
- Integration & Pages: 6 tasks (Weeks 5-7)
- Polish & Deploy: 7 tasks (Weeks 7-10)

---

## 🗓️ Week-by-Week Breakdown

### **Week 1-2: Backend Foundation** ✓ Tasks 1-6

**Goal:** Create FastAPI backend that wraps existing Python code

**Tasks:**
1. ✅ Set up FastAPI project structure
2. ✅ Create verse lookup service and API endpoints
3. ✅ Create lexicon lookup service and API endpoints
4. ✅ Create AI chat service with WebSocket streaming
5. ✅ Set up SQLite database with user and conversation models
6. ✅ Implement authentication with JWT tokens

**Deliverable:** Working REST API + WebSocket for AI chat
- `http://localhost:8000/api/verses/John%203:16` → returns verse data
- `http://localhost:8000/api/lexicon/strongs/G25` → returns lexicon entry
- `ws://localhost:8000/api/chat/stream` → streams AI responses
- `POST /api/auth/login` → returns JWT token

**Key Files to Create:**
```
backend/
├── main.py                 # FastAPI app entry
├── config.py              # Environment variables
├── database.py            # SQLite setup
├── routers/
│   ├── verses.py          # Verse endpoints
│   ├── lexicon.py         # Lexicon endpoints
│   ├── chat.py            # WebSocket chat
│   └── auth.py            # Authentication
├── services/
│   ├── verse_service.py   # Wraps gospel_parser
│   ├── lexicon_service.py # Wraps lexicon_helper
│   ├── ai_service.py      # Wraps ai_providers
│   └── auth_service.py    # JWT & password hashing
├── models/
│   ├── user.py            # User model
│   └── conversation.py    # Chat history
└── requirements.txt       # Dependencies
```

**Tech Stack:**
- FastAPI 0.109+
- SQLAlchemy 2.0 (ORM)
- python-jose (JWT)
- passlib + bcrypt (password hashing)
- uvicorn (ASGI server)
- websockets (for streaming)

---

### **Week 3-5: Frontend Core** ✓ Tasks 7-12

**Goal:** Build React components and API integration

**Tasks:**
7. ✅ Set up React frontend with Vite and TypeScript
8. ✅ Create TypeScript interfaces and API client
9. ✅ Build VerseDisplay component with Greek and English text
10. ✅ Build ChatInterface component with streaming support
11. ✅ Build LexiconPanel component for Strong's definitions
12. ✅ Build VerseSearch component with autocomplete

**Deliverable:** Functional UI components (not yet fully integrated)
- Verse lookup works (search → display)
- AI chat works (type question → stream response)
- Lexicon panel works (click word → show definition)

**Key Files to Create:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── VerseDisplay.tsx
│   │   ├── ChatInterface.tsx
│   │   ├── LexiconPanel.tsx
│   │   ├── VerseSearch.tsx
│   │   └── AuthForm.tsx
│   ├── services/
│   │   ├── api.ts            # Axios client
│   │   ├── verseAPI.ts
│   │   ├── chatAPI.ts
│   │   ├── lexiconAPI.ts
│   │   └── authAPI.ts
│   ├── types/
│   │   ├── verse.ts
│   │   ├── chat.ts
│   │   ├── user.ts
│   │   └── lexicon.ts
│   └── hooks/
│       ├── useWebSocket.ts   # WebSocket hook
│       ├── useVerse.ts
│       ├── useAuth.ts
│       └── useLexicon.ts
└── package.json
```

**Tech Stack:**
- React 18
- TypeScript 5.x
- Vite 5.x
- TailwindCSS 3.x
- React Router 6.x
- Axios (HTTP client)
- WebSocket API (native)

---

### **Week 5-7: Integration & Pages** ✓ Tasks 13-18

**Goal:** Assemble components into complete pages

**Tasks:**
13. ✅ Build Dashboard page with integrated study interface
14. ✅ Build Login and Register pages with authentication flow
15. ✅ Create custom React hooks for WebSocket and state management
16. ✅ Implement protected routes and authentication routing
17. ✅ Add Greek font support and text rendering utilities
18. ✅ Add conversation history persistence to database

**Deliverable:** Fully functional web app (MVP complete!)
- Users can register, login
- Search verses → see Greek + English
- Ask AI questions → get streaming responses
- Click Greek words → see Strong's definitions
- Conversations saved to database

**Pages:**
- `/` - Dashboard (main study interface)
- `/login` - Login page
- `/register` - Registration page
- `/settings` - Settings (placeholder)
- `/about` - About/Help page

**Layout (Dashboard):**
```
┌────────────────────────────────────────────────────────┐
│  Header: AI Gospel Parser  [User Menu]  [Logout]       │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │              │  │              │  │             │  │
│  │    VERSE     │  │     CHAT     │  │   LEXICON   │  │
│  │   DISPLAY    │  │  INTERFACE   │  │    PANEL    │  │
│  │              │  │              │  │             │  │
│  │  [Search]    │  │  [Messages]  │  │  Strong's   │  │
│  │  Greek Text  │  │              │  │  G25: ἀγαπάω│  │
│  │  English Ref │  │  [Input Box] │  │             │  │
│  │              │  │              │  │  (collapsed │  │
│  │              │  │              │  │   on mobile)│  │
│  └──────────────┘  └──────────────┘  └─────────────┘  │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**Mobile Layout (Tabs):**
```
┌──────────────────────────┐
│  AI Gospel Parser   ☰    │
├──────────────────────────┤
│ [Verse] [Chat] [Lexicon] │  ← Tabs
├──────────────────────────┤
│                          │
│  Active Tab Content      │
│                          │
│                          │
│                          │
│                          │
│                          │
└──────────────────────────┘
```

---

### **Week 7-10: Polish & Deploy** ✓ Tasks 19-25

**Goal:** Production-ready application

**Tasks:**
19. ✅ Create Docker setup for easy deployment
20. ✅ Add loading states, error handling, and user feedback
21. ✅ Implement mobile-responsive design and touch interactions
22. ✅ Write integration tests for critical user flows
23. ✅ Create user documentation and onboarding tutorial
24. ✅ Performance optimization and caching strategy
25. ✅ Add analytics and monitoring for production

**Deliverable:** Beta-ready web app
- Dockerized (one-command deployment)
- Mobile-optimized
- Error handling + loading states
- Onboarding tutorial for new users
- Tests written (70%+ coverage)
- Performance optimized (<2s verse lookup)
- Monitoring in place

**Deployment Options:**
1. **Local (Development):**
   ```bash
   # Backend
   cd backend && uvicorn main:app --reload

   # Frontend
   cd frontend && npm run dev
   ```

2. **Docker (Production):**
   ```bash
   docker-compose up -d
   ```

3. **Cloud Deployment:**
   - Backend: Render, Railway, or DigitalOcean
   - Frontend: Vercel, Netlify, or Cloudflare Pages
   - Database: SQLite → PostgreSQL (Supabase, Neon)

---

## 🎯 Success Metrics

**MVP Success Criteria (End of Week 7):**
- ✅ User can register and login
- ✅ User can search for any NT verse
- ✅ Verse displays Greek + English correctly
- ✅ AI chat responds with streaming (like ChatGPT)
- ✅ Lexicon panel shows Strong's definitions
- ✅ Conversations persist across sessions
- ✅ Works on mobile devices

**Beta Launch Success (Week 10):**
- ✅ 50 beta users signed up
- ✅ <2 second verse lookup time
- ✅ <5 second AI response time
- ✅ Zero critical bugs
- ✅ 90%+ uptime
- ✅ Positive user feedback

**Technical Benchmarks:**
- API response time: <500ms (verse lookup)
- WebSocket latency: <100ms (first chunk)
- Page load time: <2s (initial load)
- Mobile performance: 90+ Lighthouse score
- Test coverage: 70%+ on critical paths

---

## 🛠️ Development Workflow

### **Daily Workflow:**
1. Start backend server: `cd backend && uvicorn main:app --reload`
2. Start frontend dev server: `cd frontend && npm run dev`
3. Access app: `http://localhost:5173`
4. Backend API docs: `http://localhost:8000/docs` (FastAPI auto-generated)
5. Test changes, commit frequently

### **Git Workflow:**
```bash
# Create feature branch
git checkout -b feature/verse-lookup

# Make changes, test locally
# ...

# Commit with clear message
git add .
git commit -m "Add verse lookup API endpoint with SBLGNT integration"

# Push and create PR
git push origin feature/verse-lookup
```

### **Testing Before Commit:**
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm run test

# Linting
cd backend && ruff check .
cd frontend && npm run lint

# Type checking
cd frontend && npm run type-check
```

---

## 📚 Resources & Documentation

**FastAPI:**
- Docs: https://fastapi.tiangolo.com
- WebSocket: https://fastapi.tiangolo.com/advanced/websockets/
- Authentication: https://fastapi.tiangolo.com/tutorial/security/

**React + TypeScript:**
- React Docs: https://react.dev
- TypeScript: https://www.typescriptlang.org/docs/
- Vite: https://vitejs.dev

**TailwindCSS:**
- Docs: https://tailwindcss.com/docs
- Components: https://tailwindui.com (paid) or https://daisyui.com (free)

**Deployment:**
- Docker: https://docs.docker.com/compose/
- Render: https://render.com (backend hosting)
- Vercel: https://vercel.com (frontend hosting)

---

## 🚀 Quick Start (Week 1, Day 1)

**1. Create backend directory:**
```bash
cd /home/justin/ai-projects/ai_gospel_parser
mkdir -p backend/{routers,services,models,schemas}
touch backend/main.py
touch backend/config.py
touch backend/database.py
touch backend/requirements.txt
```

**2. Install backend dependencies:**
```bash
cd backend
python -m venv venv_backend
source venv_backend/bin/activate
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart websockets python-dotenv
pip freeze > requirements.txt
```

**3. Create basic FastAPI app:**
Edit `backend/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Gospel Parser API")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Gospel Parser API"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}
```

**4. Run backend:**
```bash
uvicorn main:app --reload
# Visit: http://localhost:8000/docs
```

**5. Create frontend:**
```bash
cd /home/justin/ai-projects/ai_gospel_parser
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install react-router-dom axios tailwindcss
npm run dev
# Visit: http://localhost:5173
```

---

## 📝 Notes

**Environment Variables (.env):**
```bash
# Backend (.env in backend/)
DATABASE_URL=sqlite:///./data/gospel_parser.db
JWT_SECRET_KEY=your-secret-key-change-in-production
AI_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mixtral
GEMINI_API_KEY=your-gemini-key-if-using

# Frontend (.env in frontend/)
VITE_API_URL=http://localhost:8000
```

**Reusing Existing Code:**
- `gospel_parser_interlinear.py` → Backend service (parse verses, query ChromaDB)
- `lexicon_helper.py` → Backend service (Strong's lookups)
- `ai_providers.py` → Backend service (Ollama/Gemini integration)
- `reference_config.py` → Backend config (enabled texts)

**Git Strategy:**
- Main branch: `main` (stable, deployable)
- Development branch: `develop` (active development)
- Feature branches: `feature/task-name`
- Merge develop → main for releases

**Future Enhancements (Post-Beta):**
- Recommendation #2: Grammatical Search
- Recommendation #3: Cross-Reference System
- Recommendation #4: Comparative Analysis (Critical vs Byzantine)
- Phase 2 features (Septuagint, Hebrew OT)

---

**Status:** Ready to begin!
**Next Action:** Start Task #1 (Set up FastAPI project structure)

**Questions?** Refer to this roadmap or ask for clarification.

🚀 Let's build this!
