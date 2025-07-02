#!/usr/bin/env python
"""
Railway startup script with proper environment handling
"""
import os

import uvicorn

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

    # Run the application
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
