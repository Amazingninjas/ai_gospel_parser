# Docker Deployment Guide

This guide explains how to deploy the AI Gospel Parser using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/engine/install/))
- Docker Compose 2.0+ (included with Docker Desktop)
- 4GB+ RAM available for containers
- Ollama running on host machine (for local AI) OR Gemini API key (for cloud AI)

## Quick Start

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd ai_gospel_parser
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.docker .env

# Edit .env and set your configuration
nano .env
```

**Important:** Change `JWT_SECRET_KEY` to a random secret in production!

```bash
# Generate a random secret key
openssl rand -hex 32
```

### 3. Start Services

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 4. Access Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Configuration Options

### AI Provider

#### Option 1: Ollama (Local LLM)

```env
AI_PROVIDER=ollama
OLLAMA_HOST=http://host.docker.internal:11434  # Access host machine
OLLAMA_MODEL=mixtral
```

**Important:** Ollama must be running on your host machine!

```bash
# On host machine (not in Docker)
ollama serve
ollama pull mixtral
```

#### Option 2: Gemini (Cloud LLM)

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-api-key-here
```

Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### Port Configuration

Default ports can be changed in `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8000:8000"  # Change host port: "9000:8000"

  frontend:
    ports:
      - "3000:80"    # Change host port: "8080:80"
```

### Data Persistence

Data is persisted in bind mounts:
- Database: `./backend/data/gospel_parser.db`
- ChromaDB: `./backend/chroma_db_interlinear/`

**Backup Strategy:**

```bash
# Backup database
cp backend/data/gospel_parser.db backup/gospel_parser_$(date +%Y%m%d).db

# Backup ChromaDB
tar -czf backup/chromadb_$(date +%Y%m%d).tar.gz backend/chroma_db_interlinear/
```

## Docker Commands

### Start Services

```bash
# Start in foreground (see logs)
docker-compose up

# Start in background (detached)
docker-compose up -d
```

### Stop Services

```bash
# Stop containers (keeps data)
docker-compose down

# Stop and remove volumes (DELETES DATA!)
docker-compose down -v
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up -d --build

# Rebuild specific service
docker-compose build backend
docker-compose up -d backend
```

### Execute Commands in Containers

```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# Run Python script in backend
docker-compose exec backend python <script.py>
```

## Health Checks

Both services have health checks configured:

```bash
# Check health status
docker-compose ps

# Backend health
curl http://localhost:8000/api/health

# Frontend health
curl http://localhost:3000/health
```

## Production Deployment

### Security Checklist

- [ ] Change `JWT_SECRET_KEY` to a strong random secret
- [ ] Set `AI_PROVIDER` and API keys appropriately
- [ ] Configure firewall rules (only allow necessary ports)
- [ ] Enable HTTPS with reverse proxy (nginx/Caddy)
- [ ] Set up automated backups
- [ ] Configure log rotation
- [ ] Review CORS settings in `backend/main.py`

### HTTPS with Nginx Reverse Proxy

Example nginx config:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket support
    location /api/chat/stream {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Automated Backups

Add to crontab:

```bash
# Backup daily at 2 AM
0 2 * * * cd /path/to/ai_gospel_parser && ./backup.sh
```

Create `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backup/gospel_parser"
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR"
cp backend/data/gospel_parser.db "$BACKUP_DIR/db_$DATE.db"
tar -czf "$BACKUP_DIR/chromadb_$DATE.tar.gz" backend/chroma_db_interlinear/

# Keep only last 30 days
find "$BACKUP_DIR" -name "*.db" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
```

## Troubleshooting

### Backend Can't Connect to Ollama

**Error:** "Failed to connect to Ollama"

**Solution:**
- Ensure Ollama is running: `ollama serve`
- Verify host access: `OLLAMA_HOST=http://host.docker.internal:11434`
- On Linux, use: `OLLAMA_HOST=http://172.17.0.1:11434` (Docker bridge IP)

### Frontend Can't Reach Backend

**Error:** "Network Error" or CORS issues

**Solution:**
- Check backend is running: `curl http://localhost:8000/api/health`
- Verify `VITE_API_URL` in `.env`
- Check CORS settings in `backend/main.py`

### Database Permission Errors

**Error:** "Permission denied" on database file

**Solution:**
```bash
# Fix permissions on host
sudo chown -R 1000:1000 backend/data
sudo chown -R 1000:1000 backend/chroma_db_interlinear
```

### Container Won't Start

**Error:** "Error starting userland proxy"

**Solution:**
- Port already in use. Change port mapping or stop conflicting service
- Check with: `sudo lsof -i :8000` or `sudo lsof -i :3000`

### Out of Memory

**Error:** Container killed or OOM

**Solution:**
- Increase Docker memory limit (Docker Desktop > Settings > Resources)
- Use smaller AI model: `OLLAMA_MODEL=phi3:mini`

### ChromaDB Data Not Persisting

**Solution:**
```bash
# Ensure directory exists
mkdir -p backend/chroma_db_interlinear

# Check volume mount in docker-compose.yml
docker-compose config | grep chroma_db_interlinear
```

## Updating

### Pull Latest Changes

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build
```

### Database Migrations

If database schema changes:

```bash
# Backup first!
cp backend/data/gospel_parser.db backup/

# Restart backend (auto-migrates)
docker-compose restart backend
```

## Monitoring

### Resource Usage

```bash
# View resource usage
docker stats

# View disk usage
docker system df
```

### Log Management

Logs are stored in Docker's log system. To prevent disk space issues:

```yaml
# Add to docker-compose.yml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Uninstall

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi gospel-parser-backend gospel-parser-frontend

# Remove data (CAUTION!)
rm -rf backend/data backend/chroma_db_interlinear
```

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Verify health: `curl http://localhost:8000/api/health`
- Review environment variables: `docker-compose config`

## Next Steps

- Set up HTTPS with Let's Encrypt
- Configure automated backups
- Set up monitoring (Prometheus, Grafana)
- Enable log aggregation (ELK stack)
- Configure CI/CD pipeline
