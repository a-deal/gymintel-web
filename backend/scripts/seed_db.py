#!/usr/bin/env python3
"""
Database seeding script for GymIntel.

This script provides an easy interface to seed the database with sample data
for development or import real data for production environments.

Usage:
    # Seed development data
    python scripts/seed_db.py

    # Import from CLI export
    python scripts/seed_db.py --import-file exports/gyms_78704.json

    # Refresh data for a specific zipcode
    python scripts/seed_db.py --refresh-zipcode 78704

    # Production seeding (requires confirmation)
    python scripts/seed_db.py --production
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import get_settings  # noqa: E402
from app.seed_data import (  # noqa: E402
    import_from_cli_export,
    refresh_gym_data,
    seed_database,
    seed_development_data,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def confirm_action(message: str) -> bool:
    """Ask for user confirmation."""
    response = input(f"\n{message} (yes/no): ").lower().strip()
    return response in ["yes", "y"]


async def main():
    """Main entry point for the seeding script."""
    parser = argparse.ArgumentParser(
        description="Seed GymIntel database with sample or real data"
    )

    # Mutually exclusive group for different seeding modes
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--development",
        action="store_true",
        default=True,
        help="Seed with development sample data (default)",
    )

    group.add_argument(
        "--production",
        action="store_true",
        help="Seed for production environment",
    )

    group.add_argument(
        "--import-file",
        type=str,
        help="Import data from CLI JSON export file",
    )

    group.add_argument(
        "--refresh-zipcode",
        type=str,
        help="Refresh data for a specific zipcode using CLI",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompts",
    )

    args = parser.parse_args()

    settings = get_settings()

    try:
        if args.import_file:
            # Import from file
            file_path = Path(args.import_file)
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                sys.exit(1)

            if not args.force:
                if not confirm_action(f"Import data from {file_path}?"):
                    logger.info("Import cancelled")
                    sys.exit(0)

            logger.info(f"Importing data from {file_path}")
            await import_from_cli_export(str(file_path))
            logger.info("Import completed successfully")

        elif args.refresh_zipcode:
            # Refresh specific zipcode
            if not args.force:
                if not confirm_action(
                    f"Refresh data for zipcode {args.refresh_zipcode}?"
                ):
                    logger.info("Refresh cancelled")
                    sys.exit(0)

            logger.info(f"Refreshing data for zipcode {args.refresh_zipcode}")
            await refresh_gym_data(args.refresh_zipcode)
            logger.info("Refresh completed successfully")

        elif args.production:
            # Production seeding
            if settings.environment != "production":
                logger.warning(
                    f"Running production seed in {settings.environment} environment"
                )
                if not args.force:
                    if not confirm_action("Continue with production seeding?"):
                        logger.info("Production seeding cancelled")
                        sys.exit(0)

            logger.info("Starting production database seeding")
            await seed_database("production")
            logger.info("Production seeding completed")

        else:
            # Default: development seeding
            if settings.environment == "production" and not args.force:
                logger.warning(
                    "About to seed development data in production environment!"
                )
                if not confirm_action("Are you sure you want to continue?"):
                    logger.info("Development seeding cancelled")
                    sys.exit(0)

            logger.info("Starting development database seeding")
            await seed_development_data()
            logger.info("Development seeding completed successfully")

    except Exception as e:
        logger.error(f"Seeding failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
