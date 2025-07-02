#!/bin/bash
# Setup local development environment for GymIntel Web
# Provides Node.js via nvm and Python tools for pre-commit hooks

set -e

echo "🚀 Setting up local development environment for GymIntel Web..."

# Install nvm if not present
if ! command -v nvm &> /dev/null && [ ! -f "$HOME/.nvm/nvm.sh" ]; then
    echo "📦 Installing nvm (Node Version Manager)..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

    # Source nvm
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi

# Source nvm if available
if [ -f "$HOME/.nvm/nvm.sh" ]; then
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

# Install and use Node 18 if nvm is available
if command -v nvm &> /dev/null; then
    echo "📦 Installing Node.js 18..."
    nvm install 18
    nvm use 18
    nvm alias default 18

    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "⚠️  nvm not available. Please install Node.js 18 manually."
fi

# Setup Python virtual environment for backend linting
echo "🐍 Setting up Python virtual environment..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Install pre-commit in the virtual environment
pip install pre-commit

echo "✅ Local development environment setup complete!"
echo ""
echo "📝 Usage:"
echo "   Frontend development:"
echo "     cd frontend && npm run dev"
echo ""
echo "   Backend development:"
echo "     cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "   Pre-commit hooks:"
echo "     ./scripts/setup-hooks.sh"
echo ""
echo "   Or use Docker:"
echo "     ./scripts/dev-start.sh"
