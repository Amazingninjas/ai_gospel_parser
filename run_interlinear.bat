@echo off
echo ====================================
echo AI Gospel Parser - Interlinear Mode
echo ====================================
echo.

cd /d "%~dp0"

REM Check if Ollama is running
echo [1/3] Checking Ollama connection...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Cannot connect to Ollama at http://localhost:11434
    echo.
    echo Please ensure Ollama is running:
    echo   1. Open a new terminal
    echo   2. Run: ollama serve
    echo   3. Then run this script again
    echo.
    pause
    exit /b 1
)
echo [OK] Ollama is running

REM Check if virtual environment exists
echo.
echo [2/3] Checking Python virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo [!] Virtual environment not found. Creating...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [!] ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo.
echo [3/3] Checking dependencies...
python -c "import chromadb" 2>nul
if %errorlevel% neq 0 (
    echo [!] Installing dependencies...
    pip install -r requirements.txt
)
echo [OK] Dependencies ready

REM Run the interlinear parser
echo.
echo ====================================
echo Starting Interlinear Gospel Parser
echo ====================================
echo.
python gospel_parser_interlinear.py

pause
