"""
GymIntel Web Application - FastAPI + GraphQL Backend
High-performance gym discovery platform with PostgreSQL and real-time updates
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import uvicorn

from .graphql.schema import schema


# Create FastAPI application
app = FastAPI(
    title="GymIntel GraphQL API",
    description="Advanced gym discovery platform with intelligent confidence scoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "https://gymintel.vercel.app",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Create GraphQL router
graphql_app = GraphQLRouter(
    schema, graphql_ide="graphiql"  # Enable GraphQL playground in development
)

# Include GraphQL router
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "GymIntel GraphQL API",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {"graphql": "/graphql", "playground": "/graphql", "docs": "/docs"},
    }


@app.get("/health")
async def health_check():
    """Detailed health check for monitoring"""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB health check
        "services": {
            "yelp_api": "configured",
            "google_places": "configured",
            "postgresql": "connected",
        },
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable hot reload in development
    )
