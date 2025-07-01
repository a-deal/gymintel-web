#!/bin/bash
# Setup test database for pytest

echo "Setting up test database..."

# Check if postgres is running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "PostgreSQL is not running. Please start PostgreSQL first."
    echo "On macOS: brew services start postgresql"
    echo "On Linux: sudo systemctl start postgresql"
    exit 1
fi

# Get database credentials from environment or use defaults
TEST_DB_NAME=${TEST_DATABASE_NAME:-test_gymintel}
TEST_DB_USER=${TEST_DATABASE_USER:-gymintel_test}
TEST_DB_PASSWORD=${TEST_DATABASE_PASSWORD:-gymintel_test}

# Create test user if it doesn't exist
createuser -s $TEST_DB_USER 2>/dev/null || echo "User $TEST_DB_USER already exists"

# Set password for test user
psql -c "ALTER USER $TEST_DB_USER WITH PASSWORD '$TEST_DB_PASSWORD';" 2>/dev/null

# Create test database
createdb -O $TEST_DB_USER $TEST_DB_NAME 2>/dev/null || echo "Database $TEST_DB_NAME already exists"

# Install PostGIS extension
psql -d $TEST_DB_NAME -c "CREATE EXTENSION IF NOT EXISTS postgis;" 2>/dev/null || {
    echo "Failed to create PostGIS extension. You may need to install PostGIS:"
    echo "On macOS: brew install postgis"
    echo "On Linux: sudo apt-get install postgresql-postgis"
}

echo "Test database setup complete!"
