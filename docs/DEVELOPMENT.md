# GymIntel Web Development Guide

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (or Docker Engine + Docker Compose)
- Git

### Start Development Environment
```bash
# Clean up any previous processes
./cleanup.sh

# Start the full Docker environment
./dev-start.sh
```

### Your Application URLs
- **Frontend**: http://localhost:3000
- **GraphQL Playground**: http://localhost:8000/graphql
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🐳 Docker Setup

### Development Files
- `docker-compose.yml` - Development orchestration
- `backend/Dockerfile.dev` - Backend development container
- `frontend/Dockerfile.dev` - Frontend development container

### Production Files  
- `docker-compose.prod.yml` - Production orchestration
- `backend/Dockerfile` - Backend production container
- `frontend/Dockerfile` - Frontend production container

### Services
- **PostgreSQL**: Database with PostGIS extensions
- **Backend**: FastAPI + GraphQL API
- **Frontend**: React + Tailwind UI
- **Redis**: Caching and real-time features

## 🛠️ Development Commands

### Docker Operations
```bash
# Start everything
./dev-start.sh

# Clean up processes and ports
./cleanup.sh

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database

# Stop everything
docker-compose down

# Restart a service
docker-compose restart backend
docker-compose restart frontend

# Shell access
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec database psql -U gymintel -d gymintel
```

### Manual Development (if needed)
```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend  
cd frontend
npm run dev
```

## 🎨 Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework
- **Strawberry GraphQL**: GraphQL implementation
- **SQLAlchemy**: ORM with PostgreSQL + PostGIS
- **Alembic**: Database migrations
- **CLI Bridge**: Integration with gymintel-cli

### Frontend Stack
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **Tailwind UI**: Professional components
- **Apollo Client**: GraphQL client
- **React Map GL**: Mapbox integration
- **Recharts**: Data visualization

### Typography
- **Headings**: JetBrains Mono
- **Body Text**: System monospace
- **Developer-focused**: Clean, technical aesthetic

## 📁 Project Structure

```
gymintel-web/
├── backend/                    # FastAPI + GraphQL API
│   ├── app/
│   │   ├── graphql/           # Schema & resolvers
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic
│   │   └── main.py            # FastAPI app
│   ├── Dockerfile             # Production container
│   ├── Dockerfile.dev         # Development container
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React + TypeScript
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── pages/             # Page components
│   │   ├── graphql/           # GraphQL queries
│   │   └── types/             # TypeScript types
│   ├── Dockerfile             # Production container
│   ├── Dockerfile.dev         # Development container
│   └── package.json           # Node dependencies
├── docker-compose.yml         # Development orchestration
├── docker-compose.prod.yml    # Production orchestration
├── dev-start.sh              # Start development
├── cleanup.sh                # Clean up processes
└── DEVELOPMENT.md            # This guide
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```env
# API Keys (optional for basic development)
YELP_API_KEY=your-yelp-api-key
GOOGLE_PLACES_API_KEY=your-google-places-api-key

# Mapbox (optional - maps show fallback without token)
MAPBOX_ACCESS_TOKEN=your-mapbox-token

# Database (handled by Docker)
DATABASE_URL=postgresql://gymintel:gymintel_dev@database:5432/gymintel
```

### Frontend Configuration
In `frontend/.env`:
```env
VITE_GRAPHQL_ENDPOINT=http://localhost:8000/graphql
VITE_GRAPHQL_WS_ENDPOINT=ws://localhost:8000/graphql
VITE_MAPBOX_ACCESS_TOKEN=your-mapbox-token
```

## 🧪 Testing GraphQL

### Sample Queries
```graphql
# List metropolitan areas
query {
  listMetropolitanAreas {
    name
    code
    state
    zipCodes
  }
}

# Search gyms
query {
  searchGyms(zipcode: "10001", radius: 10) {
    totalResults
    gyms {
      name
      address
      confidence
      rating
    }
  }
}

# Get gym analytics
query {
  gymAnalytics(zipcode: "10001") {
    totalGyms
    marketSaturation
    densityScore
  }
}
```

## 🔄 Development Workflow

1. **Start Environment**: `./dev-start.sh`
2. **Make Changes**: Edit code (auto-reloads)
3. **Test API**: Use GraphQL playground
4. **View Frontend**: Check http://localhost:3000
5. **Debug**: Use `docker-compose logs -f [service]`
6. **Commit**: Changes are auto-saved in containers

## 🚢 Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production stack
docker-compose -f docker-compose.prod.yml up -d
```

## 🐛 Troubleshooting

### Port Conflicts
```bash
# Clean up everything
./cleanup.sh

# Check port usage
lsof -i :3000
lsof -i :8000
```

### Container Issues
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# Reset everything
docker-compose down -v
docker system prune -f
```

### Database Issues
```bash
# Access database
docker-compose exec database psql -U gymintel -d gymintel

# Reset database
docker-compose down
docker volume rm gymintel-web_postgres_data
docker-compose up -d
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Apollo Client](https://www.apollographql.com/docs/react/)
- [Docker Compose](https://docs.docker.com/compose/)

## 🏋️ Happy Development!

Your GymIntel web application is ready for development with:
- ✅ JetBrains Mono typography
- ✅ Tailwind UI components  
- ✅ GraphQL API with playground
- ✅ Hot reload for both frontend and backend
- ✅ PostgreSQL with PostGIS
- ✅ Professional developer experience