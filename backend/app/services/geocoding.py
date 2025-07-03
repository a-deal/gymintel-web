"""
Geocoding service for converting cities to coordinates and location information.
"""

import logging
import re
import ssl
from typing import List, Optional, Tuple

import certifi
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim

from ..config import settings
from .google_places import google_places_service

logger = logging.getLogger(__name__)


class GeocodingService:
    """Service for geocoding operations."""

    def __init__(self, timeout: int = 10):
        """Initialize the geocoding service.

        Args:
            timeout: Timeout in seconds for geocoding requests (default: 10)
        """
        # Create SSL context with proper certificates
        ctx = ssl.create_default_context(cafile=certifi.where())

        self.geolocator = Nominatim(
            user_agent="gymintel-web/1.0", timeout=timeout, ssl_context=ctx
        )

        # TODO: Make country codes configurable for international support
        # Currently hardcoded to US only in search methods
        # Future enhancement:
        # 1. Add country_codes parameter to __init__ (default: ["us"])
        # 2. Store as instance variable: self.country_codes
        # 3. Update search_location to use self.country_codes
        # 4. Make country suffix dynamic based on country_codes
        # 5. Support multiple countries for global gym search

    async def search_location(self, query: str) -> Optional[dict]:
        """
        Search for a location by city name.

        Args:
            query: City name

        Returns:
            Dict with location info including coordinates, city, state, etc.
        """
        # Check if query is a zipcode (for backward compatibility)
        if self._is_zipcode(query):
            return await self._get_location_from_zipcode(query)

        # If Google Places API is configured, try it first for city validation
        if settings.google_places_api_key:
            try:
                is_valid, place_details = (
                    await google_places_service.validate_city_input(query)
                )
                if is_valid and place_details:
                    logger.info(f"Google Places validated city: {place_details.name}")
                    return {
                        "latitude": place_details.latitude,
                        "longitude": place_details.longitude,
                        "display_name": place_details.formatted_address,
                        "city": place_details.locality or place_details.name,
                        "state": place_details.administrative_area_level_1,
                        "google_place_id": place_details.place_id,
                        "postal_code": place_details.postal_code,
                    }
            except Exception as e:
                logger.error(f"Google Places API error: {e}")
                # Fall back to Nominatim

        # Otherwise, try to find city using Nominatim
        _, location_info = await self._get_zipcode_from_city(query)
        return location_info

    def _is_zipcode(self, query: str) -> bool:
        """Check if the query is a US zipcode."""
        # US zipcode pattern: 5 digits or 5+4 format
        zipcode_pattern = r"^\d{5}(-\d{4})?$"
        return bool(re.match(zipcode_pattern, query.strip()))

    async def _get_location_from_zipcode(self, zipcode: str) -> Optional[dict]:
        """Get location information from a zipcode."""
        try:
            location = self.geolocator.geocode(f"{zipcode}, USA", addressdetails=True)

            if location:
                return {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "display_name": location.address,
                    "city": self._extract_city(location.raw.get("address", {})),
                    "state": location.raw.get("address", {}).get("state"),
                }

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Geocoding error for zipcode {zipcode}: {e}")

        return None

    async def _get_zipcode_from_city(
        self, city: str
    ) -> Tuple[Optional[str], Optional[dict]]:
        """Get zipcode from a city name."""
        try:
            # Add USA to improve accuracy
            query = f"{city}, USA" if "usa" not in city.lower() else city

            location = self.geolocator.geocode(
                query, addressdetails=True, country_codes=["us"]
            )

            if location:
                address = location.raw.get("address", {})
                zipcode = address.get("postcode")

                if zipcode:
                    # Clean zipcode (sometimes includes +4)
                    zipcode = zipcode.split("-")[0]

                    return zipcode, {
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                        "display_name": location.address,
                        "city": self._extract_city(address),
                        "state": address.get("state"),
                    }

                # If no zipcode in result, try to get representative zipcode
                # by searching for the city center
                logger.info(f"No zipcode found for {city}, using coordinates")
                return None, {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "display_name": location.address,
                    "city": self._extract_city(address),
                    "state": address.get("state"),
                }

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Geocoding error for city {city}: {e}")

        return None, None

    def _extract_city(self, address: dict) -> Optional[str]:
        """Extract city name from address components."""
        # Try different keys that might contain city name
        city_keys = ["city", "town", "village", "municipality", "suburb"]

        for key in city_keys:
            if key in address:
                return address[key]

        return None

    async def get_nearby_zipcodes(
        self, latitude: float, longitude: float, radius_miles: float = 10
    ) -> List[str]:
        """
        Get nearby zipcodes within a radius.

        This is a simplified implementation. In production, you'd want to use
        a proper ZIP code database or API.
        """
        # For now, return empty list
        # In a real implementation, this would query a ZIP code database
        return []


# Singleton instance
geocoding_service = GeocodingService()
