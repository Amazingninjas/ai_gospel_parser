@echo off
REM AI Gospel Parser - Quick Setup Script for Windows

echo AI Gospel Parser - Portable Installation
echo =========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Check if we're in the right directory
if not exist "docker-compose.yml" (
    echo ERROR: docker-compose.yml not found.
    echo Please run this script from the ai_gospel_parser directory.
    pause
    exit /b 1
)

echo Starting AI Gospel Parser...
echo.

REM Start containers
docker-compose up -d

echo.
echo =========================================
echo Installation complete!
echo.
echo Access the application at:
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000/docs
echo.
echo To stop: docker-compose down
echo =========================================
echo.
pause
