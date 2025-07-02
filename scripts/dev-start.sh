#!/bin/bash

# GymIntel Web Development Environment Starter
echo "🏋️ GymIntel Web Development Environment"
echo "======================================="
echo

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose -f ../docker/docker-compose.yml is available
if ! command -v docker-compose -f ../docker/docker-compose.yml &> /dev/null; then
    echo "❌ docker-compose -f ../docker/docker-compose.yml could not be found. Please install Docker Compose."
    exit 1
fi

echo "🔧 Starting GymIntel development environment..."
echo

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f ../docker/docker-compose.yml down

# Build and start services
echo "🚀 Building and starting services..."
docker-compose -f ../docker/docker-compose.yml up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
echo "=================="

# Check PostgreSQL
if docker-compose -f ../docker/docker-compose.yml ps postgres | grep -q "Up"; then
    echo "✅ PostgreSQL: Running"
else
    echo "❌ PostgreSQL: Not running"
fi

# Check Backend
if docker-compose -f ../docker/docker-compose.yml ps backend | grep -q "Up"; then
    echo "✅ Backend: Running"
else
    echo "❌ Backend: Not running"
fi

# Check Frontend
if docker-compose -f ../docker/docker-compose.yml ps frontend | grep -q "Up"; then
    echo "✅ Frontend: Running"
else
    echo "❌ Frontend: Not running"
fi

echo
echo "🌐 Your GymIntel Web Application is ready!"
echo "=========================================="
echo
echo "📍 Available URLs:"
echo "  • Frontend Application: http://localhost:3000"
echo "  • GraphQL Playground: http://localhost:8000/graphql"
echo "  • API Documentation: http://localhost:8000/docs"
echo "  • API Health Check: http://localhost:8000/health"
echo "  • PostgreSQL: localhost:5432"
echo
echo "🔧 Useful Commands:"
echo "  • View logs: docker-compose -f ../docker/docker-compose.yml logs -f [service]"
echo "  • Stop all: docker-compose -f ../docker/docker-compose.yml down"
echo "  • Restart: docker-compose -f ../docker/docker-compose.yml restart [service]"
echo "  • Shell access: docker-compose -f ../docker/docker-compose.yml exec [service] bash"
echo
echo "💡 Try this GraphQL query:"
echo "   query { listMetropolitanAreas { name code state } }"
echo
echo "🎨 Features:"
echo "  • JetBrains Mono typography for headings"
echo "  • Monospace fonts for body text"
echo "  • Tailwind UI components"
echo "  • Real-time GraphQL subscriptions"
echo "  • Interactive maps with Mapbox"
echo
echo "✨ Happy coding!"
