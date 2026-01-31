#!/bin/bash

echo "🎯 AI Gospel Parser - Quick Launch Test"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "🧹 Step 1: Cleaning up old containers..."
docker-compose down -v 2>/dev/null

echo ""
echo "🏗️  Step 2: Building and starting services..."
docker-compose up -d --build

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services. Check Docker is running."
    exit 1
fi

echo ""
echo "⏳ Step 3: Waiting for services to start (15 seconds)..."
sleep 15

echo ""
echo "🔍 Step 4: Testing endpoints..."
echo ""

echo "Backend health check:"
curl -s http://localhost:8000/api/health | python3 -m json.tool 2>/dev/null || echo "⚠️  Backend not responding yet"

echo ""
echo ""

echo "Frontend check:"
curl -s http://localhost:3000 > /dev/null && echo "✅ Frontend is responding" || echo "⚠️  Frontend not responding yet"

echo ""
echo ""
echo "📋 Container status:"
docker-compose ps

echo ""
echo "✅ Launch test complete!"
echo ""
echo "📱 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Register a new account"
echo "   3. Try searching for 'John 3:16'"
echo "   4. Click a Greek word to see the lexicon"
echo "   5. Ask the AI a question"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down"
