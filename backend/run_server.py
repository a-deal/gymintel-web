#!/usr/bin/env python3
"""
Simple script to run the GymIntel FastAPI server
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🏋️ Starting GymIntel GraphQL API Server...")
    print("📍 Server will be available at:")
    print("   • API: http://localhost:8001")
    print("   • GraphQL Playground: http://localhost:8001/graphql")
    print("   • API Docs: http://localhost:8001/docs")
    print("   • Health Check: http://localhost:8001/health")
    print()

    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info", access_log=True)
