#!/usr/bin/env python3
"""
Development server launcher for GymIntel Web
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🏋️ GymIntel Web - Development Server")
    print("=" * 50)
    print()
    print("🌐 Your GymIntel API is starting up...")
    print()
    print("📍 Available URLs:")
    print("   • GraphQL Playground: http://localhost:8000/graphql")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("   • API Root: http://localhost:8000/")
    print()
    print("🔧 Features:")
    print("   • JetBrains Mono typography")
    print("   • FastAPI + Strawberry GraphQL")
    print("   • Real-time subscriptions")
    print("   • CLI bridge integration")
    print()
    print("💡 Try this query in GraphQL Playground:")
    print("   query { listMetropolitanAreas { name code state } }")
    print()
    print("🚀 Starting server...")
    print()

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
