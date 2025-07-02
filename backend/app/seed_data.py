"""
Database seeding module for development and production environments.

This module provides functions to populate the database with:
- Sample data for local development
- Real data imports from CLI for production
- Scheduled data refresh capabilities
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict
from uuid import uuid4

from app.database import get_db_session
from app.models.gym import DataSource, Gym, Review
from app.models.metro import MetropolitanArea
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


# Sample data for local development
SAMPLE_METRO_AREAS = [
    {
        "code": "austin-tx",
        "name": "Austin-Round Rock-Georgetown",
        "title": "Austin-Round Rock-Georgetown, TX Metropolitan Statistical Area",
        "population": 2283371,
        "land_area_sq_miles": 4279.5,
        "zipcodes": ["78701", "78702", "78703", "78704", "78705"],
    },
    {
        "code": "sf-ca",
        "name": "San Francisco-Oakland-Berkeley",
        "title": "San Francisco-Oakland-Berkeley, CA Metropolitan Statistical Area",
        "population": 4749008,
        "land_area_sq_miles": 2474.0,
        "zipcodes": ["94102", "94103", "94104", "94105", "94107"],
    },
    {
        "code": "nyc-ny",
        "name": "New York-Newark-Jersey City",
        "title": "New York-Newark-Jersey City, NY-NJ-PA Metropolitan Statistical Area",
        "population": 8336817,
        "land_area_sq_miles": 302.6,
        "zipcodes": ["10001", "10002", "10003", "10004", "10005"],
    },
]

SAMPLE_GYMS = [
    # High confidence gyms (0.8-1.0)
    {
        "name": "Gold's Gym Downtown",
        "address": "123 Main St, Austin, TX 78701",
        "phone": "(512) 555-0100",
        "website": "https://goldsgym.com/downtown",
        "instagram": "@goldsgymdowntown",
        "latitude": 30.2672,
        "longitude": -97.7431,
        "confidence": 0.95,
        "match_confidence": 0.92,
        "rating": 4.5,
        "review_count": 328,
        "source_zipcode": "78701",
        "metropolitan_area_code": "austin-tx",
    },
    {
        "name": "CrossFit Austin Central",
        "address": "456 Congress Ave, Austin, TX 78701",
        "phone": "(512) 555-0200",
        "website": "https://crossfitaustin.com",
        "instagram": "@crossfitaustin",
        "latitude": 30.2688,
        "longitude": -97.7405,
        "confidence": 0.88,
        "match_confidence": 0.85,
        "rating": 4.8,
        "review_count": 156,
        "source_zipcode": "78701",
        "metropolitan_area_code": "austin-tx",
    },
    # Medium confidence gyms (0.5-0.8)
    {
        "name": "FitLife Wellness Center",
        "address": "789 Lamar Blvd, Austin, TX 78704",
        "phone": "(512) 555-0300",
        "website": None,
        "instagram": "@fitlifeatx",
        "latitude": 30.2572,
        "longitude": -97.7560,
        "confidence": 0.72,
        "match_confidence": 0.68,
        "rating": 4.2,
        "review_count": 89,
        "source_zipcode": "78704",
        "metropolitan_area_code": "austin-tx",
    },
    # Low confidence gyms (0.0-0.5)
    {
        "name": "Underground Strength",
        "address": "321 Side St, Austin, TX 78702",
        "phone": None,
        "website": None,
        "instagram": None,
        "latitude": 30.2622,
        "longitude": -97.7280,
        "confidence": 0.35,
        "match_confidence": 0.30,
        "rating": None,
        "review_count": 0,
        "source_zipcode": "78702",
        "metropolitan_area_code": "austin-tx",
    },
]

SAMPLE_REVIEWS = [
    {
        "gym_name": "Gold's Gym Downtown",
        "reviews": [
            {
                "source": "Google Places",
                "rating": 5.0,
                "review_count": 150,
                "sample_review_text": "Amazing gym with state-of-the-art equipment!",
                "sentiment_score": 0.9,
                "source_url": "https://maps.google.com/?q=Gold's+Gym+Downtown",
            },
            {
                "source": "Yelp",
                "rating": 4.0,
                "review_count": 178,
                "sample_review_text": (
                    "Great classes but can get crowded during peak hours."
                ),
                "sentiment_score": 0.6,
                "source_url": "https://yelp.com/biz/golds-gym-downtown",
            },
        ],
    },
    {
        "gym_name": "CrossFit Austin Central",
        "reviews": [
            {
                "source": "Google Places",
                "rating": 5.0,
                "review_count": 85,
                "sample_review_text": (
                    "Best CrossFit box in Austin! Coaches are incredible."
                ),
                "sentiment_score": 0.95,
                "source_url": "https://maps.google.com/?q=CrossFit+Austin+Central",
            },
            {
                "source": "Yelp",
                "rating": 4.8,
                "review_count": 71,
                "sample_review_text": "Excellent community and challenging workouts.",
                "sentiment_score": 0.85,
                "source_url": "https://yelp.com/biz/crossfit-austin-central",
            },
        ],
    },
]


async def seed_metro_areas(session: AsyncSession) -> Dict[str, MetropolitanArea]:
    """Seed metropolitan areas and return mapping."""
    metro_map = {}

    for metro_data in SAMPLE_METRO_AREAS:
        # Extract zipcodes (not a model field)
        zipcodes = metro_data.pop("zipcodes", [])

        # Check if already exists
        result = await session.execute(
            select(MetropolitanArea).where(MetropolitanArea.code == metro_data["code"])
        )
        metro = result.scalar_one_or_none()

        if not metro:
            metro = MetropolitanArea(
                id=uuid4(),
                **metro_data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(metro)
            logger.info(f"Created metro area: {metro.name}")

        metro_map[metro.code] = metro

        # Add zipcodes back for gym seeding reference
        metro_data["zipcodes"] = zipcodes

    await session.commit()
    return metro_map


async def seed_gyms(
    session: AsyncSession, metro_map: Dict[str, MetropolitanArea]
) -> Dict[str, Gym]:
    """Seed gyms and return mapping."""
    gym_map = {}

    for gym_data in SAMPLE_GYMS:
        # Check if already exists
        result = await session.execute(
            select(Gym).where(
                Gym.name == gym_data["name"],
                Gym.address == gym_data["address"],
            )
        )
        gym = result.scalar_one_or_none()

        if not gym:
            gym_dict = gym_data.copy()
            # Remove metro code as it's not a direct field
            # metro_code = gym_dict.pop("metropolitan_area_code", None)
            gym_dict.pop("metropolitan_area_code", None)

            # Create PostGIS point
            if gym_dict.get("latitude") and gym_dict.get("longitude"):
                from geoalchemy2 import WKTElement

                point = WKTElement(
                    f"POINT({gym_dict['longitude']} {gym_dict['latitude']})",
                    srid=4326,
                )
                gym_dict["location"] = point

            gym = Gym(
                id=uuid4(),
                **gym_dict,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(gym)
            logger.info(f"Created gym: {gym.name}")

            # Create data sources
            if gym_data.get("rating") is not None:
                # Google source
                google_source = DataSource(
                    id=uuid4(),
                    gym_id=gym.id,
                    name="Google Places",
                    source_id=f"google_{gym.id}",
                    confidence=gym_data.get("confidence", 0.5),
                    api_response={
                        "rating": gym_data["rating"],
                        "review_count": gym_data["review_count"] // 2,
                    },
                    last_updated=datetime.utcnow(),
                )
                session.add(google_source)

                # Yelp source
                yelp_source = DataSource(
                    id=uuid4(),
                    gym_id=gym.id,
                    name="Yelp",
                    source_id=f"yelp_{gym.id}",
                    confidence=gym_data.get("confidence", 0.5),
                    api_response={
                        "rating": gym_data["rating"],
                        "review_count": gym_data["review_count"] // 2,
                    },
                    last_updated=datetime.utcnow(),
                )
                session.add(yelp_source)

        gym_map[gym.name] = gym

    await session.commit()
    return gym_map


async def seed_reviews(session: AsyncSession, gym_map: Dict[str, Gym]) -> None:
    """Seed reviews for gyms."""
    for review_data in SAMPLE_REVIEWS:
        gym = gym_map.get(review_data["gym_name"])
        if not gym:
            continue

        for review in review_data["reviews"]:
            # Check if review already exists
            result = await session.execute(
                select(Review).where(
                    Review.gym_id == gym.id,
                    Review.source == review["source"],
                )
            )
            existing = result.scalar_one_or_none()

            if not existing:
                new_review = Review(
                    id=uuid4(),
                    gym_id=gym.id,
                    rating=review["rating"],
                    review_count=review["review_count"],
                    sentiment_score=review.get("sentiment_score"),
                    source=review["source"],
                    source_url=review.get("source_url"),
                    sample_review_text=review.get("sample_review_text"),
                    last_updated=datetime.utcnow(),
                )
                session.add(new_review)
                logger.info(f"Created {review['source']} reviews for {gym.name}")

    await session.commit()


async def seed_development_data() -> None:
    """Seed the database with sample data for development."""
    logger.info("Starting development data seeding...")

    async with get_db_session() as session:
        # Seed in order of dependencies
        metro_map = await seed_metro_areas(session)
        gym_map = await seed_gyms(session, metro_map)
        await seed_reviews(session, gym_map)

    logger.info("Development data seeding completed!")


async def import_from_cli_export(json_file_path: str) -> None:
    """Import gym data from CLI JSON export."""
    logger.info(f"Importing data from CLI export: {json_file_path}")

    with open(json_file_path, "r") as f:
        cli_data = json.load(f)

    async with get_db_session() as session:
        # Import gyms
        gyms = cli_data.get("gyms", [])
        imported_count = 0

        for gym_data in gyms:
            # Check if gym already exists
            result = await session.execute(
                select(Gym).where(
                    Gym.name == gym_data["name"],
                    Gym.address == gym_data["address"],
                )
            )
            existing = result.scalar_one_or_none()

            if not existing:
                # Transform CLI data to our schema
                gym = Gym(
                    id=uuid4(),
                    name=gym_data["name"],
                    address=gym_data["address"],
                    phone=gym_data.get("phone"),
                    website=gym_data.get("website"),
                    latitude=gym_data.get("latitude"),
                    longitude=gym_data.get("longitude"),
                    confidence=gym_data.get("confidence_score", 0.5),
                    match_confidence=gym_data.get("match_confidence", 0.5),
                    rating=gym_data.get("rating"),
                    review_count=gym_data.get("review_count", 0),
                    source_zipcode=gym_data.get("zipcode"),
                    raw_data=gym_data,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )

                # Create location point if coordinates exist
                if gym.latitude and gym.longitude:
                    from geoalchemy2 import WKTElement

                    gym.location = WKTElement(
                        f"POINT({gym.longitude} {gym.latitude})",
                        srid=4326,
                    )

                session.add(gym)
                imported_count += 1

        await session.commit()
        logger.info(f"Imported {imported_count} new gyms from CLI export")


async def refresh_gym_data(zipcode: str) -> None:
    """Refresh gym data for a specific zipcode using CLI integration."""
    logger.info(f"Refreshing gym data for zipcode: {zipcode}")

    try:
        # Import CLI search function
        from cli_services.run_gym_search import run_gym_search

        # Run search
        result = await run_gym_search(zipcode, quiet=True)

        if result and "gyms" in result:
            # Import the fresh data
            async with get_db_session() as session:
                updated_count = 0

                for gym_data in result["gyms"]:
                    # Update or create gym
                    result = await session.execute(
                        select(Gym).where(
                            Gym.name == gym_data["name"],
                            Gym.source_zipcode == zipcode,
                        )
                    )
                    gym = result.scalar_one_or_none()

                    if gym:
                        # Update existing
                        gym.confidence = gym_data.get(
                            "confidence_score", gym.confidence
                        )
                        gym.rating = gym_data.get("rating", gym.rating)
                        gym.review_count = gym_data.get(
                            "review_count", gym.review_count
                        )
                        gym.updated_at = datetime.utcnow()
                        updated_count += 1
                    else:
                        # Create new (use import logic)
                        # ... (similar to import_from_cli_export)
                        pass

                await session.commit()
                logger.info(f"Updated {updated_count} gyms for zipcode {zipcode}")

    except ImportError:
        logger.warning("CLI services not available for data refresh")
    except Exception as e:
        logger.error(f"Error refreshing data for {zipcode}: {e}")


# Main seeding function
async def seed_database(environment: str = "development") -> None:
    """Main function to seed database based on environment."""
    if environment == "development":
        await seed_development_data()
    elif environment == "production":
        # In production, we might want to:
        # 1. Import from a specific CLI export
        # 2. Set up scheduled refreshes
        # 3. Import from multiple sources
        logger.info("Production seeding should be configured based on requirements")
    else:
        logger.warning(f"Unknown environment: {environment}")


if __name__ == "__main__":
    # Run seeding when module is executed directly
    asyncio.run(seed_database())
