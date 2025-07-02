# Deployment Secrets Configuration

This document lists all the required GitHub secrets for successful deployment of the GymIntel Web Application.

## Required GitHub Secrets

### Vercel Deployment (Frontend)
- **VERCEL_TOKEN**: Your Vercel personal access token
  - Get it from: <https://vercel.com/account/tokens>
- **VERCEL_ORG_ID**: Your Vercel organization ID
  - Find in Vercel project settings
- **VERCEL_PROJECT_ID**: Your Vercel project ID (Production)
  - Find in Vercel project settings
- **VERCEL_STAGING_PROJECT_ID**: Your Vercel staging project ID
  - Find in Vercel staging project settings

### Railway Deployment (Backend)
- **RAILWAY_TOKEN**: Your Railway API token (Production)
  - Get it from: <https://railway.app/account/tokens>
- **RAILWAY_STAGING_TOKEN**: Your Railway API token (Staging)
  - Get it from: <https://railway.app/account/tokens> (same token can be used)
- **RAILWAY_PROJECT_ID**: Your Railway project ID (Production)
  - Find in Railway project settings
- **RAILWAY_STAGING_PROJECT_ID**: Your Railway staging project ID
  - Find in Railway staging project settings

### API Keys
- **MAPBOX_ACCESS_TOKEN**: Mapbox API key for maps
  - Get it from: <https://account.mapbox.com/>
- **YELP_API_KEY**: Yelp Fusion API key
  - Get it from: <https://www.yelp.com/developers>
- **GOOGLE_PLACES_API_KEY**: Google Places API key
  - Get it from: <https://console.cloud.google.com/>

### Production URLs
- **PRODUCTION_GRAPHQL_ENDPOINT**: Your backend GraphQL endpoint URL
  - Example: `https://your-backend.railway.app/graphql`
- **PRODUCTION_API_URL**: Your backend API base URL
  - Example: `https://your-backend.railway.app`
- **PRODUCTION_FRONTEND_URL**: Your frontend URL
  - Example: `https://your-app.vercel.app`

## Setting up Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret" for each secret above
4. Enter the secret name and value

## Testing Deployments

After setting up all secrets, you can trigger a deployment by:
1. Pushing to the `main` branch
2. Or manually triggering the Deploy workflow from the Actions tab

## Current Status

⚠️ **Missing Secrets** (based on latest CI/CD run):
- VERCEL_TOKEN
- VERCEL_ORG_ID
- VERCEL_PROJECT_ID
- PRODUCTION_GRAPHQL_ENDPOINT
- PRODUCTION_API_URL
- PRODUCTION_FRONTEND_URL

These need to be configured before deployments will succeed.
