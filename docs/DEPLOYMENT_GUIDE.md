# Deployment Guide

This guide covers deployment strategies for GymIntel Web Application across different environments.

## Environment Overview

| Environment | Frontend URL | Backend URL | Branch | Purpose |
|------------|--------------|-------------|--------|---------|
| Development | http://localhost:3000 | http://localhost:8000 | feature/* | Local development |
| Staging | https://gymintel-web-staging.vercel.app | https://gymintel-backend-staging.railway.app | staging | Testing & integration |
| Production | https://gymintel-web.vercel.app | https://gymintel-backend.railway.app | main | Live application |

## Deployment Flow

```mermaid
feature/* or fix/* branches
    ↓ (PR)
staging branch → Staging Environment (auto-deploy)
    ↓ (PR)
main branch → Production Environment (auto-deploy)
```

## Setting Up Deployments

### Prerequisites

1. **GitHub Secrets** (Required for both environments):
   ```bash
   # Vercel
   VERCEL_TOKEN
   VERCEL_ORG_ID
   VERCEL_PROJECT_ID         # Production
   VERCEL_PROJECT_ID_STAGING # Staging

   # Railway
   RAILWAY_TOKEN             # Production
   RAILWAY_TOKEN_STAGING     # Staging
   RAILWAY_PROJECT_ID        # Production
   RAILWAY_PROJECT_ID_STAGING # Staging
   ```

2. **Environment Variables**:
   - Set in Vercel Dashboard for each project
   - Set in Railway Dashboard for each project

### Initial Setup

1. **Run the setup script**:
   ```bash
   ./scripts/setup-staging-environment.sh
   ```

2. **Configure GitHub Integration**:
   - In Vercel: `Settings → Git → Connect Repository`
   - In Railway: `Settings → GitHub → Connect Repository`

3. **Set deployment branches**:
   - Staging: `staging` branch
   - Production: `main` branch

## Deployment Process

### Feature Development

1. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Develop and test locally**:
   ```bash
   ./scripts/dev-start.sh
   ```

3. **Create PR to staging**:
   ```bash
   git push origin feature/your-feature
   gh pr create --base staging
   ```

4. **After PR merge**: Automatically deploys to staging

### Production Release

1. **Create PR from staging to main**:
   ```bash
   git checkout staging
   git pull origin staging
   gh pr create --base main --title "Release: v1.x.x"
   ```

2. **After PR merge**: Automatically deploys to production

## Manual Deployment

### Deploy to Staging

```bash
# Backend
cd backend
railway link  # Select gymintel-backend-staging
railway up --environment staging

# Frontend
cd frontend
vercel --prod --env staging
```

### Deploy to Production

```bash
# Backend
cd backend
railway link  # Select gymintel-backend
railway up

# Frontend
cd frontend
vercel --prod
```

## Environment Configuration

### Backend Environment Variables

#### Development (Local)

```env
ENVIRONMENT=development
DATABASE_URL=postgresql://postgres:password@localhost:5432/gymintel  # pragma: allowlist secret
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/gymintel  # pragma: allowlist secret
AUTO_INIT_DB=true
SEED_DATABASE=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=DEBUG
YELP_API_KEY=your-dev-key
GOOGLE_PLACES_API_KEY=your-dev-key
```

#### Staging

```env
ENVIRONMENT=staging
DATABASE_URL=(auto-provided by Railway)
ASYNC_DATABASE_URL=$DATABASE_URL
AUTO_INIT_DB=true
SEED_DATABASE=true
CORS_ORIGINS=https://gymintel-web-staging.vercel.app,http://localhost:3000
LOG_LEVEL=DEBUG
YELP_API_KEY=your-staging-key
GOOGLE_PLACES_API_KEY=your-staging-key
```

#### Production

```env
ENVIRONMENT=production
DATABASE_URL=(auto-provided by Railway)
ASYNC_DATABASE_URL=$DATABASE_URL
AUTO_INIT_DB=false
SEED_DATABASE=false
CORS_ORIGINS=https://gymintel-web.vercel.app
LOG_LEVEL=INFO
YELP_API_KEY=your-prod-key
GOOGLE_PLACES_API_KEY=your-prod-key
```

### Frontend Environment Variables

#### Development (Local)

```env
VITE_ENVIRONMENT=development
VITE_GRAPHQL_ENDPOINT=http://localhost:8000/graphql
VITE_MAPBOX_ACCESS_TOKEN=your-token
VITE_DEBUG=true
```

#### Staging

```env
VITE_ENVIRONMENT=staging
VITE_GRAPHQL_ENDPOINT=https://gymintel-backend-staging.railway.app/graphql
VITE_MAPBOX_ACCESS_TOKEN=your-token
VITE_DEBUG=true
```

#### Production

```env
VITE_ENVIRONMENT=production
VITE_GRAPHQL_ENDPOINT=https://gymintel-backend.railway.app/graphql
VITE_MAPBOX_ACCESS_TOKEN=your-token
VITE_DEBUG=false
```

## Monitoring Deployments

### Health Checks

```bash
# Staging
curl https://gymintel-backend-staging.railway.app/health
curl https://gymintel-backend-staging.railway.app/docs

# Production
curl https://gymintel-backend.railway.app/health
curl https://gymintel-backend.railway.app/docs
```

### Logs

```bash
# Vercel logs
vercel logs gymintel-web-staging
vercel logs gymintel-web

# Railway logs
railway logs --environment staging
railway logs --environment production
```

### Metrics

- **Vercel**: `Dashboard → Analytics → Web Vitals`
- **Railway**: `Dashboard → Metrics → Resource Usage`

## Rollback Procedures

### Vercel Rollback

```bash
# List deployments
vercel ls

# Rollback to specific deployment
vercel rollback [deployment-url]
```

### Railway Rollback

1. Go to Railway Dashboard
2. Select `project → Deployments`
3. Click on previous successful deployment
4. Click "Rollback to this deployment"

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check `CORS_ORIGINS` in Railway
   - Verify frontend URL matches exactly

2. **Database Connection Issues**
   - Check `ASYNC_DATABASE_URL` is set
   - Verify PostGIS extension is enabled

3. **Build Failures**
   - Check GitHub Actions logs
   - Verify all secrets are set
   - Check environment variables

### Debug Commands

```bash
# Check deployment status
vercel inspect [deployment-url]
railway status

# Force rebuild
vercel --force
railway up --detach

# Check environment variables
vercel env ls
railway variables
```

## Security Considerations

1. **Secrets Management**:
   - Never commit secrets to repository
   - Use GitHub Secrets for CI/CD
   - Rotate API keys regularly

2. **Environment Isolation**:
   - Development uses separate database
   - Different API keys per environment
   - Restricted CORS origins

3. **Access Control**:
   - Limit production deployments to main branch
   - Use branch protection rules
   - Require PR reviews

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables verified
- [ ] Database migrations ready
- [ ] API keys valid

### Post-Deployment
- [ ] Health checks passing
- [ ] GraphQL endpoint accessible
- [ ] Frontend can connect to backend
- [ ] No console errors

### Monitoring
- [ ] Set up alerts for failures
- [ ] Monitor resource usage
- [ ] Check error rates
- [ ] Review performance metrics
