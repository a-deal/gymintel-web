#!/usr/bin/env python3
"""
Initialize the database with tables and migrations.

Usage:
    python scripts/init_db.py [--force]

Options:
    --force     Drop and recreate all tables (WARNING: Data loss!)
"""

import asyncio
import logging
import os
import sys

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine  # noqa: E402
from app.db_init import init_database  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def drop_all_tables():
    """Drop all tables. Use with caution!"""
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("All tables dropped")


async def run_alembic_migrations():
    """Run Alembic migrations."""
    import subprocess

    try:
        # Run alembic upgrade head
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            logger.info("Alembic migrations completed successfully")
            logger.info(result.stdout)
        else:
            logger.error(f"Alembic migrations failed: {result.stderr}")
            return False

    except Exception as e:
        logger.error(f"Failed to run alembic migrations: {e}")
        return False

    return True


async def main():
    """Main function."""
    force = "--force" in sys.argv

    if force:
        logger.warning("Force mode enabled. This will drop all existing tables!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Aborted")
            return

        await drop_all_tables()

    # Initialize database (create tables, install PostGIS, etc.)
    await init_database()

    # Try to run Alembic migrations
    logger.info("Running Alembic migrations...")
    success = await run_alembic_migrations()

    if not success:
        logger.warning("Alembic migrations failed, but tables were created directly")

    logger.info("Database initialization completed!")


if __name__ == "__main__":
    asyncio.run(main())
