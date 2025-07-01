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
└── docker-compose.yml         # Local development environment
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

**Phase 3B Progress**: ✅ 80% Complete
- React components with Tailwind CSS + Tailwind UI
- Professional UI components (GymCard, SearchFilters, Layout)
- Complete page structure (HomePage, SearchPage, AnalyticsPage, MetroPage)
- GraphQL integration working
- Docker development environment configured
- JetBrains Mono typography implemented
- Comprehensive development documentation

**Next Priorities**:
1. **Start Development Environment** - Run `./dev-start.sh` to launch Docker containers
2. **Integrate Mapbox GL JS** - Add interactive maps to SearchPage
3. **Implement Real-time Features** - GraphQL subscriptions for live updates
4. **Test CLI Data Pipeline** - Import gym data from gymintel-cli
5. **Add API Keys** - Configure Yelp/Google Places/Mapbox tokens
6. **Database Seeding** - Populate with initial metro area data
7. **Error Handling** - Add comprehensive error boundaries and loading states

## Development Environment Setup

### **One-Command Start (Recommended)**
```bash
# Clean any previous processes
./cleanup.sh

# Start full Docker environment with hot reload
./dev-start.sh

# Access applications
# Frontend: http://localhost:3000
# GraphQL Playground: http://localhost:8000/graphql
# API Docs: http://localhost:8000/docs
```

### **Manual Development (Alternative)**
```bash
# Backend development
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend development (new terminal)
cd frontend
npm install
npm run dev

# Database migrations
cd backend
alembic upgrade head
```

### **Environment Configuration**
```bash
# Create .env file with API keys (optional for basic development)
cp .env.example .env

# Required for maps (optional - fallback available)
MAPBOX_ACCESS_TOKEN=your-mapbox-token

# Required for CLI integration (optional for UI development)
YELP_API_KEY=your-yelp-api-key
GOOGLE_PLACES_API_KEY=your-google-places-api-key
```

### **Development URLs**
- **Frontend App**: http://localhost:3000
- **GraphQL Playground**: http://localhost:8000/graphql  
- **API Documentation**: http://localhost:8000/docs
- **Database Admin**: http://localhost:8080 (pgAdmin via Docker)

This context helps AI assistants understand the sophisticated architecture, current development status, and implementation priorities for the GymIntel Web Application.