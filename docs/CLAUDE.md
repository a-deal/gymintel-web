# CLAUDE.md - GymIntel Web Application Context

This file provides context for AI assistants (like Claude) working on the GymIntel Web Application - an advanced gym discovery platform with GraphQL API, interactive maps, and business intelligence.

## Project Overview

GymIntel Web is the **Phase 3 evolution** of the GymIntel project, transforming from a CLI tool into a comprehensive web platform. This represents the "business intelligence & visualization" phase with persistent storage, interactive maps, and advanced analytics.

## Architecture

### **Tech Stack**
- **Backend**: FastAPI + Strawberry GraphQL + Python 3.9+
- **Frontend**: React + TypeScript + Apollo Client + Vite
- **Database**: PostgreSQL 15+ with PostGIS extension
- **Maps**: Mapbox GL JS / React Map GL
- **Real-time**: GraphQL subscriptions via WebSockets
- **Deployment**: Railway (backend) + Vercel (frontend)

### **Project Structure**
```
gymintel-web/
├── backend/                    # FastAPI + GraphQL API
│   ├── app/
│   │   ├── graphql/           # Schema, resolvers, subscriptions
│   │   ├── models/            # SQLAlchemy + PostGIS models
│   │   ├── services/          # Business logic & CLI bridge
│   │   └── main.py            # FastAPI application
│   ├── migrations/            # Alembic database migrations
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React + TypeScript app
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── graphql/           # GraphQL queries/mutations
│   │   ├── pages/             # Page-level components
│   │   └── App.tsx            # Main application
│   └── package.json           # Node.js dependencies
├── shared/                    # Shared types & utilities
├── docker/                    # Docker configuration files
│   └── docker-compose.yml     # Local development environment
├── scripts/                   # Development and utility scripts
└── docs/                      # Documentation files
```

## Key Features & Design

### **1. GraphQL-First Architecture**
- **15+ Types**: Comprehensive schema for gym intelligence
- **Real-time Subscriptions**: Live gym updates, search progress
- **Type Safety**: End-to-end TypeScript + GraphQL codegen
- **Flexible Queries**: Frontend requests exactly what it needs

### **2. Geospatial Intelligence**
- **PostGIS Integration**: Advanced geographic queries
- **Interactive Maps**: Mapbox GL with confidence score overlays
- **Clustering**: Automatic marker grouping at different zoom levels
- **Heat Maps**: Gym density visualization

### **3. CLI Integration Bridge**
- **Data Import**: Seamless integration with gymintel-cli tool
- **Shared Services**: Reuse confidence scoring algorithms
- **Real-time Sync**: GraphQL mutations for fresh CLI data
- **Migration Path**: JSON export → PostgreSQL import

### **4. Business Intelligence**
- **Market Analytics**: Gap analysis, competitor mapping
- **Confidence Visualization**: Interactive confidence score displays
- **Demographic Insights**: Population vs gym density analysis
- **Trend Analysis**: Historical data patterns

## GraphQL Schema Highlights

### **Core Types**
```graphql
type Gym {
  id: ID!
  name: String!
  address: String!
  coordinates: Coordinates!
  confidence: Float!           # 0.0-1.0 confidence score
  sources: [DataSource!]!     # Multi-source tracking
  metropolitanArea: MetropolitanArea
}

type Query {
  searchGyms(zipcode: String!, radius: Float): SearchResult!
  metropolitanArea(code: String!): MetropolitanArea
  gymAnalytics(zipcode: String!): GymAnalytics!
  marketGapAnalysis(zipcode: String!): [MarketGap!]!
}

type Subscription {
  gymUpdates(zipcode: String!): Gym!
  searchProgress(searchId: String!): SearchProgress!
}
```

## Development Phases

### **✅ Phase 3A: Foundation** (Completed)
- [x] Repository setup with professional architecture
- [x] GraphQL schema design (15+ types)
- [x] FastAPI + Strawberry GraphQL backend structure
- [x] PostgreSQL + PostGIS database models
- [x] CLI bridge service for data integration
- [x] Docker Compose development environment
- [x] Database migrations with Alembic
- [x] Basic GraphQL resolvers implementation
- [x] Apollo Client frontend setup

### **🚧 Phase 3B: Core Features** (In Progress)
- [x] React components with Tailwind CSS styling
- [x] HomePage with hero section and feature overview
- [x] SearchPage with filters and dual view modes
- [x] Layout component with sidebar navigation
- [ ] Interactive map component with Mapbox
- [ ] Real-time gym search with progress tracking
- [ ] Confidence score visualization
- [ ] Basic analytics dashboard
- [ ] CLI data import functionality

### **🎯 Phase 3C: Business Intelligence** (Q1 2025)
- [ ] Advanced filtering and search
- [ ] Market gap analysis algorithms
- [ ] Competitor proximity mapping
- [ ] Demographics integration
- [ ] Export capabilities for analysis
- [ ] Real-time notifications

### **🚀 Phase 4: Web Platform** (Q2 2025)
- [ ] User accounts and saved searches
- [ ] API rate limiting and caching
- [ ] Mobile PWA optimization
- [ ] Advanced visualization (heatmaps, charts)
- [ ] Machine learning recommendations
- [ ] Public API endpoints

