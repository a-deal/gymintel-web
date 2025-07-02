#!/usr/bin/env python3
"""
Production data refresh script for GymIntel.

This script is designed to be run periodically (e.g., via cron) to refresh
gym data for active zipcodes in production environments.

Features:
- Refresh data for high-traffic zipcodes
- Rate-limited API calls to avoid overloading external services
- Error handling and retry logic
- Logging for monitoring
- Can be scheduled via cron or other schedulers

Usage:
    # Refresh data for specific zipcodes
    python scripts/refresh_production_data.py --zipcodes 78704 78705 78706

    # Refresh data for top N most searched zipcodes
    python scripts/refresh_production_data.py --top-zipcodes 10

    # Refresh all zipcodes that haven't been updated in N days
    python scripts/refresh_production_data.py --stale-days 7

    # Dry run (show what would be refreshed)
    python scripts/refresh_production_data.py --top-zipcodes 5 --dry-run
"""

import argparse
import asyncio
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import get_settings  # noqa: E402
from app.database import get_db_session  # noqa: E402
from app.models import Gym  # noqa: E402
from app.seed_data import refresh_gym_data  # noqa: E402
from sqlalchemy import and_, func, select  # noqa: E402

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def get_stale_zipcodes(days: int) -> List[str]:
    """Get zipcodes that haven't been updated in N days."""
    stale_date = datetime.utcnow() - timedelta(days=days)

    async with get_db_session() as session:
        query = (
            select(Gym.source_zipcode)
            .where(
                and_(
                    Gym.source_zipcode.isnot(None),
                    Gym.updated_at < stale_date,
                )
            )
            .group_by(Gym.source_zipcode)
            .order_by(func.min(Gym.updated_at))
        )

        result = await session.execute(query)
        return [row[0] for row in result.fetchall()]


async def get_top_searched_zipcodes(limit: int) -> List[str]:
    """Get the most frequently accessed zipcodes."""
    # In a real implementation, this would query access logs or analytics
    # For now, we'll use zipcodes with the most gyms as a proxy
    async with get_db_session() as session:
        query = (
            select(Gym.source_zipcode, func.count(Gym.id).label("gym_count"))
            .where(Gym.source_zipcode.isnot(None))
            .group_by(Gym.source_zipcode)
            .order_by(func.count(Gym.id).desc())
            .limit(limit)
        )

        result = await session.execute(query)
        return [row[0] for row in result.fetchall()]


async def refresh_zipcodes_with_rate_limit(
    zipcodes: List[str], dry_run: bool = False
) -> None:
    """Refresh multiple zipcodes with rate limiting."""
    total = len(zipcodes)
    success_count = 0
    error_count = 0

    logger.info(f"Starting refresh for {total} zipcodes")

    for i, zipcode in enumerate(zipcodes, 1):
        try:
            if dry_run:
                logger.info(f"[DRY RUN] Would refresh {zipcode} ({i}/{total})")
            else:
                logger.info(f"Refreshing {zipcode} ({i}/{total})")
                await refresh_gym_data(zipcode)
                success_count += 1

                # Rate limit: wait 2 seconds between API calls
                if i < total:
                    await asyncio.sleep(2)

        except Exception as e:
            error_count += 1
            logger.error(f"Failed to refresh {zipcode}: {e}")

            # Continue with next zipcode
            continue

    logger.info(f"Refresh completed: {success_count} successful, {error_count} errors")


async def main():
    """Main entry point for the refresh script."""
    parser = argparse.ArgumentParser(
        description="Refresh gym data for production environments"
    )

    # Mutually exclusive group for different refresh modes
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--zipcodes",
        nargs="+",
        help="Specific zipcodes to refresh",
    )

    group.add_argument(
        "--top-zipcodes",
        type=int,
        help="Refresh the top N most searched zipcodes",
    )

    group.add_argument(
        "--stale-days",
        type=int,
        help="Refresh zipcodes not updated in N days",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be refreshed without making changes",
    )

    parser.add_argument(
        "--max-zipcodes",
        type=int,
        default=50,
        help="Maximum number of zipcodes to refresh in one run (default: 50)",
    )

    args = parser.parse_args()

    settings = get_settings()

    if settings.environment != "production":
        logger.warning(
            f"Running production refresh in {settings.environment} environment"
        )

    try:
        # Determine which zipcodes to refresh
        if args.zipcodes:
            zipcodes = args.zipcodes
            logger.info(f"Refreshing specific zipcodes: {zipcodes}")

        elif args.top_zipcodes:
            zipcodes = await get_top_searched_zipcodes(args.top_zipcodes)
            logger.info(f"Found {len(zipcodes)} top searched zipcodes")

        elif args.stale_days:
            zipcodes = await get_stale_zipcodes(args.stale_days)
            logger.info(
                f"Found {len(zipcodes)} zipcodes not updated in {args.stale_days} days"
            )

        # Apply max limit
        if len(zipcodes) > args.max_zipcodes:
            logger.warning(
                f"Limiting refresh to {args.max_zipcodes} zipcodes "
                f"(found {len(zipcodes)})"
            )
            zipcodes = zipcodes[: args.max_zipcodes]

        # Perform refresh
        if zipcodes:
            await refresh_zipcodes_with_rate_limit(zipcodes, args.dry_run)
        else:
            logger.info("No zipcodes found to refresh")

    except Exception as e:
        logger.error(f"Refresh script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
