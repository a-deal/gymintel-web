# Database Setup Guide

This guide explains how to set up the GymIntel database for both local development and production environments.

## Overview

GymIntel uses PostgreSQL with PostGIS extension for geographic data. The database schema includes:
- `gyms` - Main gym information with location data
- `data_sources` - External data sources (Yelp, Google Places)
- `reviews` - Aggregated reviews from various sources
- `metropolitan_areas` - Metro area definitions
- `users` - User accounts
- `saved_searches` - User saved searches

## Local Development Setup

### Option 1: Automatic Setup with Docker (Recommended)

The easiest way to set up the database locally is using Docker Compose with automatic initialization:

```bash
# From the project root
cd docker
docker-compose up -d
```

The database will be automatically initialized with:
- PostgreSQL with PostGIS extension
- All required tables
- Default development settings

The `AUTO_INIT_DB=true` environment variable ensures tables are created on first startup.

### Option 2: Manual Setup

If you prefer manual setup or need to reinitialize:

```bash
# Navigate to backend directory
cd backend

# Option A: Run the initialization script
python3 scripts/init_db.py

# Option B: Use Alembic migrations
alembic upgrade head

# Option C: Force recreate all tables (WARNING: Data loss!)
python3 scripts/init_db.py --force
```

### Option 3: Direct Database Creation

For testing or quick setup:

```python
# In a Python shell
from app.db_init import init_database
import asyncio

asyncio.run(init_database())
```

## Production Setup (Railway)

### Initial Deployment

1. **Add PostgreSQL Database in Railway**
   - Go to your Railway project
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set `DATABASE_URL`

2. **Enable PostGIS Extension**
   ```bash
   railway run psql -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```

3. **Run Database Migrations**
   ```bash
   railway run --service=backend-service cd backend && alembic upgrade head
   ```

### Automatic Initialization (Optional)

To enable automatic database initialization on deployment:

1. Add environment variable in Railway:
   ```
   AUTO_INIT_DB=true
   ```

2. The application will automatically create tables on startup if they don't exist

⚠️ **Note**: For production, it's recommended to run migrations manually rather than auto-initialization.

## Environment Variables

### Required Database Variables

```bash
# Local Development (.env)
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=gymintel
DATABASE_USER=gymintel
DATABASE_PASSWORD=gymintel_dev

# Production (Railway provides these)
DATABASE_URL=postgresql://user:pass@host:port/database  # pragma: allowlist secret
```

### Optional Initialization Variable

```bash
# Enable automatic database initialization
AUTO_INIT_DB=true  # Set to false in production after initial setup
```

## Troubleshooting

### "relation 'gyms' does not exist" Error

This error occurs when the database tables haven't been created. Solutions:

1. **Local Development**: Ensure `AUTO_INIT_DB=true` in docker-compose.yml
2. **Production**: Run migrations manually (see Production Setup above)
3. **Quick Fix**: Run `python3 scripts/init_db.py`

### PostGIS Extension Missing

If you see errors about geographic functions:

```sql
-- Connect to database and run:
CREATE EXTENSION IF NOT EXISTS postgis;
```

### Permission Errors

If you can't create the PostGIS extension:
- Local: Use the postgis/postgis Docker image (already configured)
- Production: Contact Railway support or use their PostgreSQL with PostGIS addon

## Database Schema

The database is defined using SQLAlchemy models in `backend/app/models/`:
- `gym.py` - Gym, DataSource, Review models
- `metro.py` - MetropolitanArea model
- `user.py` - User, SavedSearch models

## Migration Management

We use Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Best Practices

1. **Development**: Use `AUTO_INIT_DB=true` for convenience
2. **Production**:
   - Use Alembic migrations for schema changes
   - Set `AUTO_INIT_DB=false` after initial setup
   - Always backup before migrations
3. **Testing**: Each test creates its own schema using `create_tables()`

## Data Seeding

After setting up the database, you'll want to populate it with data:

1. **Development**: Use sample data for testing
   ```bash
   # Enable automatic seeding on startup
   SEED_DATABASE=true docker-compose up

   # Or manually seed
   cd backend && python scripts/seed_db.py
   ```

2. **Production**: Configure JIT (Just-In-Time) data fetching
   - Data is automatically fetched when users search
   - No need to pre-seed all zipcodes
   - See [Database Seeding Guide](./DATABASE_SEEDING.md) for details

3. **Import Existing Data**: Use CLI exports
   ```bash
   python scripts/seed_db.py --import-file exports/gyms_data.json
   ```

## Next Steps

1. **Seed the Database**: Follow the [Database Seeding Guide](./DATABASE_SEEDING.md)
2. **Test the Setup**: Run the test suite to verify everything works
3. **Start Development**: Launch the development environment
4. **Monitor Performance**: Use database tools to optimize queries

## Related Documentation

- [Database Seeding Guide](./DATABASE_SEEDING.md)
- [Railway Setup Guide](./RAILWAY_SETUP.md)
- [API Documentation](./backend/README.md)
- [Development Guide](./CONTRIBUTING.md)
