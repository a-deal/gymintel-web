"""
Test GraphQL schema and resolvers
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_graphql_schema_introspection(async_client: AsyncClient):
    """Test GraphQL schema introspection query."""
    query = """
    query IntrospectionQuery {
      __schema {
        types {
          name
          kind
        }
      }
    }
    """

    response = await async_client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "__schema" in data["data"]
    assert "types" in data["data"]["__schema"]


@pytest.mark.asyncio
async def test_list_metropolitan_areas_query(async_client: AsyncClient):
    """Test the listMetropolitanAreas GraphQL query."""
    query = """
    query {
      listMetropolitanAreas {
        name
        code
        state
      }
    }
    """

    response = await async_client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "listMetropolitanAreas" in data["data"]
    # Should return a list (might be empty in test environment)
    assert isinstance(data["data"]["listMetropolitanAreas"], list)


@pytest.mark.asyncio
async def test_invalid_graphql_query(async_client: AsyncClient):
    """Test handling of invalid GraphQL queries."""
    query = """
    query {
      nonExistentField {
        invalidField
      }
    }
    """

    response = await async_client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    data = response.json()
    assert "errors" in data
    assert len(data["errors"]) > 0
