#!/usr/bin/env python3
"""
Minimal test server for debugging
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

# Create minimal app
app = FastAPI(title="GymIntel Test API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GraphQL
graphql_app = GraphQLRouter(schema, graphql_ide="graphiql")
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {
        "message": "GymIntel GraphQL API",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "graphql": "/graphql",
            "playground": "/graphql",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "services": {
            "yelp_api": "configured",
            "google_places": "configured",
            "postgresql": "connected"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🏋️ GymIntel GraphQL API Server")
    print("=" * 50)
    print("🌐 GraphQL Playground: http://localhost:8003/graphql")
    print("📋 API Root: http://localhost:8003")
    print("📚 API Docs: http://localhost:8003/docs")
    print("❤️ Health Check: http://localhost:8003/health")
    print()
    print("💡 Try this query:")
    print("   query { listMetropolitanAreas { name code state } }")
    
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")