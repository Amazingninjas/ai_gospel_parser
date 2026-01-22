#!/bin/bash

# AI Gospel Parser Launcher Script
# This script activates the virtual environment and runs the gospel parser

# Change to the script's directory
cd "$(dirname "$0")"

# Check if Ollama is accessible
echo "Checking Ollama connection..."

# Try localhost first
OLLAMA_ACCESSIBLE=false
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama found at localhost:11434"
    OLLAMA_ACCESSIBLE=true
else
    # Try Windows host IP (for WSL)
    WINDOWS_HOST=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
    if [ -n "$WINDOWS_HOST" ]; then
        echo "Trying Windows host at $WINDOWS_HOST:11434..."
        if curl -s http://$WINDOWS_HOST:11434/api/tags > /dev/null 2>&1; then
            echo "✓ Ollama found at $WINDOWS_HOST:11434"
            OLLAMA_ACCESSIBLE=true
        fi
    fi
fi

if [ "$OLLAMA_ACCESSIBLE" = false ]; then
    echo ""
    echo "⚠ Warning: Cannot connect to Ollama"
    echo ""
    echo "TROUBLESHOOTING:"
    echo "1. Make sure Ollama is running on Windows"
    echo "2. Set OLLAMA_HOST environment variable on Windows:"
    echo "   PowerShell (as Admin): [System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'Machine')"
    echo "3. Restart Ollama after setting the variable"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Ensure all dependencies are installed
echo "Ensuring all dependencies are installed..."
pip install -r requirements.txt

# Run the parser
echo ""
echo "Starting AI Gospel Parser..."
echo "================================"
python3 gospel_parser.py "$@"

# Deactivate when done
deactivate
