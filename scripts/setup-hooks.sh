#!/bin/bash
# Setup pre-commit hooks for GymIntel Web

set -e

echo "🔧 Setting up pre-commit hooks for GymIntel Web..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
fi

# Install the git hook scripts
echo "🔗 Installing pre-commit hooks..."
pre-commit install

# Run hooks on all files to ensure everything is working
echo "🧹 Running pre-commit on all files..."
pre-commit run --all-files || {
    echo "⚠️  Some hooks failed. This is normal on first run."
    echo "   The hooks have auto-fixed issues where possible."
    echo "   Please review the changes and commit them."
}

echo "✅ Pre-commit hooks setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Review any auto-fixed changes"
echo "   2. Commit the changes: git add -A && git commit -m 'Setup pre-commit hooks'"
echo "   3. Hooks will now run automatically on each commit"
echo ""
echo "🛠️  Manual commands:"
echo "   - Run hooks manually: pre-commit run --all-files"
echo "   - Update hooks: pre-commit autoupdate"
echo "   - Skip hooks: git commit --no-verify"
