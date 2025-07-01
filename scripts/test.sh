#!/bin/bash

# GymIntel Web Test Runner
echo "🧪 GymIntel Web Test Suite"
echo "========================="
echo

# Function to run tests in containers
run_tests() {
    echo "🚀 Starting test environment..."
    
    # Stop any existing test containers
    docker compose -f docker-compose.test.yml down -v
    
    # Build and run test containers
    echo "📦 Building test containers..."
    docker compose -f docker-compose.test.yml build
    
    echo "🧪 Running backend tests..."
    docker compose -f docker-compose.test.yml run --rm backend-tests
    BACKEND_EXIT_CODE=$?
    
    echo "🧪 Running frontend tests..."
    docker compose -f docker-compose.test.yml run --rm frontend-tests
    FRONTEND_EXIT_CODE=$?
    
    # Cleanup
    echo "🧹 Cleaning up test environment..."
    docker compose -f docker-compose.test.yml down -v
    
    # Report results
    echo
    echo "📊 Test Results:"
    echo "==============="
    if [ $BACKEND_EXIT_CODE -eq 0 ]; then
        echo "✅ Backend tests: PASSED"
    else
        echo "❌ Backend tests: FAILED"
    fi
    
    if [ $FRONTEND_EXIT_CODE -eq 0 ]; then
        echo "✅ Frontend tests: PASSED"
    else
        echo "❌ Frontend tests: FAILED"
    fi
    
    # Exit with error if any tests failed
    if [ $BACKEND_EXIT_CODE -ne 0 ] || [ $FRONTEND_EXIT_CODE -ne 0 ]; then
        echo
        echo "❌ Some tests failed. Please check the output above."
        exit 1
    else
        echo
        echo "🎉 All tests passed!"
        exit 0
    fi
}

# Function to run tests locally (without Docker)
run_local_tests() {
    echo "🏠 Running tests locally..."
    echo
    
    # Backend tests
    echo "🐍 Running backend tests..."
    cd backend
    pytest --cov=app --cov-report=term-missing
    BACKEND_EXIT_CODE=$?
    cd ..
    
    # Frontend tests
    echo "⚛️ Running frontend tests..."
    cd frontend
    npm run test:coverage
    FRONTEND_EXIT_CODE=$?
    cd ..
    
    # Report results
    echo
    echo "📊 Test Results:"
    echo "==============="
    if [ $BACKEND_EXIT_CODE -eq 0 ]; then
        echo "✅ Backend tests: PASSED"
    else
        echo "❌ Backend tests: FAILED"
    fi
    
    if [ $FRONTEND_EXIT_CODE -eq 0 ]; then
        echo "✅ Frontend tests: PASSED"
    else
        echo "❌ Frontend tests: FAILED"
    fi
    
    # Exit with error if any tests failed
    if [ $BACKEND_EXIT_CODE -ne 0 ] || [ $FRONTEND_EXIT_CODE -ne 0 ]; then
        echo
        echo "❌ Some tests failed. Please check the output above."
        exit 1
    else
        echo
        echo "🎉 All tests passed!"
        exit 0
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -c, --container    Run tests in Docker containers (default)"
    echo "  -l, --local        Run tests locally (requires local setup)"
    echo "  -h, --help         Show this help message"
    echo
    echo "Examples:"
    echo "  $0                 # Run tests in containers"
    echo "  $0 --container     # Run tests in containers"
    echo "  $0 --local         # Run tests locally"
}

# Parse command line arguments
case "$1" in
    -l|--local)
        run_local_tests
        ;;
    -c|--container|"")
        run_tests
        ;;
    -h|--help)
        show_help
        ;;
    *)
        echo "❌ Unknown option: $1"
        echo
        show_help
        exit 1
        ;;
esac