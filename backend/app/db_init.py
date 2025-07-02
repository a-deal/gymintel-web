"""Database initialization module.

This module ensures the database is properly initialized with:
1. PostGIS extension (if using PostgreSQL)
2. All required tables
3. Initial migrations
"""

import asyncio
import logging

from app.config import settings
from app.database import Base, engine
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

logger = logging.getLogger(__name__)


async def ensure_postgis_extension():
    """Ensure PostGIS extension is installed in PostgreSQL."""
    if not settings.async_database_url.startswith("postgresql"):
        logger.info("Not using PostgreSQL, skipping PostGIS check")
        return

    try:
        # Create a new engine without database name to connect to postgres db
        db_url_parts = settings.async_database_url.split("/")
        base_url = "/".join(db_url_parts[:-1])
        db_name = db_url_parts[-1].split("?")[0]

        # Connect to the default 'postgres' database
        postgres_url = f"{base_url}/postgres"
        if "asyncpg" in postgres_url:
            postgres_engine = create_async_engine(postgres_url, echo=False)
        else:
            # Convert to async URL if needed
            postgres_url = postgres_url.replace(
                "postgresql://", "postgresql+asyncpg://"
            )
            postgres_engine = create_async_engine(postgres_url, echo=False)

        async with postgres_engine.connect() as conn:
            # First ensure the database exists
            result = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            )
            if not result.scalar():
                logger.error(f"Database '{db_name}' does not exist")
                return

        # Now connect to our actual database
        async with engine.connect() as conn:
            # Check if PostGIS is already installed
            result = await conn.execute(
                text("SELECT 1 FROM pg_extension WHERE extname = 'postgis'")
            )
            if result.scalar():
                logger.info("PostGIS extension already installed")
            else:
                # Try to create PostGIS extension
                try:
                    await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
                    await conn.commit()
                    logger.info("PostGIS extension installed successfully")
                except Exception as e:
                    logger.warning(f"Could not create PostGIS extension: {e}")
                    logger.warning(
                        "You may need to install it manually with superuser privileges"
                    )

    except Exception as e:
        logger.error(f"Error checking/installing PostGIS: {e}")


async def create_tables():
    """Create all database tables from SQLAlchemy models."""
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("All database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise


async def init_database():
    """Initialize the database with all required components."""
    logger.info("Starting database initialization...")

    # Ensure PostGIS is installed (for PostgreSQL)
    await ensure_postgis_extension()

    # Create tables
    await create_tables()

    logger.info("Database initialization completed")


if __name__ == "__main__":
    # Run initialization when module is executed directly
    asyncio.run(init_database())
