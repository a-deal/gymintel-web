# GymIntel Backend

FastAPI + GraphQL backend for the GymIntel web application.

## Setup

### Requirements
- Python 3.9+
- PostgreSQL 15+ with PostGIS extension
- Redis (optional, for caching)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
# Create database
createdb gymintel

# Install PostGIS extension
psql -d gymintel -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Run migrations
alembic upgrade head
```

## Testing

Tests require PostgreSQL with PostGIS extension.

### Setup Test Database

```bash
# One-time setup
./scripts/setup_test_db.sh

# Or manually:
createdb test_gymintel
psql -d test_gymintel -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

### Test Configuration

Tests use PostgreSQL by default. Configure with environment variables:

```bash
# Use custom test database with environment variables
TEST_DATABASE_USER=myuser TEST_DATABASE_PASSWORD=mypass pytest

# Or set in .env file
cp ../.env.example ../.env
# Edit .env with your test database credentials
pytest
```

## Development

```bash
# Run development server
uvicorn app.main:app --reload

# Access endpoints:
# - API: http://localhost:8000
# - GraphQL Playground: http://localhost:8000/graphql
# - OpenAPI Docs: http://localhost:8000/docs
```

## Docker

```bash
# Build image
docker build -t gymintel-backend .

# Run with docker-compose (recommended)
cd .. && docker-compose up backend
```
