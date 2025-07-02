#!/bin/bash

# Interactive CLI Setup for Vercel and Railway Environments
# This script will guide you through setting up both staging and production environments

set -e

echo "🚀 GymIntel Environment Setup via CLI"
echo "====================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Install Vercel CLI if not present
if ! command_exists vercel; then
    echo -e "${YELLOW}Installing Vercel CLI...${NC}"
    npm install -g vercel
fi

# Install Railway CLI if not present
if ! command_exists railway; then
    echo -e "${YELLOW}Installing Railway CLI...${NC}"
    npm install -g @railway/cli
fi

# Install GitHub CLI if not present (for setting secrets)
if ! command_exists gh; then
    echo -e "${YELLOW}GitHub CLI not found. Install it for automatic secret setup.${NC}"
    echo "Visit: https://cli.github.com/"
fi

echo -e "${GREEN}✅ All prerequisites met${NC}"
echo ""

# Login to services
echo -e "${BLUE}🔐 Service Authentication${NC}"
echo "========================"
echo ""

# Vercel login
echo "Logging into Vercel..."
vercel login

# Railway login
echo ""
echo "Logging into Railway..."
railway login

# Get current user info
VERCEL_USER=$(vercel whoami 2>/dev/null || echo "unknown")
echo -e "${GREEN}✅ Logged into Vercel as: $VERCEL_USER${NC}"

# Setup Vercel Projects
echo ""
echo -e "${BLUE}🔷 Setting up Vercel Projects${NC}"
echo "============================="

cd frontend

# Production Vercel setup
echo ""
echo "Setting up Production Vercel project..."
echo "Run: vercel"
echo "When prompted:"
echo "  - Set up and deploy: Yes"
echo "  - Scope: Select your account"
echo "  - Link to existing project: No"
echo "  - Project name: gymintel-web"
echo "  - Directory: ./"
echo ""
read -p "Press Enter when production project is created..."

# Get production project details
if [ -f ".vercel/project.json" ]; then
    VERCEL_PROJECT_ID_PROD=$(cat .vercel/project.json | grep '"projectId"' | cut -d'"' -f4)
    VERCEL_ORG_ID=$(cat .vercel/project.json | grep '"orgId"' | cut -d'"' -f4)
    echo -e "${GREEN}✅ Production Project ID: $VERCEL_PROJECT_ID_PROD${NC}"
    echo -e "${GREEN}✅ Org ID: $VERCEL_ORG_ID${NC}"

    # Save for later
    echo "VERCEL_ORG_ID=$VERCEL_ORG_ID" > ../.env.deployment
    echo "VERCEL_PROJECT_ID=$VERCEL_PROJECT_ID_PROD" >> ../.env.deployment
fi

# Staging Vercel setup
echo ""
echo "Setting up Staging Vercel project..."
echo "Run: vercel --name gymintel-web-staging"
echo "When prompted:"
echo "  - Set up and deploy: Yes"
echo "  - Link to existing project: No"
echo "  - Project name: gymintel-web-staging"
echo ""
read -p "Press Enter when staging project is created..."

# Get staging project ID
VERCEL_PROJECT_ID_STAGING=$(vercel ls 2>/dev/null | grep "gymintel-web-staging" | awk '{print $1}' || echo "")
if [ -n "$VERCEL_PROJECT_ID_STAGING" ]; then
    echo -e "${GREEN}✅ Staging Project ID: $VERCEL_PROJECT_ID_STAGING${NC}"
    echo "VERCEL_PROJECT_ID_STAGING=$VERCEL_PROJECT_ID_STAGING" >> ../.env.deployment
fi

# Set Vercel environment variables via CLI
echo ""
echo -e "${BLUE}🔧 Setting Vercel Environment Variables${NC}"
echo "====================================="

# Get Mapbox token
MAPBOX_TOKEN=$(prompt_with_default "Enter Mapbox Access Token" "your-mapbox-token")

# Production env vars
echo ""
echo "Setting production environment variables..."
vercel env add VITE_ENVIRONMENT production --yes
vercel env add VITE_GRAPHQL_ENDPOINT production --yes <<< "https://gymintel-backend.railway.app/graphql"
vercel env add VITE_MAPBOX_ACCESS_TOKEN production --yes <<< "$MAPBOX_TOKEN"

