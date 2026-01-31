#!/bin/bash
# Test the AI Gospel Parser Docker deployment

echo "Testing AI Gospel Parser..."
echo ""

echo "1. Testing Backend Health..."
curl -s http://localhost:8000/api/health && echo "" || echo "❌ Backend not responding"

echo ""
echo "2. Testing Verse Lookup..."
curl -s "http://localhost:8000/api/verses/John%203:16" | python3 -m json.tool | head -5 || echo "❌ Verse lookup failed"

echo ""
echo "3. Testing Lexicon..."
curl -s "http://localhost:8000/api/lexicon/strongs/G25" | python3 -m json.tool | head -5 || echo "❌ Lexicon failed"

echo ""
echo "✅ All tests complete!"
echo ""
echo "Open in browser:"
echo "  Frontend: http://localhost:3000"
echo "  API Docs: http://localhost:8000/docs"
