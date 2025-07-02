# Staging Environment Setup

This guide covers setting up staging environments for testing deployments before production.

## Overview

We use three separate environments:
- **Development**: Local development (localhost)
- **Staging**: Testing deployments and integration
- **Production**: Live application

Staging environments are used to:
- Test deployment configurations
- Validate environment variables
- Preview features before production
- Test CI/CD pipelines

## Vercel Staging Environment

### 1. Create Staging Project in Vercel

```bash
cd frontend

# Login to Vercel (if not already)
npx vercel login

# Create a new project for staging
npx vercel --name gymintel-web-staging
```

When prompted:
- Set up and deploy: Yes
- Scope: Select your account
- Link to existing project: No
- Project name: `gymintel-web-staging`
- Directory: `./` (current directory)
- Override settings: No

### 2. Configure Staging Environment

```bash
# Set environment to staging
npx vercel env add VITE_ENVIRONMENT staging
# Enter: staging

# Set GraphQL endpoint for staging backend
npx vercel env add VITE_GRAPHQL_ENDPOINT staging
# Enter: https://gymintel-backend-staging.railway.app/graphql

# Set Mapbox token (same as production)
npx vercel env add VITE_MAPBOX_ACCESS_TOKEN staging
# Enter: your-mapbox-token
```

### 3. Set Up Git Integration

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select `gymintel-web-staging` project
3. Go to `Settings → Git`
4. Connect to GitHub repository
5. Set:
   - Production Branch: `staging`
   - Automatic Deployments: Enable for `staging` branch

### 4. Update vercel.json for Staging

Create `frontend/vercel.staging.json`:

```json
{
  "version": 2,
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "env": {
    "NODE_ENV": "staging",
    "VITE_ENVIRONMENT": "staging"
  },
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

## Railway Staging Environment

### 1. Create Staging Service

```bash
# Install Railway CLI if not already installed
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project for staging
railway init
# Select: Create new project
# Name: gymintel-backend-staging
```

### 2. Configure PostgreSQL for Staging

```bash
# Link to the staging project
railway link

# Add PostgreSQL plugin
railway add postgresql

# Get the database URL
railway variables
```

### 3. Set Environment Variables

```bash
# Set all required environment variables
railway variables set ENVIRONMENT=staging
railway variables set ASYNC_DATABASE_URL=$DATABASE_URL
railway variables set AUTO_INIT_DB=true
railway variables set SEED_DATABASE=true
railway variables set CORS_ORIGINS=https://gymintel-web-staging.vercel.app,http://localhost:3000
railway variables set LOG_LEVEL=DEBUG

# Optional: Set API keys if needed for staging
railway variables set YELP_API_KEY=your-staging-yelp-key
railway variables set GOOGLE_PLACES_API_KEY=your-staging-google-key
```

### 4. Deploy Staging Backend

```bash
# Deploy to Railway
railway up

# Get deployment URL
railway open
```

### 5. Configure GitHub Integration

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Select `gymintel-backend-staging` project
3. Go to `Settings → GitHub`
4. Connect repository
5. Set:
   - Deploy on push: Enable
   - Branch: `staging`
   - Root directory: `/backend`

## Environment-Specific Configuration

### Backend Configuration

Create `backend/app/config_staging.py`:

```python
from .config import Settings

class StagingSettings(Settings):
    """Staging-specific settings"""

    environment: str = "staging"
    debug: bool = True
    log_level: str = "DEBUG"

    # Staging CORS settings
    cors_origins: list = [
        "https://gymintel-web-staging.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173"
    ]

    # Enable auto-initialization in staging
    auto_init_db: bool = True
    seed_database: bool = True

    class Config:
        env_prefix = "STAGING_"
```

### Frontend Configuration

Create `frontend/.env.staging`:

```env
VITE_ENVIRONMENT=staging
VITE_GRAPHQL_ENDPOINT=https://gymintel-backend-staging.railway.app/graphql
VITE_MAPBOX_ACCESS_TOKEN=your-mapbox-token
VITE_DEBUG=true
```

## Branch Strategy

### Recommended Git Flow

```mermaid
main (production)
  └── staging (staging environment)
       └── feature/* (feature branches)
       └── fix/* (bugfix branches)
```

### Deployment Triggers

- **Production**: Merges to `main` branch
- **Staging**: Merges to `staging` branch
- **Preview**: Pull requests to `staging` or `main`

## Testing Staging Deployments

### 1. Create Staging Branch

```bash
git checkout -b staging
git push -u origin staging
```

### 2. Verify Deployments

- **Vercel**: Check `https://gymintel-web-staging.vercel.app`
- **Railway**: Check `https://gymintel-backend-staging.railway.app/health`

### 3. Test GraphQL Connection

```bash
# Test GraphQL endpoint
curl https://gymintel-backend-staging.railway.app/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { queryType { name } } }"}'
```

## Environment Variables Reference

### Vercel (Frontend)

| Variable | Development (Local) | Staging | Production |
|----------|-------------------|---------|------------|
| VITE_ENVIRONMENT | development | staging | production |
| VITE_GRAPHQL_ENDPOINT | `http://localhost:8000/graphql` | `https://gymintel-backend-staging.railway.app/graphql` | `https://gymintel-backend.railway.app/graphql` |
| VITE_MAPBOX_ACCESS_TOKEN | same-token | same-token | same-token |
| VITE_DEBUG | true | true | false |

### Railway (Backend)

| Variable | Development (Local) | Staging | Production |
|----------|-------------------|---------|------------|
| ENVIRONMENT | development | staging | production |
| DATABASE_URL | (local) | (auto) | (auto) |
| ASYNC_DATABASE_URL | (local) | (same as DATABASE_URL) | (same as DATABASE_URL) |
| AUTO_INIT_DB | true | true | false |
| SEED_DATABASE | true | true | false |
| CORS_ORIGINS | `http://localhost:3000` | staging URLs | prod URLs |
| LOG_LEVEL | DEBUG | DEBUG | INFO |

## Monitoring Staging Environment

### Vercel Analytics

1. Go to `Vercel Dashboard → Analytics`
2. Monitor:
   - Build times
   - Error rates
   - Performance metrics

### Railway Metrics

1. Go to `Railway Dashboard → Metrics`
2. Monitor:
   - CPU usage
   - Memory usage
   - Database connections
   - Response times

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Verify CORS_ORIGINS includes your Vercel staging URL
   - Check browser console for specific origin

2. **Database Connection Issues**
   - Ensure ASYNC_DATABASE_URL is set correctly
   - Check Railway logs: `railway logs`

3. **Build Failures**
   - Check Vercel build logs
   - Verify all environment variables are set

### Debug Commands

```bash
# Check Vercel deployment
npx vercel ls
npx vercel logs gymintel-web-staging

# Check Railway deployment
railway logs
railway status

# Test endpoints
curl https://gymintel-backend-staging.railway.app/health
curl https://gymintel-backend-staging.railway.app/docs
```

## Cleanup

To remove staging environment:

### Vercel
```bash
npx vercel remove gymintel-web-staging
```

### Railway
```bash
railway down
railway delete
```
