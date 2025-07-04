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
from ..services.city_boundaries import CityBoundaryService
from ..services.cli_bridge import cli_bridge_service
from ..services.geocoding import geocoding_service
from ..services.search_progress import search_progress_manager
from .schema import Coordinates
from .schema import DataSource as DataSourceType
from .schema import Gym as GymType
from .schema import GymAnalytics, ImportResult, MarketGap, MetropolitanArea
from .schema import Review as ReviewType
from .schema import SearchFilters, SearchResult


class GymResolvers:
    """Resolvers for Gym-related GraphQL operations"""

    @staticmethod
    async def search_gyms_by_location(
        location: str,
        radius: float = 10.0,
        limit: int = 50,
        filters: Optional[SearchFilters] = None,
    ) -> SearchResult:
        """Search for gyms in a specific area"""
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Searching for gyms in location: {location}")

        # Initialize city boundary service
        city_boundary_service = CityBoundaryService(geocoding_service)

        # Get location information (city coordinates, boundaries, etc.)
        location_info = await geocoding_service.search_location(location)
        logger.info(f"Geocoding result - location_info: {location_info}")

        if not location_info:
            # Could not geocode the location
            raise Exception(f"Could not find location: {location}")

        # Location is passed as parameter to this function

        # First, try to get from database using city boundary service
        async with get_db_session() as session:
            # Build base query
            query = select(Gym).options(
                selectinload(Gym.sources), selectinload(Gym.reviews)
            )

            # Use city boundary service to find gyms
            existing_gyms = []  # Initialize to empty list

            # Extract state from location_info if available
            state = None
            if location_info:
                # Try to extract state from geocoding result
                if "state" in location_info:
                    state = location_info["state"]
                elif "address_components" in location_info:
                    # Look for state in address components (common in geocoding results)
                    for component in location_info.get("address_components", []):
                        if "administrative_area_level_1" in component.get("types", []):
                            state = component.get("short_name")
                            break

            # Use city boundary service to find gyms
            try:
                gym_results = await city_boundary_service.find_gyms_in_city(
                    session, city_name=location, state=state, limit=limit
                )
                logger.info(f"Found {len(gym_results)} gyms for {location}")

                # Convert city boundary service results to Gym objects
                if gym_results:
                    # Get the gym IDs from results
                    gym_ids = [result["id"] for result in gym_results]

                    # Query to get full Gym objects with relationships
                    query = (
                        select(Gym)
                        .options(selectinload(Gym.sources), selectinload(Gym.reviews))
                        .where(Gym.id.in_(gym_ids))
                    )

                    # Apply additional filters before executing
                    if filters:
                        if filters.min_rating and filters.min_rating > 0:
                            query = query.where(Gym.rating >= filters.min_rating)
                        if filters.min_confidence and filters.min_confidence > 0:
                            query = query.where(
                                Gym.confidence >= filters.min_confidence
                            )
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

                    result = await session.execute(query)
                    existing_gyms = result.scalars().all()

                    # Sort gyms by their original order from city boundary service
                    gym_order = {gym_id: idx for idx, gym_id in enumerate(gym_ids)}
                    existing_gyms.sort(
                        key=lambda gym: gym_order.get(str(gym.id), float("inf"))
                    )

                    logger.info(f"After filtering, returning {len(existing_gyms)} gyms")
                else:
                    logger.info("No gyms found by city boundary service")
                    existing_gyms = []
            except Exception as e:
                logger.error(f"Error using city boundary service: {e}")
                existing_gyms = []

            # If we have recent data, return it
            if existing_gyms:
                return SearchResult(
                    location=location,
                    coordinates=Coordinates(
                        latitude=(
                            location_info.get("latitude", existing_gyms[0].latitude)
                            if location_info
                            else existing_gyms[0].latitude
                        ),
                        longitude=(
                            location_info.get("longitude", existing_gyms[0].longitude)
                            if location_info
                            else existing_gyms[0].longitude
                        ),
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
            # For now, return empty result as CLI expects zipcode
            # TODO: Update CLI to support city-based search
            logger.warning(f"CLI search not yet supported for city: {location}")
            return SearchResult(
                location=location,
                coordinates=Coordinates(
                    latitude=(
                        location_info.get("latitude", 0.0) if location_info else 0.0
                    ),
                    longitude=(
                        location_info.get("longitude", 0.0) if location_info else 0.0
                    ),
                ),
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

            # Original CLI call code (disabled for now)
            # cli_result = await cli_bridge_service.search_gyms_via_cli(
            #     zipcode=search_zipcode, radius=radius, use_google=True
            # )

            # Store results in database when CLI is available
            # await GymResolvers._store_cli_results(cli_result)

            # Transform to GraphQL format when CLI is available
            # search_info = cli_result["search_info"]
            # gyms_data = cli_result["gyms"]

            # CLI code disabled until city-based search is supported
            pass

        except Exception as e:
            # Re-raise the exception instead of hiding it
            logger.error(f"Error in search_gyms: {e}")
            raise

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
    async def gym_analytics(location: str) -> GymAnalytics:
        """Get comprehensive analytics for a city or area"""
        # Get location information to find gyms by coordinates
        location_info = await geocoding_service.search_location(location)

        async with get_db_session() as session:
            if (
                location_info
                and "latitude" in location_info
                and "longitude" in location_info
            ):
                lat = location_info["latitude"]
                lon = location_info["longitude"]

                # Find gyms within 10 miles of the city center using PostGIS
                from geoalchemy2 import WKTElement
                from sqlalchemy import func

                # Create a point for the city center
                city_point = WKTElement(f"POINT({lon} {lat})", srid=4326)
                radius_meters = 10 * 1609.34  # 10 miles in meters

                query = select(Gym).where(
                    func.ST_DWithin(Gym.location, city_point, radius_meters)
                )
                result = await session.execute(query)
                gyms = result.scalars().all()
            else:
                gyms = []

            if not gyms:
                return GymAnalytics(
                    location=location,
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
                location=location,
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
        location: str, radius: float = 10.0
    ) -> List[MarketGap]:
        """Identify potential market opportunities"""
        # This is a simplified implementation
        # In a real app, this would use sophisticated geospatial analysis
        return [
            MarketGap(
                area_description=f"Underserved area near {location}",
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
    async def _store_cli_results(cli_result: dict, location: str = "Unknown"):
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
                        source_city=location,
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
            source_city=gym.source_city,
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
                        cities=metro.get("cities", []),
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
    async def import_gym_data(location: str, data: List) -> ImportResult:
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
                                source_city=location,
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

    @staticmethod
    async def trigger_gym_search(location: str, radius: float = 10.0) -> str:
        """
        Trigger a gym search for a location.
        Returns a search_id to track progress via subscription.
        """
        import asyncio

        # Create search in progress manager
        search_id = search_progress_manager.create_search(location, radius)

        # Start the search asynchronously
        asyncio.create_task(
            MutationResolvers._perform_gym_search(search_id, location, radius)
        )

        return search_id

    @staticmethod
    async def _perform_gym_search(search_id: str, location: str, radius: float):
        """Perform the actual gym search with progress updates."""
        import asyncio
        import logging

        logger = logging.getLogger(__name__)

        # Set a 5-minute timeout for the entire search operation
        search_timeout = 300  # 5 minutes

        try:
            # Run the search with a timeout
            await asyncio.wait_for(
                MutationResolvers._perform_gym_search_internal(
                    search_id, location, radius
                ),
                timeout=search_timeout,
            )
        except asyncio.TimeoutError:
            logger.error(f"Search {search_id} timed out after {search_timeout} seconds")
            await search_progress_manager.update_progress(
                search_id,
                "error",
                0.0,
                "Search timed out",
                message=f"Search operation exceeded {search_timeout} seconds",
            )
        except Exception as e:
            logger.error(f"Search failed: {e}")
            await search_progress_manager.update_progress(
                search_id, "error", 0.0, "Search failed", message=str(e)
            )

    @staticmethod
    async def _perform_gym_search_internal(
        search_id: str, location: str, radius: float
    ):
        """Internal method to perform the actual gym search."""
        import logging

        logger = logging.getLogger(__name__)

        try:
            # Step 1: Geocoding (10% progress)
            await search_progress_manager.update_progress(
                search_id, "geocoding", 10.0, "Converting location to coordinates"
            )

            location_info = await geocoding_service.search_location(location)

            if not location_info:
                await search_progress_manager.update_progress(
                    search_id,
                    "error",
                    10.0,
                    "Location not found",
                    message=f"Could not find location: {location}",
                )
                return

            # Update with location info
            await search_progress_manager.update_progress(
                search_id,
                "searching",
                20.0,
                "Location found",
                location_info=location_info,
            )

            search_location = location

            # Step 2: Check database (30% progress)
            await search_progress_manager.update_progress(
                search_id, "searching", 30.0, "Checking existing data"
            )

            async with get_db_session() as session:
                # Check if we already have gyms for this city
                query = select(Gym).where(Gym.source_city == search_location).limit(1)
                result = await session.execute(query)
                existing_gym = result.scalar_one_or_none()

                if existing_gym:
                    # We already have data
                    await search_progress_manager.update_progress(
                        search_id,
                        "complete",
                        100.0,
                        "Search complete",
                        message="Found existing gym data in database",
                    )
                    return

            # Step 3: Search Yelp (50% progress)
            await search_progress_manager.update_progress(
                search_id, "searching_yelp", 50.0, "Searching Yelp for gyms"
            )

            # Step 4: Search Google (70% progress)
            await search_progress_manager.update_progress(
                search_id, "searching_google", 70.0, "Searching Google Places"
            )

            # Step 5: Perform actual CLI search
            try:
                # TODO: Update CLI to support city-based search
                logger.warning(
                    f"CLI search not yet supported for city: {search_location}"
                )
                await search_progress_manager.update_progress(
                    search_id,
                    "error",
                    90.0,
                    "CLI search not available",
                    message="City-based CLI search not yet implemented",
                )
                return

                # Step 6: Merge and store results (90% progress)
                await search_progress_manager.update_progress(
                    search_id, "merging", 90.0, "Merging and storing results"
                )

                # await GymResolvers._store_cli_results(cli_result)

                # Complete (100% progress)
                gym_count = 0  # len(cli_result.get("gyms", []))
                await search_progress_manager.update_progress(
                    search_id,
                    "complete",
                    100.0,
                    "Search complete",
                    message=f"Found {gym_count} gyms",
                )

            except Exception as e:
                logger.error(f"CLI search failed: {e}")
                await search_progress_manager.update_progress(
                    search_id, "error", 90.0, "Search failed", message=str(e)
                )

        except Exception as e:
            logger.error(f"Search failed: {e}")
            await search_progress_manager.update_progress(
                search_id, "error", 0.0, "Search failed", message=str(e)
            )
            raise  # Re-raise to be caught by timeout handler
