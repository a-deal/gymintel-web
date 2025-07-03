## Development Workflow
- All changes must be done on branches not main, create a pr for each
- Use python3 instead of python for all local commands
- Always use docker for local development

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
   - Implemented location-based search (originally city or zipcode)
   - Added real-time progress tracking with GraphQL subscriptions
   - Created geocoding service using geopy
   - Added `trigger_gym_search` mutation and `search_progress` subscription
   - PR created: https://github.com/a-deal/gymintel-web/pull/9

4. **Environment Strategy Update** ✅
   - Restructured from 2 environments to 3:
     - Development: Local (localhost)
     - Staging: Testing & integration
     - Production: Live application
   - Renamed all "development" references to "staging"
   - Updated all configuration files and documentation
   - Created separate deployment workflows
   - Successfully created staging environments on Vercel and Railway

5. **City-Based Search Implementation** ✅
   - Removed ALL ZIP code references from the codebase
   - Implemented city-based search using PostGIS geographic queries
   - Added Google Places API integration for city autocomplete
   - Created Material-UI autocomplete components for city search
   - Updated all GraphQL schemas, queries, mutations, and subscriptions
   - Created database migrations to transition schema
   - Updated Analytics page to use cities instead of ZIP codes
   - PR branch: feature/gym-search-with-progress

### Current Task: UI Redesign
- Ready to begin UI/UX improvements
- Focus areas to be determined

### Environment URLs:
| Environment | Frontend | Backend | Branch |
|------------|----------|---------|--------|
| Development | http://localhost:3000 | http://localhost:8000 | feature/* |
| Staging | https://gymintel-web-staging.vercel.app | https://gymintel-backend-staging.railway.app | staging |
| Production | https://gymintel-web.vercel.app | https://gymintel-backend.railway.app | main |

### Deployment Flow:
```mermaid
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
- `/backend/app/services/city_boundaries.py` - PostGIS city boundary queries
- `/backend/app/services/google_places.py` - Google Places API integration
- `/frontend/src/components/SearchInputMUISimple.tsx` - Material-UI autocomplete
- `/backend/migrations/versions/*` - Database migration files
- `/docs/GOOGLE_PLACES_SETUP.md` - Google Places API setup guide

### Key Technical Implementations:
1. **PostGIS Integration**: Using spatial queries for accurate city boundary searches
2. **Google Places API**: Autocomplete and validation for city names
3. **Material-UI Components**: Professional autocomplete UI with debouncing
4. **Database Migrations**: Smooth transition from ZIP code to location-based schema
5. **GraphQL Schema Evolution**: Complete type system update for location-based search

### Next Steps for UI Redesign:
1. Define design system and component library
2. Create mockups for key pages (Search, Results, Analytics)
3. Implement responsive layouts
4. Add animations and transitions
5. Improve data visualization components