# Staging env vars
echo ""
echo "Setting staging environment variables..."
vercel env add VITE_ENVIRONMENT staging --yes <<< "staging"
vercel env add VITE_GRAPHQL_ENDPOINT staging --yes <<< "https://gymintel-backend-staging.railway.app/graphql"
vercel env add VITE_MAPBOX_ACCESS_TOKEN staging --yes <<< "$MAPBOX_TOKEN"
vercel env add VITE_DEBUG staging --yes <<< "true"

cd ..

# Setup Railway Projects
echo ""
echo -e "${BLUE}🚂 Setting up Railway Projects${NC}"
echo "============================="

# Production Railway setup
echo ""
echo "Creating Production Railway project..."
railway init -n gymintel-backend

# Get production project ID
RAILWAY_PROJECT_ID=$(railway status --json 2>/dev/null | grep '"projectId"' | cut -d'"' -f4 || echo "")
if [ -n "$RAILWAY_PROJECT_ID" ]; then
    echo -e "${GREEN}✅ Production Railway Project ID: $RAILWAY_PROJECT_ID${NC}"
    echo "RAILWAY_PROJECT_ID=$RAILWAY_PROJECT_ID" >> .env.deployment
fi

# Add PostgreSQL to production
echo "Adding PostgreSQL to production..."
railway add

# Staging Railway setup
echo ""
echo "Creating Staging Railway project..."
railway init -n gymintel-backend-staging

# Get staging project ID
RAILWAY_PROJECT_ID_STAGING=$(railway status --json 2>/dev/null | grep '"projectId"' | cut -d'"' -f4 || echo "")
if [ -n "$RAILWAY_PROJECT_ID_STAGING" ]; then
    echo -e "${GREEN}✅ Staging Railway Project ID: $RAILWAY_PROJECT_ID_STAGING${NC}"
    echo "RAILWAY_PROJECT_ID_STAGING=$RAILWAY_PROJECT_ID_STAGING" >> .env.deployment
fi

# Add PostgreSQL to staging
echo "Adding PostgreSQL to staging..."
railway add

# Set Railway environment variables
echo ""
echo -e "${BLUE}🔧 Setting Railway Environment Variables${NC}"
echo "======================================"

# Get API keys
YELP_KEY=$(prompt_with_default "Enter Yelp API Key (optional)" "")
GOOGLE_KEY=$(prompt_with_default "Enter Google Places API Key (optional)" "")

# Production Railway env vars
echo ""
echo "Setting production Railway environment variables..."
railway link $RAILWAY_PROJECT_ID
railway variables set ENVIRONMENT=production
railway variables set AUTO_INIT_DB=false
railway variables set SEED_DATABASE=false
railway variables set CORS_ORIGINS=https://gymintel-web.vercel.app
railway variables set LOG_LEVEL=INFO
[ -n "$YELP_KEY" ] && railway variables set YELP_API_KEY="$YELP_KEY"
[ -n "$GOOGLE_KEY" ] && railway variables set GOOGLE_PLACES_API_KEY="$GOOGLE_KEY"

# Get database URL
PROD_DB_URL=$(railway variables get DATABASE_URL)
railway variables set ASYNC_DATABASE_URL="$PROD_DB_URL"

# Staging Railway env vars
echo ""
echo "Setting staging Railway environment variables..."
railway link $RAILWAY_PROJECT_ID_STAGING
railway variables set ENVIRONMENT=staging
railway variables set AUTO_INIT_DB=true
railway variables set SEED_DATABASE=true
railway variables set CORS_ORIGINS=https://gymintel-web-staging.vercel.app,http://localhost:3000
railway variables set LOG_LEVEL=DEBUG
[ -n "$YELP_KEY" ] && railway variables set YELP_API_KEY="$YELP_KEY"
[ -n "$GOOGLE_KEY" ] && railway variables set GOOGLE_PLACES_API_KEY="$GOOGLE_KEY"

# Get database URL
STAGING_DB_URL=$(railway variables get DATABASE_URL)
railway variables set ASYNC_DATABASE_URL="$STAGING_DB_URL"

# Get tokens
echo ""
echo -e "${BLUE}🔑 Retrieving API Tokens${NC}"
echo "======================="

