# Vercel Setup Guide for GymIntel Web

This guide walks through setting up Vercel deployment for the GymIntel frontend.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed locally (optional): `npm i -g vercel`

## Step 1: Create Vercel Project

### Option A: Using Vercel CLI (Recommended)
```bash
cd frontend
npx vercel

# Follow prompts:
# - Login to Vercel (if not already)
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? gymintel-web
# - In which directory is your code located? ./
# - Want to override settings? No
```

### Option B: Using Vercel Dashboard
1. Go to https://vercel.com/new
2. Import Git Repository → Select `a-deal/gymintel-web`
3. Configure Project:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

## Step 2: Get Required Tokens

After creating the project, you need three values:

### 1. Vercel Token
- Go to: https://vercel.com/account/tokens
- Click "Create Token"
- Name: `gymintel-github-actions`
- Scope: Full Access
- Copy the token

### 2. Organization ID
```bash
# Using CLI
vercel whoami

# Or from Dashboard
# Go to: https://vercel.com/[your-username]/settings
# Find "Your ID" under Team Settings
```

### 3. Project ID
```bash
# Using CLI (in frontend directory)
vercel project ls

# Or from Dashboard
# Go to your project → Settings → General
# Find "Project ID"
```

## Step 3: Configure Environment Variables in Vercel

Go to your project settings → Environment Variables and add:

```
VITE_GRAPHQL_ENDPOINT = https://your-backend-api.railway.app/graphql
VITE_MAPBOX_ACCESS_TOKEN = your-mapbox-token
```

## Step 4: Add GitHub Secrets

In your GitHub repository, go to Settings → Secrets → Actions and add:

```
VERCEL_TOKEN = (token from step 2.1)
VERCEL_ORG_ID = (org ID from step 2.2)
VERCEL_PROJECT_ID = (project ID from step 2.3)
```

## Step 5: Test Deployment

### Manual Test (CLI)
```bash
cd frontend
vercel --prod
```

### GitHub Actions Test
Push to main branch and check Actions tab

## Troubleshooting

### Deployment Hangs
1. Check if all secrets are set correctly
2. Verify project exists in Vercel dashboard
3. Check Vercel project logs: https://vercel.com/[username]/[project]/deployments

### Build Fails
1. Test build locally: `cd frontend && npm run build`
2. Check Node version compatibility (should be 18+)
3. Verify all environment variables are set

### Common Issues

**Issue: "Project not found"**
- Solution: Make sure VERCEL_PROJECT_ID matches exactly

**Issue: "Invalid token"**
- Solution: Regenerate token and update GitHub secret

**Issue: "No output directory"**
- Solution: Ensure `dist` folder is created during build

## Vercel Project Settings

Recommended settings in Vercel Dashboard:

### Build & Development Settings
- Framework Preset: Vite
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`
- Development Command: `npm run dev`

### Node.js Version
- 18.x (set in project settings)

### Environment Variables
- Add all `VITE_*` variables for production
- Different values per environment (preview/production)

## Alternative: Direct GitHub Integration

Instead of GitHub Actions, you can use Vercel's GitHub integration:

1. In Vercel Dashboard → Import Project
2. Connect GitHub account
3. Select repository
4. Vercel will auto-deploy on every push

This eliminates the need for tokens but gives less control over the deployment process.