## Key Implementation Details

### **CLI Integration Strategy**
```python
# Import CLI services directly
from cli_services.run_gym_search import run_gym_search
from cli_services.metro_areas import get_metro_area

# Bridge service transforms CLI → GraphQL
class CLIBridgeService:
    async def search_gyms_via_cli(zipcode: str) -> Dict:
        cli_result = await run_gym_search(zipcode, quiet=True)
        return transform_to_graphql_format(cli_result)
```

### **Database Design**
- **Gyms Table**: Core gym data with PostGIS POINT geometry
- **DataSources Table**: Multi-source tracking (Yelp, Google, Merged)
- **Reviews Table**: Aggregated review data with sentiment
- **MetropolitanAreas Table**: Geographic boundaries and metadata

### **Real-time Features**
- **GraphQL Subscriptions**: WebSocket connections for live updates
- **Search Progress**: Real-time feedback for long-running searches
- **Data Changes**: Live notifications when gym data updates

## Performance Considerations

### **Database Optimization**
- **PostGIS Indexes**: Spatial indexes on gym locations
- **Query Optimization**: Efficient radius-based searches
- **Connection Pooling**: SQLAlchemy async connection management

### **Frontend Performance**
- **Map Clustering**: Handle 1000+ markers efficiently
- **Apollo Caching**: Smart GraphQL query caching
- **Code Splitting**: Lazy load map components
- **Image Optimization**: Optimized marker icons

### **API Design**
- **Pagination**: Limit large result sets
- **Field Selection**: GraphQL eliminates over-fetching
- **Caching**: Redis for expensive operations
- **Rate Limiting**: Protect against abuse

## Development Guidelines

### **GraphQL Best Practices**
1. **Type-First Development**: Define schema before implementation
2. **Resolver Efficiency**: Avoid N+1 queries with DataLoader
3. **Error Handling**: Comprehensive GraphQL error responses
4. **Testing**: Schema validation and resolver testing

### **Database Guidelines**
1. **Migrations**: Use Alembic for schema changes
2. **Relationships**: Proper foreign key constraints
3. **Indexing**: Optimize for geographic queries
4. **Data Types**: Use appropriate PostGIS geometry types

### **Frontend Architecture**
1. **Component Organization**: Feature-based folder structure
2. **State Management**: Apollo Cache + Zustand for UI state
3. **Styling**: Tailwind CSS for rapid, consistent UI development
4. **Type Safety**: GraphQL codegen for TypeScript types
5. **Testing**: Component testing with Testing Library

## Common Development Tasks

### **Adding New GraphQL Types**
1. Define in `backend/app/graphql/schema.py`
2. Create SQLAlchemy model in `backend/app/models/`
3. Implement resolver logic
4. Update frontend GraphQL queries
5. Generate TypeScript types

### **Map Feature Development**
1. Create React component in `frontend/src/components/map/`
2. Integrate with Mapbox GL JS
3. Add GraphQL queries for geographic data
4. Implement clustering and filtering
5. Test across different zoom levels

### **CLI Integration**
1. Import CLI services in `backend/app/services/cli_bridge.py`
2. Transform CLI data format to GraphQL schema
3. Create GraphQL mutations for import
4. Add error handling and progress tracking
5. Test with various CLI outputs

## Related Projects

