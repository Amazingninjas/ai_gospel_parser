# AI Gospel Parser - Portable Installation

## Quick Start

### Option 1: From GitHub (Recommended)
```bash
# Clone the repository
git clone https://github.com/Amazingninjas/ai_gospel_parser.git
cd ai_gospel_parser

# Start the application
docker-compose up -d
```

Access at: http://localhost:3000

### Option 2: Portable Installation (This Folder)

**Requirements:**
- Docker Desktop installed and running
- Git (optional, for easy updates)

**Installation Steps:**

1. **Copy entire project from GitHub:**
   ```bash
   git clone https://github.com/Amazingninjas/ai_gospel_parser.git
   cd ai_gospel_parser
   ```

2. **OR copy this folder structure (minimum files needed):**
   - You'll need the full repository because Docker builds from source code
   - This folder alone won't work without the source files

3. **Configure environment (optional):**
   ```bash
   cp .env.example backend/.env
   # Edit backend/.env if needed (SMTP settings, etc.)
   ```

4. **Start the application:**
   ```bash
   docker-compose up -d
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## First Time Setup

1. Visit http://localhost:3000
2. Click "Register" to create an account
3. Use password with 8+ characters
4. Start exploring Greek NT verses!

## Stopping the Application

```bash
docker-compose down
```

## Updating

```bash
git pull origin main
docker-compose up -d --build
```

## Troubleshooting

**Containers won't start:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

**Reset everything:**
```bash
docker-compose down
docker-compose up -d --build
```

**Check if Ollama is needed:**
- AI chat requires Ollama running with Mixtral model
- Without it, verse lookup and lexicon still work
