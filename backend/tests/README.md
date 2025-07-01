# Backend Testing Guide

## Test Database Configuration

The backend tests have been updated to use PostgreSQL (matching production) instead of SQLite.

### Why PostgreSQL for Tests?

1. **Feature Parity**: Our models use PostgreSQL-specific features:
   - UUID type for primary keys
   - PostGIS geometry types for location data
   - JSONB for flexible data storage

2. **Realistic Testing**: Testing with the same database as production catches issues early

3. **No Compatibility Hacks**: Avoid complex mocking and patching

### Setup Options

#### Option 1: Local PostgreSQL (Recommended)

```bash
# Install PostgreSQL with PostGIS
# macOS:
brew install postgresql postgis
brew services start postgresql

# Ubuntu/Debian:
sudo apt install postgresql postgresql-contrib postgis

# Create test database
./scripts/setup_test_db.sh
```

#### Option 2: Docker PostgreSQL

```bash
# Run PostgreSQL with PostGIS in Docker
docker run -d \
  --name test-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=test_gymintel \
  -p 5432:5432 \
  postgis/postgis:15-3.3

# Wait for it to start
sleep 5

# Create PostGIS extension
docker exec test-postgres psql -U postgres -d test_gymintel -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

#### Option 3: Use Docker Compose

```bash
# From project root, run test services
docker-compose -f docker-compose.test.yml up -d
```

### Running Tests

```bash
# With local PostgreSQL running:
pytest

# With custom database credentials:
TEST_DATABASE_USER=myuser TEST_DATABASE_PASSWORD=mypass pytest

# Skip database tests if PostgreSQL not available:
pytest -m "not database"
```

### CI/CD

GitHub Actions already uses PostgreSQL service for tests. No changes needed.

### Fallback for Quick Testing

If you need to run tests without PostgreSQL, you can mark database-dependent tests:

```python
@pytest.mark.database
async def test_database_operation():
    # This test requires PostgreSQL
    pass

def test_simple_logic():
    # This test runs without database
    pass
```

Then run non-database tests with: `pytest -m "not database"`