- **[GymIntel CLI](https://github.com/a-deal/gymintel-cli)**: Stable command-line tool (data source)
- **Shared Algorithms**: Confidence scoring, deduplication, API services
- **Data Flow**: CLI exports → Web app imports → Enhanced visualization

## Current Status

**Phase 3A Progress**: ✅ 100% Complete
- GraphQL schema designed and documented
- FastAPI backend architecture established
- PostgreSQL + PostGIS models defined
- CLI bridge service implemented
- Docker development environment ready
- GraphQL resolvers implemented
- Database migrations configured
- Apollo Client setup complete

**Phase 3B Progress**: ✅ 60% Complete
- React components with Tailwind CSS
- Layout and navigation structure
- HomePage and SearchPage implemented
- GraphQL integration working

**Next Priorities**:
1. Complete remaining UI components (GymCard, SearchFilters, MapView)
2. Integrate Mapbox GL JS for interactive maps
3. Add AnalyticsPage and MetroPage
4. Test CLI data import pipeline
5. Add error handling and loading states

## Development Environment Setup

### **Hybrid Approach: Docker + Local Tooling**

We use a **hybrid development strategy** that combines the best of both worlds:

- **🐳 Docker-first**: Primary development environment (database, services, runtime)
- **🔧 Local tooling**: Code quality tools (linting, formatting, type checking, pre-commit hooks)

This approach ensures:
✅ Consistent runtime environment across all developers
✅ Fast, reliable linting and formatting in editors
✅ Pre-commit hooks work without Docker overhead
✅ TypeScript/ESLint work seamlessly in IDEs

### **Quick Setup**

**Option A: Local Tooling (Recommended)**
```bash
# 1. Setup local development tooling with nvm + Node 18 (one-time)
./setup-local-dev.sh

# 2. For new terminals, ensure Node 18 is active
nvm use 18  # or add to your shell profile

# 3. Start Docker development environment
./scripts/dev-start.sh
```

**Option B: Docker-Only (Alternative)**
```bash
# 1. Use Docker-based pre-commit hooks (if local setup problematic)
ln -sf .pre-commit-config-docker.yaml .pre-commit-config.yaml
source backend/venv/bin/activate && pre-commit install

# 2. Start Docker development environment
./scripts/dev-start.sh

# 3. Run manual linting via Docker
./scripts/precommit-docker.sh
```

**Access Applications:**
- Frontend: http://localhost:3000
- GraphQL Playground: http://localhost:8000/graphql
- API Docs: http://localhost:8000/docs

### **Manual Development Commands**

```bash
# Docker development (recommended)
./scripts/dev-start.sh                 # Start full environment
./scripts/cleanup.sh                   # Stop and cleanup

# Local linting/formatting
cd frontend
npx eslint . --ext ts,tsx      # Lint TypeScript
npx prettier --write .         # Format code
npx tsc --noEmit               # Type check

cd backend
source venv/bin/activate
black .                        # Format Python
isort .                        # Sort imports
flake8 .                       # Lint Python

# Database migrations
cd backend
alembic upgrade head           # Apply migrations
alembic revision --autogenerate -m "description"  # Create migration

# Manual service startup (alternative to Docker)
cd backend && source venv/bin/activate && uvicorn app.main:app --reload
cd frontend && npm run dev
```

### **Code Quality Tools**

Pre-commit hooks automatically run:
- **Python**: Black formatting, isort imports, flake8 linting
- **Frontend**: ESLint, Prettier, TypeScript checking
- **Security**: detect-secrets scanning
- **General**: trailing whitespace, YAML/JSON validation

**Local Setup Commands:**
```bash
# Manual pre-commit run (local)
pre-commit run --all-files

# Manual linting (local with Node 18)
nvm use 18
cd frontend && npx eslint . --ext ts,tsx
cd frontend && npx prettier --check .
cd frontend && npx tsc --noEmit
```

**Docker Setup Commands:**
```bash
# Manual pre-commit run (Docker)
./scripts/precommit-docker.sh

# Switch between local and Docker pre-commit
ln -sf .pre-commit-config.yaml .pre-commit-config.yaml      # Local
ln -sf .pre-commit-config-docker.yaml .pre-commit-config.yaml  # Docker
```

**Emergency Commands:**
```bash
# Skip hooks for urgent commits (use sparingly)
git commit --no-verify

# Reset to working pre-commit setup
rm .pre-commit-config.yaml && ln -sf .pre-commit-config.yaml .pre-commit-config.yaml
```

This context helps AI assistants understand the sophisticated architecture, current development status, and implementation priorities for the GymIntel Web Application.

## Current Deployment Status (July 2, 2025)

### Completed Work:
- ✅ **CI/CD Pipeline Fixed**:
  - Backend tests now use PostGIS image (fixes geometry type errors)
  - Frontend tests fixed (Router nesting, GymCard component tests)
  - Docker-based test scripts for both backend and frontend

- ✅ **Project Organization**:
  - Docker files moved to `docker/`
  - Documentation moved to `docs/`
  - Shell scripts moved to `scripts/`
  - All file references updated

- ✅ **Vercel Configuration**:
  - Created `frontend/vercel.json` with Vite settings
  - Created `frontend/.vercelignore`
  - Updated deploy workflow
  - Created comprehensive setup documentation

### Current Blockers:
- ⏳ **Vercel Deployment** - Missing GitHub secrets:
  - `VERCEL_TOKEN`
  - `VERCEL_ORG_ID`
  - `VERCEL_PROJECT_ID`

### Next Steps to Resume:

1. **Complete Vercel Setup**:
   ```bash
   cd frontend
   npx vercel login         # Choose GitHub auth
   npx vercel whoami        # Copy the ID shown
   npx vercel              # Create/link project
   cat .vercel/project.json # Get projectId
   ```

2. **Create Vercel Token**:
   - Go to https://vercel.com/account/tokens
   - Create token named `gymintel-github-actions`

3. **Add GitHub Secrets**:
   - Go to repo Settings → Secrets → Actions
   - Add VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID

4. **Set Vercel Environment Variables**:
   - In Vercel Dashboard → Project Settings → Environment Variables
   - Add VITE_GRAPHQL_ENDPOINT and VITE_MAPBOX_ACCESS_TOKEN

### Files Created/Updated Today:
- `docs/DEPLOYMENT_SECRETS.md` - Lists all required secrets
- `docs/VERCEL_SETUP.md` - Detailed Vercel setup guide
- `frontend/nginx.conf` - For production Docker builds
- `frontend/vercel.json` - Vercel configuration
- `frontend/.vercelignore` - Files to exclude from deployment
- `frontend/scripts/test-docker.sh` - Docker-based frontend testing

All code is ready for deployment - just need the Vercel credentials!
