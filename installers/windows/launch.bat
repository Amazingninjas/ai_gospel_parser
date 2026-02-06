@echo off
REM ============================================================================
REM AI Gospel Parser - Quick Launch Script
REM ============================================================================

echo ============================================================================
echo   AI GOSPEL PARSER - LAUNCHER
echo ============================================================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if Docker is running
echo [1/3] Checking Docker status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker is not running
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)
echo [OK] Docker is running

REM Check if containers are already running
echo [2/3] Checking application status...
docker-compose ps | findstr "Up" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Application is already running
) else (
    echo Starting application...
    docker-compose up -d
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to start application
        echo.
        echo Check Docker logs for details:
        echo   docker-compose logs
        echo.
        pause
        exit /b 1
    )
    echo [OK] Application started
)

echo [3/3] Opening browser...
echo.
timeout /t 2 /nobreak >nul
start http://localhost:3000

echo ============================================================================
echo   APPLICATION IS RUNNING
echo ============================================================================
echo.
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo.
echo To stop the application, run: stop.bat
echo.
echo Press any key to close this window...
pause >nul
exit /b 0
