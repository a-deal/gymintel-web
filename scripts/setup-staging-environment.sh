#!/bin/bash

# Setup Staging Environment Script
# This script helps set up Vercel and Railway staging environments

set -e

echo "🚀 GymIntel Staging Environment Setup"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to prompt for input with default
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    local response

    read -p "$prompt [$default]: " response
    echo "${response:-$default}"
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists npm; then
    echo -e "${RED}❌ npm is not installed. Please install Node.js first.${NC}"
    exit 1
fi

if ! command_exists git; then
    echo -e "${RED}❌ git is not installed. Please install git first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites met${NC}"
echo ""

# Vercel Setup
echo "🔷 Setting up Vercel Staging Environment"
echo "==========================================="

if ! command_exists vercel; then
    echo -e "${YELLOW}Installing Vercel CLI...${NC}"
    npm install -g vercel
fi

cd frontend

echo ""
echo "Please follow these steps:"
echo "1. Run: npx vercel login (if not already logged in)"
echo "2. Run: npx vercel --name gymintel-web-staging"
echo "3. When prompted:"
echo "   - Set up and deploy: Yes"
echo "   - Link to existing project: No"
echo "   - Project name: gymintel-web-staging"
echo ""

read -p "Press Enter when you've completed the Vercel setup..."

# Get Vercel project details
if [ -f ".vercel/project.json" ]; then
    echo -e "${GREEN}✅ Vercel project created${NC}"
    VERCEL_PROJECT_ID=$(cat .vercel/project.json | grep '"projectId"' | cut -d'"' -f4)
    VERCEL_ORG_ID=$(cat .vercel/project.json | grep '"orgId"' | cut -d'"' -f4)
    echo "Project ID: $VERCEL_PROJECT_ID"
    echo "Org ID: $VERCEL_ORG_ID"
else
    echo -e "${RED}❌ Vercel project not found. Please run the setup commands above.${NC}"
    exit 1
fi

# Set Vercel environment variables
echo ""
echo "Setting Vercel environment variables..."

BACKEND_STAGING_URL=$(prompt_with_default "Enter Railway staging backend URL" "https://gymintel-backend-staging.railway.app")
MAPBOX_TOKEN=$(prompt_with_default "Enter Mapbox access token" "your-mapbox-token")

echo ""
echo "Run these commands to set environment variables:"
echo "npx vercel env add VITE_ENVIRONMENT staging"
echo "  Enter: staging"
echo ""
echo "npx vercel env add VITE_GRAPHQL_ENDPOINT staging"
echo "  Enter: ${BACKEND_STAGING_URL}/graphql"
echo ""
echo "npx vercel env add VITE_MAPBOX_ACCESS_TOKEN staging"
echo "  Enter: ${MAPBOX_TOKEN}"
echo ""

read -p "Press Enter when you've set the environment variables..."

cd ..

# Railway Setup
echo ""
echo "🚂 Setting up Railway Staging Environment"
echo "==========================================="

if ! command_exists railway; then
    echo -e "${YELLOW}Installing Railway CLI...${NC}"
    npm install -g @railway/cli
fi

echo ""
echo "Please follow these steps:"
echo "1. Run: railway login (if not already logged in)"
echo "2. Run: railway init"
echo "   - Select: Create new project"
echo "   - Name: gymintel-backend-staging"
echo "3. Run: railway link (select gymintel-backend-staging)"
echo "4. Run: railway add postgresql"
echo ""

read -p "Press Enter when you've completed the Railway setup..."

# Set Railway environment variables
echo ""
echo "Setting Railway environment variables..."

VERCEL_STAGING_URL="https://gymintel-web-staging.vercel.app"
YELP_KEY=$(prompt_with_default "Enter Yelp API key (optional)" "")
GOOGLE_KEY=$(prompt_with_default "Enter Google Places API key (optional)" "")

echo ""
echo "Run these commands to set environment variables:"
echo "railway variables set ENVIRONMENT=staging"
echo "railway variables set AUTO_INIT_DB=true"
echo "railway variables set SEED_DATABASE=true"
echo "railway variables set CORS_ORIGINS=${VERCEL_STAGING_URL},http://localhost:3000,http://localhost:5173"
echo "railway variables set LOG_LEVEL=DEBUG"

if [ -n "$YELP_KEY" ]; then
    echo "railway variables set YELP_API_KEY=${YELP_KEY}"
fi

if [ -n "$GOOGLE_KEY" ]; then
    echo "railway variables set GOOGLE_PLACES_API_KEY=${GOOGLE_KEY}"
fi

echo ""
echo "railway variables set ASYNC_DATABASE_URL=\$DATABASE_URL"
echo ""

read -p "Press Enter when you've set the environment variables..."

# Create staging branch
echo ""
echo "🌿 Creating staging branch..."

if ! git show-ref --verify --quiet refs/heads/staging; then
    git checkout -b staging
    echo -e "${GREEN}✅ Created 'staging' branch${NC}"
else
    echo -e "${YELLOW}ℹ️  'staging' branch already exists${NC}"
fi

# Summary
echo ""
echo "📝 Setup Summary"
echo "================"
echo ""
echo "Vercel Staging:"
echo "  - Project: gymintel-web-staging"
echo "  - Deploy branch: staging"
echo "  - URL: https://gymintel-web-staging.vercel.app"
echo ""
echo "Railway Staging:"
echo "  - Project: gymintel-backend-staging"
echo "  - Deploy branch: staging"
echo "  - URL: ${BACKEND_STAGING_URL}"
echo ""
echo "Next Steps:"
echo "1. Push the 'staging' branch: git push -u origin staging"
echo "2. Configure GitHub integration in both Vercel and Railway dashboards"
echo "3. Set deployment branch to 'staging' for both services"
echo "4. Deploy: railway up (for Railway)"
echo ""
echo -e "${GREEN}✅ Staging environment setup complete!${NC}"
echo ""
echo "Test your setup:"
echo "  - Backend health: curl ${BACKEND_STAGING_URL}/health"
echo "  - Frontend: https://gymintel-web-staging.vercel.app"
