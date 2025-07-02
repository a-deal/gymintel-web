"""
GraphQL Resolvers Implementation
"""

import json
from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from ..database import get_db_session
from ..models.gym import DataSource, Gym
from ..services.cli_bridge import cli_bridge_service
from .schema import Coordinates
from .schema import DataSource as DataSourceType
from .schema import Gym as GymType
from .schema import GymAnalytics, ImportResult, MarketGap, MetropolitanArea
from .schema import Review as ReviewType
from .schema import SearchFilters, SearchResult


class GymResolvers:
    """Resolvers for Gym-related GraphQL operations"""

    @staticmethod
    async def search_gyms(
        zipcode: str,
        radius: float = 10.0,
        limit: int = 50,
        filters: Optional[SearchFilters] = None,
    ) -> SearchResult:
        """Search for gyms in a specific area"""

        # First, try to get from database
        async with get_db_session() as session:
            # Build base query
            query = select(Gym).options(
                selectinload(Gym.sources), selectinload(Gym.reviews)
            )

            # Apply zipcode filter if we have existing data
            if zipcode:
                query = query.where(Gym.source_zipcode == zipcode)

            # Apply additional filters
            if filters:
                if filters.min_rating and filters.min_rating > 0:
                    query = query.where(Gym.rating >= filters.min_rating)
                if filters.min_confidence and filters.min_confidence > 0:
                    query = query.where(Gym.confidence >= filters.min_confidence)
                if filters.has_website is not None:
                    if filters.has_website:
                        query = query.where(Gym.website.isnot(None))
                    else:
                        query = query.where(Gym.website.is_(None))
                if filters.has_instagram is not None:
                    if filters.has_instagram:
                        query = query.where(Gym.instagram.isnot(None))
                    else:
                        query = query.where(Gym.instagram.is_(None))

            query = query.limit(limit)
            result = await session.execute(query)
            existing_gyms = result.scalars().all()

            # If we have recent data, return it
            if existing_gyms:
                return SearchResult(
                    zipcode=zipcode,
                    coordinates=Coordinates(
                        latitude=existing_gyms[0].latitude if existing_gyms else 0.0,
                        longitude=existing_gyms[0].longitude if existing_gyms else 0.0,
                    ),
                    radius_miles=radius,
                    timestamp=datetime.utcnow(),
                    gyms=[GymResolvers._gym_to_graphql(gym) for gym in existing_gyms],
                    total_results=len(existing_gyms),
                    yelp_results=sum(
                        1
                        for gym in existing_gyms
                        if any(s.name == "Yelp" for s in gym.sources)
                    ),
                    google_results=sum(
                        1
                        for gym in existing_gyms
                        if any(s.name == "Google Places" for s in gym.sources)
                    ),
                    merged_count=sum(
                        1 for gym in existing_gyms if len(gym.sources) > 1
                    ),
                    avg_confidence=(
                        sum(gym.confidence for gym in existing_gyms)
                        / len(existing_gyms)
                        if existing_gyms
                        else 0.0
                    ),
                    execution_time_seconds=0.1,
                    use_google=True,
                )

        # If no existing data, fetch from CLI
        try:
            cli_result = await cli_bridge_service.search_gyms_via_cli(
                zipcode=zipcode, radius=radius, use_google=True
            )

            # Store results in database
            await GymResolvers._store_cli_results(cli_result)

            # Transform to GraphQL format
            search_info = cli_result["search_info"]
            gyms_data = cli_result["gyms"]

            gyms = []
            for gym_data in gyms_data:
                gym = GymType(
                    id=str(
                        gym_data.get(
                            "id", f"cli-{hash(gym_data['name'] + gym_data['address'])}"
                        )
                    ),
                    name=gym_data["name"],
                    address=gym_data["address"],
                    coordinates=Coordinates(
                        latitude=gym_data["latitude"], longitude=gym_data["longitude"]
                    ),
                    phone=gym_data.get("phone"),
                    website=gym_data.get("website"),
                    instagram=gym_data.get("instagram"),
                    confidence=gym_data["confidence"],
                    match_confidence=gym_data["confidence"],
                    rating=gym_data.get("rating"),
                    review_count=gym_data.get("review_count", 0),
                    sources=[
                        DataSourceType(
                            name=source["name"],
                            confidence=source["confidence"],
                            last_updated=datetime.fromisoformat(
                                source["last_updated"].replace("Z", "+00:00")
                            ),
                        )
                        for source in gym_data.get("sources", [])
                    ],
                    reviews=[],
                    source_zipcode=gym_data.get("source_zipcode"),
                    metropolitan_area_code=gym_data.get("metropolitan_area_code"),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                gyms.append(gym)

            return SearchResult(
                zipcode=search_info["zipcode"],
                coordinates=Coordinates(
                    latitude=search_info["coordinates"].get("latitude", 0.0),
                    longitude=search_info["coordinates"].get("longitude", 0.0),
                ),
                radius_miles=search_info["radius_miles"],
                timestamp=(
                    datetime.fromisoformat(search_info["timestamp"])
                    if search_info.get("timestamp")
                    else datetime.utcnow()
                ),
                gyms=gyms,
                total_results=search_info["total_results"],
                yelp_results=search_info["yelp_results"],
                google_results=search_info["google_results"],
                merged_count=search_info["merged_count"],
                avg_confidence=(
                    float(search_info["avg_confidence"].replace("%", "")) / 100.0
                    if isinstance(search_info["avg_confidence"], str)
                    else search_info["avg_confidence"]
                ),
                execution_time_seconds=2.0,  # Estimated CLI execution time
                use_google=search_info["use_google"],
            )

        except Exception:
            # Return empty result on error
            return SearchResult(
                zipcode=zipcode,
                coordinates=Coordinates(latitude=0.0, longitude=0.0),
                radius_miles=radius,
                timestamp=datetime.utcnow(),
                gyms=[],
                total_results=0,
                yelp_results=0,
                google_results=0,
                merged_count=0,
                avg_confidence=0.0,
                execution_time_seconds=0.0,
                use_google=True,
            )

    @staticmethod
    async def gym_by_id(gym_id: str) -> Optional[GymType]:
        """Get a specific gym by ID"""
        async with get_db_session() as session:
            query = (
                select(Gym)
                .options(selectinload(Gym.sources), selectinload(Gym.reviews))
                .where(Gym.id == gym_id)
            )

            result = await session.execute(query)
            gym = result.scalar_one_or_none()

            if gym:
                return GymResolvers._gym_to_graphql(gym)
            return None

    @staticmethod
    async def gyms_by_metro(
        metro_code: str, limit: int = 100, offset: int = 0
    ) -> List[GymType]:
        """Get gyms within a metropolitan area"""
        async with get_db_session() as session:
            query = (
                select(Gym)
                .options(selectinload(Gym.sources), selectinload(Gym.reviews))
                .where(Gym.metropolitan_area_code == metro_code)
                .offset(offset)
                .limit(limit)
            )

            result = await session.execute(query)
            gyms = result.scalars().all()

            return [GymResolvers._gym_to_graphql(gym) for gym in gyms]

    @staticmethod
    async def gym_analytics(zipcode: str) -> GymAnalytics:
        """Get comprehensive analytics for a ZIP code area"""
        async with get_db_session() as session:
            query = select(Gym).where(Gym.source_zipcode == zipcode)
            result = await session.execute(query)
            gyms = result.scalars().all()

            if not gyms:
                return GymAnalytics(
                    zipcode=zipcode,
                    total_gyms=0,
                    confidence_distribution="{}",
                    source_breakdown="{}",
                    rating_analysis="{}",
                    density_score=0.0,
                    market_saturation="low",
                )

            # Calculate analytics
            total_gyms = len(gyms)
            confidences = [gym.confidence for gym in gyms]
            ratings = [gym.rating for gym in gyms if gym.rating]

            # Confidence distribution histogram
            confidence_hist = {
                "0.0-0.2": 0,
                "0.2-0.4": 0,
                "0.4-0.6": 0,
                "0.6-0.8": 0,
                "0.8-1.0": 0,
            }
            for conf in confidences:
                if conf < 0.2:
                    confidence_hist["0.0-0.2"] += 1
                elif conf < 0.4:
                    confidence_hist["0.2-0.4"] += 1
                elif conf < 0.6:
                    confidence_hist["0.4-0.6"] += 1
                elif conf < 0.8:
                    confidence_hist["0.6-0.8"] += 1
                else:
                    confidence_hist["0.8-1.0"] += 1

            # Source breakdown
            source_counts = {}
            for gym in gyms:
                for source in gym.sources:
                    source_counts[source.name] = source_counts.get(source.name, 0) + 1

            # Rating analysis
            rating_stats = {
                "count": len(ratings),
                "average": sum(ratings) / len(ratings) if ratings else 0.0,
                "min": min(ratings) if ratings else 0.0,
                "max": max(ratings) if ratings else 0.0,
            }

            return GymAnalytics(
                zipcode=zipcode,
                total_gyms=total_gyms,
                confidence_distribution=json.dumps(confidence_hist),
                source_breakdown=json.dumps(source_counts),
                rating_analysis=json.dumps(rating_stats),
                density_score=total_gyms / 100.0,  # Simplified density calculation
                market_saturation=(
                    "high"
                    if total_gyms > 20
                    else "medium" if total_gyms > 10 else "low"
                ),
            )

    @staticmethod
    async def market_gap_analysis(
        zipcode: str, radius: float = 10.0
    ) -> List[MarketGap]:
        """Identify potential market opportunities"""
        # This is a simplified implementation
        # In a real app, this would use sophisticated geospatial analysis
        return [
            MarketGap(
                area_description=f"Underserved area near {zipcode}",
                coordinates=Coordinates(latitude=40.7128, longitude=-74.0060),
                gap_score=0.75,
                population_density=1500.0,
                nearest_gym_distance=2.5,
                reasoning=(
                    "High population density with limited gym options within 2 miles"
                ),
            )
        ]

    @staticmethod
    async def _store_cli_results(cli_result: dict):
        """Store CLI search results in database"""
        async with get_db_session() as session:
            gyms_data = cli_result.get("gyms", [])
            import logging

            logger = logging.getLogger(__name__)
            logger.info(f"Storing {len(gyms_data)} gyms from CLI search")

            for gym_data in gyms_data:
                # Check if gym already exists
                existing_query = select(Gym).where(
                    and_(
                        Gym.name == gym_data["name"], Gym.address == gym_data["address"]
                    )
                )
                result = await session.execute(existing_query)
                existing_gym = result.scalar_one_or_none()

                if existing_gym:
                    # Update existing gym
                    existing_gym.confidence = gym_data["confidence"]
                    existing_gym.rating = gym_data.get("rating")
                    existing_gym.review_count = gym_data.get("review_count", 0)
                    existing_gym.updated_at = datetime.utcnow()
                    logger.info(f"Updated existing gym: {existing_gym.name}")
                else:
                    # Create new gym
                    from geoalchemy2 import WKTElement

                    new_gym = Gym(
                        name=gym_data["name"],
                        address=gym_data["address"],
                        phone=gym_data.get("phone"),
                        website=gym_data.get("website"),
                        instagram=gym_data.get("instagram"),
                        latitude=gym_data["latitude"],
                        longitude=gym_data["longitude"],
                        location=WKTElement(
                            f"POINT({gym_data['longitude']} {gym_data['latitude']})",
                            srid=4326,
                        ),
                        confidence=gym_data["confidence"],
                        match_confidence=gym_data["confidence"],
                        rating=gym_data.get("rating"),
                        review_count=gym_data.get("review_count", 0),
                        source_zipcode=gym_data.get("source_zipcode"),
                        metropolitan_area_code=gym_data.get("metropolitan_area_code"),
                        raw_data=gym_data.get("raw_data"),
                    )
                    session.add(new_gym)
                    await session.flush()  # Get the ID
                    logger.info(f"Created new gym: {new_gym.name}")

                    # Add data sources
                    for source_data in gym_data.get("sources", []):
                        data_source = DataSource(
                            gym_id=new_gym.id,
                            name=source_data["name"],
                            confidence=source_data["confidence"],
                            last_updated=datetime.fromisoformat(
                                source_data["last_updated"].replace("Z", "+00:00")
                            ),
                        )
                        session.add(data_source)

            await session.commit()
            logger.info("Successfully committed CLI search results to database")

    @staticmethod
    def _gym_to_graphql(gym: Gym) -> GymType:
        """Convert SQLAlchemy Gym model to GraphQL type"""
        return GymType(
            id=str(gym.id),
            name=gym.name,
            address=gym.address,
            coordinates=Coordinates(latitude=gym.latitude, longitude=gym.longitude),
            phone=gym.phone,
            website=gym.website,
            instagram=gym.instagram,
            confidence=gym.confidence,
            match_confidence=gym.match_confidence,
            rating=gym.rating,
            review_count=gym.review_count,
            sources=[
                DataSourceType(
                    name=source.name,
                    confidence=source.confidence,
                    last_updated=source.last_updated,
                )
                for source in gym.sources
            ],
            reviews=[
                ReviewType(
                    rating=review.rating,
                    review_count=review.review_count,
                    sentiment_score=review.sentiment_score,
                    source=review.source,
                    last_updated=review.last_updated,
                )
                for review in gym.reviews
            ],
            source_zipcode=gym.source_zipcode,
            metropolitan_area_code=gym.metropolitan_area_code,
            created_at=gym.created_at,
            updated_at=gym.updated_at,
        )


class MetroResolvers:
    """Resolvers for Metropolitan Area operations"""

    @staticmethod
    async def metropolitan_area(code: str) -> Optional[MetropolitanArea]:
        """Get metropolitan area data by code"""
        try:
            metro_areas = await cli_bridge_service.get_metro_areas()
            for metro in metro_areas:
                if metro["code"] == code:
                    # This is a simplified implementation
                    # In production, you'd have proper MetroStatistics calculation
                    from .schema import MetroStatistics

                    stats = MetroStatistics(
                        total_gyms=0,
                        merged_gyms=0,
                        merge_rate=0.0,
                        average_confidence=0.0,
                        source_distribution="{}",
                        gyms_per_zip="{}",
                        deduplication_rate=0.0,
                    )

                    return MetropolitanArea(
                        id=metro["code"],
                        name=metro["name"],
                        code=metro["code"],
                        description=metro["description"],
                        state=metro["state"],
                        population=metro.get("population"),
                        density_category=metro["density_category"],
                        market_characteristics=metro["market_characteristics"],
                        zip_codes=metro["zip_codes"],
                        statistics=stats,
                    )
        except Exception:
            pass

        return None

    @staticmethod
    async def list_metropolitan_areas() -> List[MetropolitanArea]:
        """List all available metropolitan areas"""
        try:
            metro_areas = await cli_bridge_service.get_metro_areas()
            result = []

            for metro in metro_areas:
                from .schema import MetroStatistics

                stats = MetroStatistics(
                    total_gyms=0,
                    merged_gyms=0,
                    merge_rate=0.0,
                    average_confidence=0.0,
                    source_distribution="{}",
                    gyms_per_zip="{}",
                    deduplication_rate=0.0,
                )

                metro_area = MetropolitanArea(
                    id=metro["code"],
                    name=metro["name"],
                    code=metro["code"],
                    description=metro["description"],
                    state=metro["state"],
                    population=metro.get("population"),
                    density_category=metro["density_category"],
                    market_characteristics=metro["market_characteristics"],
                    zip_codes=metro["zip_codes"],
                    statistics=stats,
                )
                result.append(metro_area)

            return result
        except Exception:
            return []


class MutationResolvers:
    """Resolvers for GraphQL mutations"""

    @staticmethod
    async def import_gym_data(zipcode: str, data: List) -> ImportResult:
        """Import gym data from CLI search results"""
        try:
            gyms_imported = 0
            gyms_updated = 0
            errors = []
            start_time = datetime.utcnow()

            async with get_db_session() as session:
                for gym_data in data:
                    try:
                        # Check if gym exists
                        existing_query = select(Gym).where(
                            and_(
                                Gym.name == gym_data.name,
                                Gym.address == gym_data.address,
                            )
                        )
                        result = await session.execute(existing_query)
                        existing_gym = result.scalar_one_or_none()

                        if existing_gym:
                            # Update existing
                            existing_gym.confidence = gym_data.confidence
                            existing_gym.rating = gym_data.rating
                            existing_gym.review_count = gym_data.review_count
                            existing_gym.updated_at = datetime.utcnow()
                            gyms_updated += 1
                        else:
                            # Create new
                            from geoalchemy2 import WKTElement

                            new_gym = Gym(
                                name=gym_data.name,
                                address=gym_data.address,
                                phone=gym_data.phone,
                                website=gym_data.website,
                                instagram=gym_data.instagram,
                                latitude=gym_data.latitude,
                                longitude=gym_data.longitude,
                                location=WKTElement(
                                    f"POINT({gym_data.longitude} {gym_data.latitude})",
                                    srid=4326,
                                ),
                                confidence=gym_data.confidence,
                                match_confidence=gym_data.confidence,
                                rating=gym_data.rating,
                                review_count=gym_data.review_count or 0,
                                source_zipcode=zipcode,
                                raw_data={"imported": True},
                            )
                            session.add(new_gym)
                            gyms_imported += 1

                    except Exception as e:
                        errors.append(f"Failed to import {gym_data.name}: {str(e)}")

            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()

            return ImportResult(
                success=len(errors) == 0,
                gyms_imported=gyms_imported,
                gyms_updated=gyms_updated,
                errors=errors,
                import_duration_seconds=duration,
            )

        except Exception as e:
            return ImportResult(
                success=False,
                gyms_imported=0,
                gyms_updated=0,
                errors=[f"Import failed: {str(e)}"],
                import_duration_seconds=0.0,
            )