# Vercel token
echo ""
echo "To get your Vercel token:"
echo "1. Visit: https://vercel.com/account/tokens"
echo "2. Create a new token named 'gymintel-github-actions'"
echo "3. Copy the token"
VERCEL_TOKEN=$(prompt_with_default "Enter Vercel Token" "")
echo "VERCEL_TOKEN=$VERCEL_TOKEN" >> .env.deployment

# Railway token
echo ""
echo "To get your Railway token:"
echo "1. Visit: https://railway.app/account/tokens"
echo "2. Create a new token named 'gymintel-github-actions'"
echo "3. Copy the token"
RAILWAY_TOKEN=$(prompt_with_default "Enter Railway Token" "")
echo "RAILWAY_TOKEN=$RAILWAY_TOKEN" >> .env.deployment

# Set GitHub secrets if gh CLI is available
if command_exists gh; then
    echo ""
    echo -e "${BLUE}🔒 Setting GitHub Secrets${NC}"
    echo "======================="

    echo "Setting GitHub secrets..."
    gh secret set VERCEL_TOKEN --body "$VERCEL_TOKEN"
    gh secret set VERCEL_ORG_ID --body "$VERCEL_ORG_ID"
    gh secret set VERCEL_PROJECT_ID --body "$VERCEL_PROJECT_ID_PROD"
    gh secret set VERCEL_PROJECT_ID_STAGING --body "$VERCEL_PROJECT_ID_STAGING"
    gh secret set RAILWAY_TOKEN --body "$RAILWAY_TOKEN"
    gh secret set RAILWAY_TOKEN_STAGING --body "$RAILWAY_TOKEN"
    gh secret set RAILWAY_PROJECT_ID --body "$RAILWAY_PROJECT_ID"
    gh secret set RAILWAY_PROJECT_ID_STAGING --body "$RAILWAY_PROJECT_ID_STAGING"

    echo -e "${GREEN}✅ GitHub secrets configured${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  GitHub CLI not found. Add these secrets manually:${NC}"
    echo ""
    echo "Go to: Settings → Secrets → Actions → New repository secret"
    echo ""
    echo "VERCEL_TOKEN=$VERCEL_TOKEN"
    echo "VERCEL_ORG_ID=$VERCEL_ORG_ID"
    echo "VERCEL_PROJECT_ID=$VERCEL_PROJECT_ID_PROD"
    echo "VERCEL_PROJECT_ID_STAGING=$VERCEL_PROJECT_ID_STAGING"
    echo "RAILWAY_TOKEN=$RAILWAY_TOKEN"
    echo "RAILWAY_TOKEN_STAGING=$RAILWAY_TOKEN"
    echo "RAILWAY_PROJECT_ID=$RAILWAY_PROJECT_ID"
    echo "RAILWAY_PROJECT_ID_STAGING=$RAILWAY_PROJECT_ID_STAGING"
fi

# Summary
echo ""
echo -e "${BLUE}📝 Setup Summary${NC}"
echo "==============="
echo ""
echo "✅ Vercel Projects Created:"
echo "   - Production: gymintel-web"
echo "   - Staging: gymintel-web-staging"
echo ""
echo "✅ Railway Projects Created:"
echo "   - Production: gymintel-backend"
echo "   - Staging: gymintel-backend-staging"
echo ""
echo "✅ Environment Variables Set:"
echo "   - Vercel: Production & Staging"
echo "   - Railway: Production & Staging"
echo ""

if [ -f ".env.deployment" ]; then
    echo "✅ Deployment credentials saved to .env.deployment"
    echo "   ⚠️  Add .env.deployment to .gitignore!"
fi

echo ""
echo -e "${GREEN}🎉 Environment setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Create staging branch: git checkout -b staging && git push -u origin staging"
echo "2. Deploy to staging: git push origin staging"
echo "3. Deploy to production: Create PR from staging to main"
echo ""
echo "Test URLs:"
echo "- Staging Frontend: https://gymintel-web-staging.vercel.app"
echo "- Staging Backend: https://gymintel-backend-staging.railway.app/health"
echo "- Production Frontend: https://gymintel-web.vercel.app"
echo "- Production Backend: https://gymintel-backend.railway.app/health"
