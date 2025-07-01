"""
Test API endpoints and health checks
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    """Test the root API endpoint."""
    response = await async_client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "GymIntel GraphQL API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "healthy"
    assert "endpoints" in data


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Test the health check endpoint."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data


@pytest.mark.asyncio
async def test_graphql_endpoint_accessible(async_client: AsyncClient):
    """Test that GraphQL endpoint is accessible."""
    response = await async_client.get("/graphql")
    # GraphQL endpoint should return 200 with GraphQL IDE
    assert response.status_code == 200