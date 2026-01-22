@echo off
REM AI Gospel Parser Launcher for Windows
REM This script launches the gospel parser in WSL

echo Starting AI Gospel Parser...
echo.

REM Check if WSL is available
wsl --list >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: WSL is not installed or not running
    echo Please install WSL first
    pause
    exit /b 1
)

REM Launch the parser in WSL
wsl -e bash -c "cd '/mnt/c/Users/Justin/Desktop/AI Projects/ai_gospel_parser' && ./run_parser.sh"

pause
