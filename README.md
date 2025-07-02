# GymIntel Web Application 🏋️‍♂️🌐

A comprehensive **web-based gym discovery platform** with interactive maps, data visualization, and persistent storage. Built with **GraphQL, FastAPI, React, and PostgreSQL**.

> **🔗 Related Projects**: This is the web application version of [GymIntel CLI](https://github.com/a-deal/gymintel-cli), which provides the stable command-line interface.

## 🎯 Project Vision

Transform gym discovery from a command-line tool into a powerful web platform with:
- **Interactive Maps**: Real-time gym locations with confidence score overlays
- **Data Visualization**: Charts, heatmaps, and trend analysis
- **Business Intelligence**: Market analytics, competitor mapping, demographic insights
- **GraphQL API**: Flexible, type-safe data access
- **Real-time Updates**: Live gym data with change notifications

## 🏗️ Architecture Overview

### **Tech Stack**
- **Backend**: FastAPI + Strawberry GraphQL
- **Frontend**: React + Apollo Client + TypeScript
- **Database**: PostgreSQL + PostGIS (geospatial queries)
- **Maps**: Mapbox GL JS / React Map GL
- **Deployment**: Railway (backend) + Vercel (frontend)

### **Project Structure**
```
gymintel-web/
├── backend/                    # FastAPI + GraphQL backend
│   ├── app/
│   │   ├── graphql/           # GraphQL schema & resolvers
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic (imported from CLI)
│   │   └── main.py            # FastAPI app entry point
│   ├── migrations/            # Alembic database migrations
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── graphql/           # GraphQL queries & mutations
│   │   ├── pages/             # Page components
│   │   └── App.tsx            # Main app component
│   ├── package.json           # Node.js dependencies
│   └── vite.config.ts         # Vite build config
├── shared/                    # Shared types & utilities
├── docker/                    # Docker configuration files
│   └── docker-compose.yml     # Local development environment
├── scripts/                   # Development and utility scripts
└── docs/                      # Documentation files
```

## 🎨 GraphQL Schema Design

### **Core Types**
```graphql
type Gym {
  id: ID!
  name: String!
  address: String!
  coordinates: Coordinates!
  phone: String
  website: String
  rating: Float
  reviewCount: Int
  sources: [DataSource!]!
  confidence: Float!
  metropolitanArea: MetropolitanArea
  createdAt: DateTime!
  updatedAt: DateTime!
}

type MetropolitanArea {
  id: ID!
  name: String!
  code: String!
  zipCodes: [String!]!
  gyms(limit: Int, offset: Int): [Gym!]!
  statistics: MetroStatistics!
}

type Query {
  # Single gym search
  searchGyms(
    zipcode: String!
    radius: Float = 10
    limit: Int = 50
  ): SearchResult!

  # Metropolitan area queries
  metropolitanArea(code: String!): MetropolitanArea
  listMetropolitanAreas: [MetropolitanArea!]!

  # Analytics queries
  gymAnalytics(zipcode: String!): GymAnalytics!
  marketGapAnalysis(zipcode: String!): [MarketGap!]!
}

type Mutation {
  # Import data from CLI
  importGymData(zipcode: String!, data: GymDataInput!): ImportResult!

  # User preferences
  saveSearch(zipcode: String!, radius: Float): SavedSearch!
}

type Subscription {
  # Real-time updates
  gymUpdates(zipcode: String!): Gym!
  searchProgress(searchId: String!): SearchProgress!
}
```

## 🚀 Development Phases

### **Phase 3: Business Intelligence & Visualization** (Q1 2025)
- [x] Repository setup with GraphQL architecture
- [ ] Database schema with PostGIS extensions
- [ ] Core GraphQL API with gym queries
- [ ] Interactive map component with Mapbox
- [ ] Data import from CLI tool
- [ ] Basic search and filtering UI
- [ ] Confidence score visualization

### **Phase 4: Web Platform Features** (Q2 2025)
- [ ] User authentication and accounts
- [ ] Saved searches and preferences
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile-responsive PWA
- [ ] API rate limiting and caching

## 🔧 Development Setup

### **Prerequisites**
- Node.js 18+ and npm/yarn
- Python 3.9+ and pip
- PostgreSQL 14+ with PostGIS extension
- Docker (optional, for local development)

### **Quick Start**
```bash
# Clone the repository
git clone https://github.com/a-deal/gymintel-web.git
cd gymintel-web

# Start with Docker (recommended)
docker-compose -f docker/docker-compose.yml up -d

# Or setup manually:

# Backend setup
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### **Environment Variables**
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost/gymintel  # pragma: allowlist secret
YELP_API_KEY=your_yelp_key
GOOGLE_PLACES_API_KEY=your_google_key
MAPBOX_ACCESS_TOKEN=your_mapbox_token

# Frontend (.env.local)
VITE_GRAPHQL_ENDPOINT=http://localhost:8000/graphql
VITE_MAPBOX_ACCESS_TOKEN=your_mapbox_token
```

## 📊 Data Migration Strategy

### **CLI Integration**
The web app leverages the stable [GymIntel CLI](https://github.com/a-deal/gymintel-cli) for data collection:

1. **Shared Services**: Import confidence scoring and API services from CLI
2. **Batch Processing**: Use CLI's metropolitan area processing for initial data seeding
3. **Real-time Sync**: GraphQL mutations to import fresh CLI search results
4. **Export Bridge**: CLI's JSON export format directly imports to PostgreSQL

### **Migration Command**
```bash
# Import CLI data to web database
python backend/cli_importer.py --metro nyc --import-to-db

# Real-time sync during development
python backend/sync_cli_data.py --watch --zipcode 10001
```

## 🗺️ Interactive Features

### **Map Visualization**
- **Gym Markers**: Color-coded by confidence score
- **Heat Maps**: Gym density visualization
- **Metro Boundaries**: Shaded metropolitan area zones
- **Clustering**: Automatic marker clustering at zoom levels

### **Analytics Dashboard**
- **Market Analysis**: Gym distribution charts
- **Confidence Trends**: Score distribution graphs
- **Competitor Mapping**: Proximity analysis
- **Demographics**: Population vs gym density

### **Real-time Features**
- **Live Search**: Results update as you type
- **Progress Tracking**: Visual feedback for long searches
- **Change Notifications**: New gyms or data updates

## 🔗 API Documentation

GraphQL schema and API documentation will be available at:
- **GraphQL Playground**: http://localhost:8000/graphql
- **Schema Documentation**: Auto-generated from type definitions
- **API Reference**: Interactive query builder

## 🤝 Contributing

This project follows the same contribution guidelines as the [GymIntel CLI](https://github.com/a-deal/gymintel-cli/blob/main/docs/CONTRIBUTING.md).

### **Development Workflow**
1. Create feature branch from `main`
2. Develop using local Docker environment
3. Test GraphQL queries in playground
4. Submit PR with GraphQL schema changes documented

### **Code Organization**
- **Backend**: Follow FastAPI + SQLAlchemy patterns
- **Frontend**: React functional components with TypeScript
- **GraphQL**: Type-first schema development
- **Testing**: Jest (frontend) + pytest (backend)

## 📈 Performance Targets

- **Initial Load**: < 2 seconds
- **GraphQL Queries**: < 500ms average
- **Map Rendering**: < 1 second for 1000+ markers
- **Database Queries**: < 100ms with proper indexing

## 🌐 Deployment Strategy

### **Production Architecture**
- **Frontend**: Vercel (CDN + edge functions)
- **Backend**: Railway (PostgreSQL + FastAPI)
- **Database**: Railway PostgreSQL with PostGIS
- **File Storage**: Railway volumes for cached data

### **Cost Optimization**
- **Railway**: $5/month PostgreSQL + $5/month backend
- **Vercel**: Free tier for frontend
- **Total**: ~$10/month for production deployment

---

## 🤝 Project Ecosystem

| Project | Purpose | Status | Best For |
|---------|---------|--------|----------|
| **[GymIntel CLI](https://github.com/a-deal/gymintel-cli)** | Command-line tool | ✅ Production | Scripts, automation, developers |
| **[GymIntel-Web](https://github.com/a-deal/gymintel-web)** | Web application | 🚧 Development | Business users, visualization, analysis |

**GymIntel Web** - *Comprehensive gym intelligence through interactive visualization* 🏋️‍♂️🌐✨

**License**: MIT | **Status**: In Development | **Target**: Q1-Q2 2025
