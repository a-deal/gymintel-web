"""
Pytest configuration and fixtures for backend tests
"""

import asyncio

import pytest
import pytest_asyncio
from app.config import get_settings
from app.database import get_db
from app.main import app
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Get test database URL from settings
settings = get_settings()
TEST_DATABASE_URL = settings.async_test_database_url

# Create async test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Create async session factory for tests
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    async with test_engine.begin() as conn:
        # Import Base after engine is created
        from app.models.gym import Base

        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

    # Drop tables after test
    async with test_engine.begin() as conn:
        from app.models.gym import Base

        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def override_get_db(db_session):
    """Override the get_db dependency with test database."""

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(override_get_db):
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
