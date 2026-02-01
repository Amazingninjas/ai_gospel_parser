#!/bin/bash
# AI Gospel Parser - Quick Setup Script

echo "AI Gospel Parser - Portable Installation"
echo "========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found."
    echo "Please run this script from the ai_gospel_parser directory."
    exit 1
fi

echo "Starting AI Gospel Parser..."
echo ""

# Start containers
docker-compose up -d

echo ""
echo "========================================="
echo "Installation complete!"
echo ""
echo "Access the application at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000/docs"
echo ""
echo "To stop: docker-compose down"
echo "========================================="
