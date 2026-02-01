AI GOSPEL PARSER - PORTABLE INSTALLATION KIT
=============================================

IMPORTANT: This folder alone is NOT enough for installation!

You need the ENTIRE repository because Docker builds from source code.

HOW TO CREATE A PORTABLE INSTALLATION:
=======================================

Option 1: Use Git (Recommended)
--------------------------------
1. On target computer, install Docker Desktop
2. Clone the repository:
   git clone https://github.com/Amazingninjas/ai_gospel_parser.git
3. Run: docker-compose up -d
4. Access: http://localhost:3000

Option 2: Flash Drive (Full Copy)
----------------------------------
1. Copy the ENTIRE ai_gospel_parser folder to flash drive
2. On target computer:
   - Install Docker Desktop
   - Copy folder from flash drive to local drive
   - Open terminal in that folder
   - Run: docker-compose up -d
   - Access: http://localhost:3000

Option 3: Export Docker Images (Large Files ~1-2GB)
----------------------------------------------------
If you want truly portable without rebuilding:

On source computer:
  docker save -o gospel-parser-images.tar \
    ai_gospel_parser-backend \
    ai_gospel_parser-frontend
  
  Copy gospel-parser-images.tar to flash drive

On target computer:
  docker load -i gospel-parser-images.tar
  docker-compose up -d

WHAT'S IN THIS FOLDER:
======================
- docker-compose.yml: Container orchestration
- .env.example: Environment variables template  
- INSTALL.md: Detailed installation instructions
- setup.sh: Quick setup script (Linux/Mac)
- README.txt: This file

REQUIREMENTS:
=============
- Docker Desktop installed and running
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space
- Internet connection (for first-time image pull)

ACCESS URLS:
============
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

SUPPORT:
========
GitHub: https://github.com/Amazingninjas/ai_gospel_parser
Issues: https://github.com/Amazingninjas/ai_gospel_parser/issues
