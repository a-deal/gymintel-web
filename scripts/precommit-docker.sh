#!/bin/bash
# Docker-based pre-commit hook setup for GymIntel Web

set -e

echo "🐳 Setting up Docker-based pre-commit hooks for GymIntel Web..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Install pre-commit if not available
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
fi

# Install the git hook scripts
echo "🔗 Installing pre-commit hooks..."
pre-commit install

echo "🚀 Building Docker environment for frontend linting..."
docker compose build frontend

echo "✅ Docker-based pre-commit hooks setup complete!"
echo ""
echo "📝 The hooks will now:"
echo "   - Run Python linting (Black, isort, flake8) locally"
echo "   - Run frontend linting (ESLint, Prettier, TypeScript) in Docker"
echo "   - Perform security scanning and YAML validation"
echo "   - Prevent node_modules from being committed"
echo ""
echo "🛠️  Commands:"
echo "   - Test hooks: pre-commit run --all-files"
echo "   - Update hooks: pre-commit autoupdate"
echo "   - Skip hooks once: git commit --no-verify"
