"""
Database configuration and session management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from contextlib import asynccontextmanager

from .models.gym import Base

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost/gymintel_web"
)

# Convert to async URL if needed
if not DATABASE_URL.startswith("postgresql+asyncpg://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Create async engine
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_db_session():
    """Get database session with automatic cleanup"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Drop all database tables (for testing)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)