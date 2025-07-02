#!/bin/bash

# GymIntel Development Cleanup Script
echo "🧹 GymIntel Development Cleanup"
echo "================================"
echo

echo "🛑 Stopping all test processes..."
# Kill any Python development servers
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "python test_server.py" 2>/dev/null
pkill -f "python start_dev.py" 2>/dev/null
pkill -f "python run_server.py" 2>/dev/null

# Kill any Node.js development servers
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo "🐳 Stopping Docker containers..."
docker-compose -f ../docker/docker-compose.yml down 2>/dev/null

echo "🧽 Cleaning up temporary files..."
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Remove Node.js logs
find . -name "npm-debug.log*" -delete 2>/dev/null
find . -name "yarn-debug.log*" -delete 2>/dev/null
find . -name "yarn-error.log*" -delete 2>/dev/null

echo "🔍 Checking for remaining processes..."
REMAINING=$(ps aux | grep -E "(uvicorn|test_server|start_dev|npm run dev)" | grep -v grep)
if [ -z "$REMAINING" ]; then
    echo "✅ All development processes stopped"
else
    echo "⚠️ Some processes may still be running:"
    echo "$REMAINING"
fi

echo "📊 Port status:"
echo "Port 3000: $(lsof -ti:3000 2>/dev/null || echo 'Available')"
echo "Port 8000: $(lsof -ti:8000 2>/dev/null || echo 'Available')"
echo "Port 8001: $(lsof -ti:8001 2>/dev/null || echo 'Available')"
echo "Port 8002: $(lsof -ti:8002 2>/dev/null || echo 'Available')"
echo "Port 8003: $(lsof -ti:8003 2>/dev/null || echo 'Available')"
echo "Port 5432: $(lsof -ti:5432 2>/dev/null || echo 'Available')"

echo
echo "✨ Cleanup complete! Ready for Docker development."
echo "💡 Run './scripts/dev-start.sh' to start the Docker environment."
