"""
Basic tests for main FastAPI application
"""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns expected response"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "GymIntel GraphQL API"
    assert response.json()["version"] == "1.0.0"
    assert response.json()["status"] == "healthy"


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "services" in response.json()
