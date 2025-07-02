#!/usr/bin/env python
"""
Railway startup script with proper environment handling
"""
import asyncio
import logging
import os

import uvicorn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Get port from Railway or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Railway provides DATABASE_URL in postgres:// format
    # We need to ensure it's available for the app
    if "DATABASE_URL" in os.environ and not os.environ.get("DATABASE_HOST"):
        # Parse Railway's DATABASE_URL to set individual components
        db_url = os.environ["DATABASE_URL"]

        # Railway uses postgres:// but we need postgresql://
        if db_url.startswith("postgres://"):
            os.environ["DATABASE_URL"] = db_url.replace(
                "postgres://", "postgresql://", 1
            )

    # Set production environment
    os.environ["ENVIRONMENT"] = "production"

    # Check if we should auto-initialize database
    if os.environ.get("AUTO_INIT_DB", "false").lower() == "true":
        logger.info("AUTO_INIT_DB is enabled, initializing database...")
        try:
            from app.db_init import init_database

            asyncio.run(init_database())
            logger.info("Database initialization completed")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            # Continue anyway - the app might work with existing tables

    # Run the application
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
