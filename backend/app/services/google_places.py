"""
Google Places API Service for location validation and autocomplete
"""

import logging
from typing import Dict, List, Optional, Tuple

import httpx
from pydantic import BaseModel

from ..config import settings

logger = logging.getLogger(__name__)


class PlaceDetails(BaseModel):
    """Structured place details from Google Places API"""

    place_id: str
    name: str
    formatted_address: str
    types: List[str]
    latitude: float
    longitude: float
    country: Optional[str] = None
    administrative_area_level_1: Optional[str] = None  # State/Province
    administrative_area_level_2: Optional[str] = None  # County
    locality: Optional[str] = None  # City
    postal_code: Optional[str] = None


class GooglePlacesService:
    """Service for interacting with Google Places API"""

    def __init__(self):
        self.api_key = settings.google_places_api_key
        # Using the new Places API endpoints
        self.base_url = "https://places.googleapis.com/v1"
        self.legacy_base_url = "https://maps.googleapis.com/maps/api/place"
        self.geocoding_url = "https://maps.googleapis.com/maps/api/geocode"
        self.client = httpx.AsyncClient(timeout=10.0)

    async def autocomplete_cities(
        self, input_text: str, country: str = "us"
    ) -> List[Dict[str, any]]:
        """
        Get city autocomplete suggestions

        Args:
            input_text: User's input text
            country: ISO 3166-1 alpha-2 country code (default: "us")

        Returns:
            List of city suggestions with place_id and description
        """
        if not self.api_key:
            logger.warning("Google Places API key not configured")
            return []

        try:
            # New Places API uses different endpoint and format
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "suggestions.placePrediction.placeId,suggestions.placePrediction.text,suggestions.placePrediction.structuredFormat",  # noqa: E501
            }

            body = {
                "input": input_text,
                "includedPrimaryTypes": ["locality", "administrative_area_level_3"],
                "includedRegionCodes": [country.upper()],
                "languageCode": "en-US",
            }

            response = await self.client.post(
                f"{self.base_url}/places:autocomplete", headers=headers, json=body
            )
            response.raise_for_status()

            data = response.json()

            # New API doesn't have status field, check for error
            if "error" in data:
                error_message = data["error"].get("message", "")
                error_code = data["error"].get("code", "UNKNOWN")
                logger.error(
                    f"Google Places API (New) error: {error_code} - {error_message}"
                )
                return []

            # Format predictions for easier consumption
            predictions = []
            suggestions = data.get("suggestions", [])

            for suggestion in suggestions:
                place_prediction = suggestion.get("placePrediction", {})
                if place_prediction:
                    text_info = place_prediction.get("text", {})
                    structured = place_prediction.get("structuredFormat", {})

                    predictions.append(
                        {
                            "place_id": place_prediction.get("placeId", ""),
                            "description": text_info.get("text", ""),
                            "main_text": structured.get("mainText", {}).get("text", ""),
                            "secondary_text": structured.get("secondaryText", {}).get(
                                "text", ""
                            ),
                        }
                    )

            return predictions

        except Exception as e:
            logger.error(f"Error calling Google Places Autocomplete API: {e}")
            return []

    async def get_place_details(self, place_id: str) -> Optional[PlaceDetails]:
        """
        Get detailed information about a place

        Args:
            place_id: Google Places ID

        Returns:
            PlaceDetails object or None if not found
        """
        if not self.api_key:
            logger.warning("Google Places API key not configured")
            return None

        try:
            # New Places API format for place details
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "id,displayName,formattedAddress,location,addressComponents,types",  # noqa: E501
            }

            response = await self.client.get(
                f"{self.base_url}/places/{place_id}", headers=headers
            )
            response.raise_for_status()

            data = response.json()

            # New API error handling
            if "error" in data:
                error_message = data["error"].get("message", "")
                error_code = data["error"].get("code", "UNKNOWN")
                logger.error(
                    f"Google Places Details API error: {error_code} - {error_message}"
                )
                return None

            # Parse address components with new format
            components = {}
            for component in data.get("addressComponents", []):
                types = component.get("types", [])
                if "country" in types:
                    components["country"] = component.get("shortText", "")
                elif "administrative_area_level_1" in types:
                    components["administrative_area_level_1"] = component.get(
                        "shortText", ""
                    )
                elif "administrative_area_level_2" in types:
                    components["administrative_area_level_2"] = component.get(
                        "longText", ""
                    )
                elif "locality" in types:
                    components["locality"] = component.get("longText", "")
                elif "postal_code" in types:
                    components["postal_code"] = component.get("shortText", "")

            return PlaceDetails(
                place_id=data.get("id", place_id),
                name=data.get("displayName", {}).get("text", ""),
                formatted_address=data.get("formattedAddress", ""),
                types=data.get("types", []),
                latitude=data.get("location", {}).get("latitude", 0.0),
                longitude=data.get("location", {}).get("longitude", 0.0),
                **components,
            )

        except Exception as e:
            logger.error(f"Error calling Google Places Details API: {e}")
            return None

    async def validate_city_input(
        self, input_text: str, country: str = "us"
    ) -> Tuple[bool, Optional[PlaceDetails]]:
        """
        Validate if input is a valid city name and get details

        Args:
            input_text: User's input text
            country: ISO 3166-1 alpha-2 country code

        Returns:
            Tuple of (is_valid, place_details)
        """
        # First, try autocomplete to see if it matches a city
        suggestions = await self.autocomplete_cities(input_text, country)

        if not suggestions:
            return False, None

        # If we have exact match in main_text, use it
        for suggestion in suggestions:
            if suggestion["main_text"].lower() == input_text.lower():
                details = await self.get_place_details(suggestion["place_id"])
                if details and "locality" in details.types:
                    return True, details

        # Otherwise, use the first suggestion if it's reasonably close
        if suggestions:
            first_suggestion = suggestions[0]
            # Check if the input is a reasonable prefix of the suggestion
            if first_suggestion["main_text"].lower().startswith(input_text.lower()):
                details = await self.get_place_details(first_suggestion["place_id"])
                if details and "locality" in details.types:
                    return True, details

        return False, None

    async def geocode_address(self, address: str) -> Optional[Dict[str, float]]:
        """
        Geocode an address to get coordinates

        Args:
            address: Address string to geocode

        Returns:
            Dict with latitude and longitude or None
        """
        if not self.api_key:
            logger.warning("Google Places API key not configured")
            return None

        try:
            params = {
                "address": address,
                "key": self.api_key,
            }

            response = await self.client.get(
                f"{self.geocoding_url}/json", params=params
            )
            response.raise_for_status()

            data = response.json()

            if data.get("status") != "OK" or not data.get("results"):
                logger.error(f"Google Geocoding API error: {data.get('status')}")
                return None

            location = data["results"][0]["geometry"]["location"]
            return {
                "latitude": location["lat"],
                "longitude": location["lng"],
            }

        except Exception as e:
            logger.error(f"Error calling Google Geocoding API: {e}")
            return None

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Create a singleton instance
google_places_service = GooglePlacesService()
