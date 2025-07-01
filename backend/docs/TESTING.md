# Backend Testing Guide

## Quick Start

```bash
# Start test database
./scripts/test-db.sh start

# Run all tests
./scripts/test-db.sh test

# Stop test database
./scripts/test-db.sh stop
```

## Test Database Management

The `test-db.sh` script manages the PostgreSQL test database using Docker:

- **start** - Launches PostgreSQL with PostGIS in Docker
- **stop** - Stops and removes the test container
- **status** - Shows if the database is running
- **logs** - Shows database logs
- **test** - Runs tests (all if DB running, only non-DB tests if not)

## Running Tests Manually

### With Database (Full Test Suite)
```bash
# Ensure test database is running
./scripts/test-db.sh start

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### Without Database (Unit Tests Only)
```bash
# Run only non-database tests
pytest -m "not database"
```

## Test Categories

Tests are marked with pytest markers:

- `@pytest.mark.database` - Requires PostgreSQL database
- `@pytest.mark.unit` - Pure unit tests (no external dependencies)
- `@pytest.mark.integration` - Integration tests

## Continuous Integration

GitHub Actions automatically:
1. Spins up PostgreSQL service
2. Runs all tests including database tests
3. Reports coverage

## Pre-commit Hooks

Pre-commit only runs non-database tests to avoid requiring developers to have PostgreSQL running for every commit.

To run full test suite before pushing:
```bash
./scripts/test-db.sh test
```

## Troubleshooting

### Connection Refused
If tests fail with connection errors:
```bash
# Check if database is running
./scripts/test-db.sh status

# Start if needed
./scripts/test-db.sh start

# Check logs for issues
./scripts/test-db.sh logs
```

### Port Already in Use
If port 5432 is already in use:
```bash
# Stop any existing PostgreSQL
docker stop gymintel-web-test-db-1
docker rm gymintel-web-test-db-1

# Or use a different port in docker-compose.test.yml
```
