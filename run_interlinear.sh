#!/bin/bash

echo "===================================="
echo "AI Gospel Parser - Interlinear Mode"
echo "===================================="
echo

cd "$(dirname "$0")"

# Check if Ollama is running (WSL-aware)
echo "[1/3] Checking Ollama connection..."

# Get Windows host IP (for WSL)
OLLAMA_HOST="localhost"
if [ -f /etc/resolv.conf ]; then
    WIN_HOST=$(grep nameserver /etc/resolv.conf | awk '{print $2}' | head -n1)
    if [ -n "$WIN_HOST" ]; then
        OLLAMA_HOST="$WIN_HOST"
    fi
fi

if ! curl -s http://$OLLAMA_HOST:11434/api/tags > /dev/null 2>&1; then
    echo "[!] ERROR: Cannot connect to Ollama at http://$OLLAMA_HOST:11434"
    echo
    echo "Please ensure Ollama is running:"
    echo "  Windows: Start Ollama from the Start menu or system tray"
    echo "  Linux/Mac: Run 'ollama serve' in a terminal"
    echo
    exit 1
fi
echo "[OK] Ollama is running at $OLLAMA_HOST:11434"

# Check if virtual environment exists
echo
echo "[2/3] Checking Python virtual environment..."
if [ ! -f "venv/bin/activate" ]; then
    echo "[!] Virtual environment not found. Creating..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[!] ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
echo
echo "[3/3] Checking dependencies..."
python3 -c "import chromadb" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[!] Installing dependencies..."
    pip install -r requirements.txt
fi
echo "[OK] Dependencies ready"

# Run the interlinear parser
echo
echo "===================================="
echo "Starting Interlinear Gospel Parser"
echo "===================================="
echo
python3 gospel_parser_interlinear.py
