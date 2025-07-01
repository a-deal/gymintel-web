#!/bin/bash
# Frontend test runner using Docker

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

case "$1" in
  test)
    echo -e "${GREEN}Running frontend tests in Docker...${NC}"
    docker run --rm \
      -v "$FRONTEND_DIR:/app" \
      -w /app \
      node:18-alpine \
      sh -c "npm install && npm test"
    ;;

  test:ci)
    echo -e "${GREEN}Running frontend tests in CI mode...${NC}"
    docker run --rm \
      -v "$FRONTEND_DIR:/app" \
      -w /app \
      node:18-alpine \
      sh -c "npm install && npm run test:ci"
    ;;

  lint)
    echo -e "${GREEN}Running ESLint in Docker...${NC}"
    docker run --rm \
      -v "$FRONTEND_DIR:/app" \
      -w /app \
      node:18-alpine \
      sh -c "npm install && npm run lint"
    ;;

  type-check)
    echo -e "${GREEN}Running TypeScript type check in Docker...${NC}"
    docker run --rm \
      -v "$FRONTEND_DIR:/app" \
      -w /app \
      node:18-alpine \
      sh -c "npm install && npm run type-check"
    ;;

  build)
    echo -e "${GREEN}Building frontend in Docker...${NC}"
    docker run --rm \
      -v "$FRONTEND_DIR:/app" \
      -w /app \
      node:18-alpine \
      sh -c "npm install && npm run build"
    ;;

  dev)
    echo -e "${GREEN}Starting dev server in Docker...${NC}"
    docker run --rm -it \
      -v "$FRONTEND_DIR:/app" \
      -w /app \
      -p 3000:3000 \
      node:18-alpine \
      sh -c "npm install && npm run dev -- --host 0.0.0.0"
    ;;

  shell)
    echo -e "${GREEN}Opening shell in Docker container...${NC}"
    docker run --rm -it \
      -v "$FRONTEND_DIR:/app" \
      -w /app \
      node:18-alpine \
      sh
    ;;

  *)
    echo "Usage: $0 {test|test:ci|lint|type-check|build|dev|shell}"
    echo "  test       - Run tests with watch mode"
    echo "  test:ci    - Run tests in CI mode (no watch)"
    echo "  lint       - Run ESLint"
    echo "  type-check - Run TypeScript type checking"
    echo "  build      - Build for production"
    echo "  dev        - Start development server"
    echo "  shell      - Open shell in container"
    exit 1
    ;;
esac
