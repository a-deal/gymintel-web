#!/bin/bash
# Test database management script

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project root (two levels up from scripts directory)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

case "$1" in
  start)
    echo -e "${GREEN}Starting test database...${NC}"
    cd "$PROJECT_ROOT"
    docker compose -f docker/docker-compose.test.yml up -d
    echo -e "${GREEN}Waiting for database to be ready...${NC}"
    sleep 5
    echo -e "${GREEN}Test database is running on localhost:5432${NC}"
    ;;

  stop)
    echo -e "${YELLOW}Stopping test database...${NC}"
    cd "$PROJECT_ROOT"
    docker compose -f docker/docker-compose.test.yml down
    echo -e "${GREEN}Test database stopped${NC}"
    ;;

  status)
    if docker ps | grep -q "gymintel-web-test-db"; then
      echo -e "${GREEN}Test database is running${NC}"
      docker ps | grep "gymintel-web-test-db"
    else
      echo -e "${RED}Test database is not running${NC}"
      echo "Run './test-db.sh start' to start it"
    fi
    ;;

  logs)
    docker logs gymintel-web-test-db-1 -f
    ;;

  test)
    # Run tests
    if docker ps | grep -q "gymintel-web-test-db"; then
      echo -e "${GREEN}Running all backend tests...${NC}"
      cd "$PROJECT_ROOT/backend"
      python3 -m pytest tests/ -v
    else
      echo -e "${RED}Test database is not running!${NC}"
      echo -e "${YELLOW}Running only non-database tests...${NC}"
      cd "$PROJECT_ROOT/backend"
      python3 -m pytest -m "not database" -v
    fi
    ;;

  *)
    echo "Usage: $0 {start|stop|status|logs|test}"
    echo "  start  - Start the test database"
    echo "  stop   - Stop the test database"
    echo "  status - Check if test database is running"
    echo "  logs   - View test database logs"
    echo "  test   - Run backend tests"
    exit 1
    ;;
esac
