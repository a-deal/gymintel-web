"""
Geocoding service for converting cities to zipcodes and coordinates.
"""

import logging
import re
import ssl
from typing import List, Optional, Tuple

import certifi
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim

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

    async def search_location(self, query: str) -> Tuple[Optional[str], Optional[dict]]:
        """
        Search for a location by city name or zipcode.

        Args:
            query: City name or zipcode

        Returns:
            Tuple of (zipcode, location_info)
        """
        # Check if query is a zipcode
        if self._is_zipcode(query):
            return query, await self._get_location_from_zipcode(query)

        # Otherwise, try to find city
        return await self._get_zipcode_from_city(query)

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
                else:
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
