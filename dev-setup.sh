#!/bin/bash

# GymIntel Web Development Setup
echo "🏋️ Setting up GymIntel Web Development Environment..."

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "❌ Please run this script from the gymintel-web root directory"
    exit 1
fi

# Backend setup
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing backend dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Initialize database (create tables)
echo "Initializing database..."
python3 -c "
import asyncio
from app.database import create_tables
asyncio.run(create_tables())
print('✅ Database tables created')
" 2>/dev/null || echo "⚠️ Database setup skipped (PostgreSQL may not be running)"

cd ..

# Frontend setup
echo "🎨 Setting up Frontend..."
cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

cd ..

echo "🚀 Development environment ready!"
echo ""
echo "📋 Next steps:"
echo "1. Start the backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "2. Start the frontend: cd frontend && npm run dev"
echo ""
echo "🌐 URLs:"
echo "• Frontend: http://localhost:3000"
echo "• Backend API: http://localhost:8000"
echo "• GraphQL Playground: http://localhost:8000/graphql"
echo "• API Docs: http://localhost:8000/docs"