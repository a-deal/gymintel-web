## Development Workflow
- All changes must be done on branches not main, create a pr for each
- Use python3 instead of python for all local commands

## Current Status (July 2, 2025)

### Completed Today:
1. **Database Initialization Fix** ✅
   - Created `db_init.py` module for automatic database setup
   - Fixed "relation gyms does not exist" error
   - Added AUTO_INIT_DB environment variable
   - Merged PR successfully

2. **Railway Deployment Fix** ✅
   - Fixed ModuleNotFoundError for uvicorn
   - Switched Dockerfile from Alpine to Debian slim
   - Added uvicorn verification in Dockerfile
   - Updated railway.toml configuration

3. **Gym Search Feature** ✅
   - Implemented location-based search (city or zipcode)
   - Added real-time progress tracking with GraphQL subscriptions
   - Created geocoding service using geopy
   - Added `trigger_gym_search` mutation and `search_progress` subscription
   - PR created: https://github.com/a-deal/gymintel-web/pull/9

4. **Environment Strategy Update** 🚧
   - Restructured from 2 environments to 3:
     - Development: Local (localhost)
     - Staging: Testing & integration
     - Production: Live application
   - Renamed all "development" references to "staging"
   - Updated all configuration files and documentation
   - Created separate deployment workflows

### Current Task: Setting Up Staging Environments
- About to create separate Vercel project for staging (gymintel-web-staging)
- About to create separate Railway project for staging (gymintel-backend-staging)
- Will configure environment variables for both
- Will set up GitHub secrets for CI/CD

### Environment URLs (To Be Created):
| Environment | Frontend | Backend | Branch |
|------------|----------|---------|--------|
| Development | http://localhost:3000 | http://localhost:8000 | feature/* |
| Staging | https://gymintel-web-staging.vercel.app | https://gymintel-backend-staging.railway.app | staging |
| Production | https://gymintel-web.vercel.app | https://gymintel-backend.railway.app | main |

### Deployment Flow:
```
feature/* or fix/* branches
    ↓ (PR)
staging branch → Staging Environment (auto-deploy)
    ↓ (PR)
main branch → Production Environment (auto-deploy)
```

### Files Created/Updated Today:
- `/docs/STAGING_ENVIRONMENTS.md` - Complete staging setup guide
- `/docs/DEPLOYMENT_GUIDE.md` - Updated for 3 environments
- `/.github/workflows/deploy-staging.yml` - Staging deployment workflow
- `/.github/workflows/deploy-preview.yml` - Feature branch preview deployments
- `/scripts/setup-staging-environment.sh` - Interactive staging setup
- `/scripts/setup-environments-cli.sh` - Complete CLI setup guide
- `/frontend/.env.development` - Local dev configuration
- `/frontend/.env.staging` - Staging configuration
- `/frontend/vercel.staging.json` - Staging-specific Vercel config
- `/backend/railway.staging.toml` - Staging-specific Railway config

### Next Steps:
1. Create Vercel staging project (gymintel-web-staging)
2. Create Railway staging project (gymintel-backend-staging)
3. Configure environment variables for both platforms
4. Set up GitHub secrets for automated deployments
5. Create and push staging branch
6. Test deployments
