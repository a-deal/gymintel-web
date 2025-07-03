"""
City boundary service using PostGIS for accurate geographic searches
"""

import logging
from typing import Any, Dict, List, Optional

from app.services.geocoding import GeocodingService
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class CityBoundaryService:
    """Service for city boundary-based geographic queries"""

    def __init__(self, geocoding_service: GeocodingService):
        self.geocoding_service = geocoding_service

    async def find_gyms_in_city(
        self,
        session: AsyncSession,
        city_name: str,
        state: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Find all gyms within a city's boundaries using PostGIS

        Args:
            session: Database session
            city_name: Name of the city
            state: Optional state abbreviation for disambiguation
            limit: Maximum number of results

        Returns:
            List of gyms within the city boundaries
        """
        # First, geocode the city to get coordinates
        location_str = f"{city_name}, {state}" if state else city_name
        geocode_result = await self.geocoding_service.search_location(location_str)

        if not geocode_result:
            logger.warning(f"Could not geocode city: {location_str}")
            return []

        # For now, we'll use a radius-based approach from city center
        # In a full implementation, you would query actual city boundaries
        # from a PostGIS table containing city polygons

        query = text(
            """
            SELECT
                g.id,
                g.name,
                g.address,
                ST_X(g.location::geometry) as longitude,
                ST_Y(g.location::geometry) as latitude,
                g.phone,
                g.website,
                g.instagram,
                g.confidence,
                g.match_confidence,
                g.rating,
                g.review_count,
                g.source_city,
                g.metropolitan_area_code,
                ST_Distance(
                    g.location::geography,
                    ST_MakePoint(:lng, :lat)::geography
                ) / 1609.34 as distance_miles
            FROM gyms g
            WHERE g.source_city ILIKE :city_pattern
               OR ST_DWithin(
                    g.location::geography,
                    ST_MakePoint(:lng, :lat)::geography,
                    :radius_meters
                )
            ORDER BY distance_miles
            LIMIT :limit
        """
        )

        # Use a 15-mile radius for city searches (covers most city areas)
        radius_meters = 15 * 1609.34

        result = await session.execute(
            query,
            {
                "city_pattern": f"%{city_name}%",
                "lat": geocode_result["latitude"],
                "lng": geocode_result["longitude"],
                "radius_meters": radius_meters,
                "limit": limit,
            },
        )

        gyms = []
        for row in result:
            gym_dict = {
                "id": str(row.id),
                "name": row.name,
                "address": row.address,
                "coordinates": {"latitude": row.latitude, "longitude": row.longitude},
                "phone": row.phone,
                "website": row.website,
                "instagram": row.instagram,
                "confidence": row.confidence,
                "match_confidence": row.match_confidence,
                "rating": row.rating,
                "review_count": row.review_count,
                "source_city": row.source_city,
                "metropolitan_area_code": row.metropolitan_area_code,
                "distance_miles": round(row.distance_miles, 2),
            }
            gyms.append(gym_dict)

        return gyms

    async def find_gyms_near_location(
        self,
        session: AsyncSession,
        latitude: float,
        longitude: float,
        radius_miles: float = 10.0,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Find gyms within a radius of a specific coordinate

        Args:
            session: Database session
            latitude: Center point latitude
            longitude: Center point longitude
            radius_miles: Search radius in miles
            limit: Maximum number of results

        Returns:
            List of gyms within the specified radius
        """
        query = text(
            """
            SELECT
                g.id,
                g.name,
                g.address,
                ST_X(g.location::geometry) as longitude,
                ST_Y(g.location::geometry) as latitude,
                g.phone,
                g.website,
                g.instagram,
                g.confidence,
                g.match_confidence,
                g.rating,
                g.review_count,
                g.source_city,
                g.metropolitan_area_code,
                ST_Distance(
                    g.location::geography,
                    ST_MakePoint(:lng, :lat)::geography
                ) / 1609.34 as distance_miles
            FROM gyms g
            WHERE ST_DWithin(
                g.location::geography,
                ST_MakePoint(:lng, :lat)::geography,
                :radius_meters
            )
            ORDER BY distance_miles
            LIMIT :limit
        """
        )

        radius_meters = radius_miles * 1609.34

        result = await session.execute(
            query,
            {
                "lat": latitude,
                "lng": longitude,
                "radius_meters": radius_meters,
                "limit": limit,
            },
        )

        gyms = []
        for row in result:
            gym_dict = {
                "id": str(row.id),
                "name": row.name,
                "address": row.address,
                "coordinates": {"latitude": row.latitude, "longitude": row.longitude},
                "phone": row.phone,
                "website": row.website,
                "instagram": row.instagram,
                "confidence": row.confidence,
                "match_confidence": row.match_confidence,
                "rating": row.rating,
                "review_count": row.review_count,
                "source_city": row.source_city,
                "metropolitan_area_code": row.metropolitan_area_code,
                "distance_miles": round(row.distance_miles, 2),
            }
            gyms.append(gym_dict)

        return gyms

    async def get_city_stats(
        self, session: AsyncSession, city_name: str, state: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get statistics about gyms in a city

        Args:
            session: Database session
            city_name: Name of the city
            state: Optional state abbreviation

        Returns:
            Dictionary with city statistics
        """
        # Geocode the city
        location_str = f"{city_name}, {state}" if state else city_name
        geocode_result = await self.geocoding_service.search_location(location_str)

        if not geocode_result:
            return {
                "city": city_name,
                "state": state,
                "total_gyms": 0,
                "avg_confidence": 0,
                "avg_rating": 0,
            }

        query = text(
            """
            SELECT
                COUNT(*) as total_gyms,
                AVG(g.confidence) as avg_confidence,
                AVG(g.rating) FILTER (WHERE g.rating IS NOT NULL) as avg_rating,
                COUNT(DISTINCT g.source_city) as unique_cities
            FROM gyms g
            WHERE g.source_city ILIKE :city_pattern
               OR ST_DWithin(
                    g.location::geography,
                    ST_MakePoint(:lng, :lat)::geography,
                    :radius_meters
                )
        """
        )

        radius_meters = 15 * 1609.34  # 15-mile radius for city

        result = await session.execute(
            query,
            {
                "city_pattern": f"%{city_name}%",
                "lat": geocode_result["latitude"],
                "lng": geocode_result["longitude"],
                "radius_meters": radius_meters,
            },
        )

        row = result.first()

        return {
            "city": city_name,
            "state": state,
            "coordinates": {
                "latitude": geocode_result["latitude"],
                "longitude": geocode_result["longitude"],
            },
            "total_gyms": row.total_gyms or 0,
            "avg_confidence": float(row.avg_confidence or 0),
            "avg_rating": float(row.avg_rating or 0) if row.avg_rating else None,
            "unique_source_cities": row.unique_cities or 0,
        }
