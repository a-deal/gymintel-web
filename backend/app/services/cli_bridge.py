"""
CLI Bridge Service - Import data from GymIntel CLI
Integrates the stable CLI tool with web application database
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add CLI services to Python path
CLI_PATH = Path(__file__).parent.parent.parent.parent.parent / "gymintel-cli" / "src"
sys.path.insert(0, str(CLI_PATH))

try:
    from metro_areas import get_metro_area, list_metro_areas
    from run_gym_search import run_gym_search, run_metro_search

    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False
    print("Warning: CLI services not available. Ensure gymintel-cli is accessible.")


class CLIBridgeService:
    """Service to bridge CLI tool with web application"""

    def __init__(self):
        self.cli_available = CLI_AVAILABLE

    async def search_gyms_via_cli(
        self, zipcode: str, radius: float = 10.0, use_google: bool = True
    ) -> Dict[str, Any]:
        """
        Execute gym search using CLI and return structured results

        Args:
            zipcode: ZIP code to search
            radius: Search radius in miles
            use_google: Whether to use Google Places API

        Returns:
            Dict with search results compatible with GraphQL schema
        """
        if not self.cli_available:
            raise RuntimeError("CLI services not available")

        # Run CLI search in thread pool to avoid blocking
        loop = asyncio.get_event_loop()

        def run_search():
            return run_gym_search(
                zipcode=zipcode,
                radius=radius,
                use_google=use_google,
                quiet=True,  # Suppress CLI output
            )

        # Execute CLI search asynchronously
        result = await loop.run_in_executor(None, run_search)

        if "error" in result:
            raise ValueError(f"CLI search failed: {result['error']}")

        return self._transform_cli_result(result)

    async def search_metro_via_cli(
        self, metro_code: str, radius: float = 10.0, sample_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute metropolitan area search using CLI

        Args:
            metro_code: Metropolitan area code (e.g., 'nyc', 'la')
            radius: Search radius in miles
            sample_size: Limit number of ZIP codes for testing

        Returns:
            Dict with metro search results
        """
        if not self.cli_available:
            raise RuntimeError("CLI services not available")

        loop = asyncio.get_event_loop()

        def run_metro():
            return run_metro_search(
                metro_code=metro_code,
                radius=radius,
                sample_size=sample_size,
                use_google=True,
                max_workers=4,
            )

        result = await loop.run_in_executor(None, run_metro)

        if "error" in result:
            raise ValueError(f"CLI metro search failed: {result['error']}")

        return self._transform_metro_result(result, metro_code)

    async def get_metro_areas(self) -> List[Dict[str, Any]]:
        """Get list of available metropolitan areas from CLI"""
        if not self.cli_available:
            return []

        metro_codes = list_metro_areas()
        metro_areas = []

        for code in metro_codes:
            metro = get_metro_area(code)
            if metro:
                metro_areas.append(
                    {
                        "code": metro.code,
                        "name": metro.name,
                        "description": metro.description,
                        "state": metro.state,
                        "population": metro.population,
                        "density_category": metro.density_category,
                        "market_characteristics": metro.market_characteristics,
                        "zip_codes": metro.zip_codes,
                    }
                )

        return metro_areas

    def _transform_cli_result(self, cli_result: Dict[str, Any]) -> Dict[str, Any]:
        """Transform CLI search result to web app format"""
        search_info = cli_result.get("search_info", {})
        gyms = cli_result.get("gyms", [])

        # Transform gym data
        transformed_gyms = []
        for gym in gyms:
            transformed_gym = {
                "name": gym.get("name", ""),
                "address": gym.get("address", ""),
                "phone": gym.get("phone"),
                "website": gym.get("website"),
                "instagram": gym.get("instagram"),
                "latitude": gym.get("latitude", 0.0),
                "longitude": gym.get("longitude", 0.0),
                "rating": gym.get("rating"),
                "review_count": gym.get("review_count", 0),
                "confidence": gym.get("match_confidence", 0.0),
                "sources": self._extract_sources(gym),
                "source_zipcode": search_info.get("zipcode"),
                "raw_data": gym,  # Store original CLI data
            }
            transformed_gyms.append(transformed_gym)

        return {
            "search_info": {
                "zipcode": search_info.get("zipcode"),
                "coordinates": search_info.get("coordinates", {}),
                "radius_miles": search_info.get("radius_miles", 10.0),
                "timestamp": search_info.get("timestamp"),
                "total_results": search_info.get("total_results", 0),
                "yelp_results": search_info.get("yelp_results", 0),
                "google_results": search_info.get("google_results", 0),
                "merged_count": search_info.get("merged_count", 0),
                "avg_confidence": search_info.get("avg_confidence", "0%"),
                "use_google": search_info.get("use_google", True),
            },
            "gyms": transformed_gyms,
        }

    def _transform_metro_result(
        self, cli_result: Dict[str, Any], metro_code: str
    ) -> Dict[str, Any]:
        """Transform CLI metro search result to web app format"""
        metro_info = cli_result.get("metro_info", {})
        all_gyms = cli_result.get("all_gyms", [])
        zip_results = cli_result.get("zip_results", {})

        # Transform all gyms
        transformed_gyms = []
        for gym in all_gyms:
            transformed_gym = {
                "name": gym.get("name", ""),
                "address": gym.get("address", ""),
                "phone": gym.get("phone"),
                "website": gym.get("website"),
                "instagram": gym.get("instagram"),
                "latitude": gym.get("latitude", 0.0),
                "longitude": gym.get("longitude", 0.0),
                "rating": gym.get("rating"),
                "review_count": gym.get("review_count", 0),
                "confidence": gym.get("match_confidence", 0.0),
                "sources": self._extract_sources(gym),
                "source_zipcode": gym.get("source_zipcode"),
                "metropolitan_area_code": metro_code,
                "raw_data": gym,
            }
            transformed_gyms.append(transformed_gym)

        return {
            "metro_info": metro_info,
            "gyms": transformed_gyms,
            "zip_results": zip_results,
            "statistics": metro_info.get("statistics", {}),
        }

    def _extract_sources(self, gym: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract data sources from CLI gym record"""
        sources = []

        # Get source information
        source_name = gym.get("source", "Unknown")
        confidence = gym.get("match_confidence", 0.0)

        if "Merged" in source_name:
            # Merged record has multiple sources
            if gym.get("sources"):
                for source in gym["sources"]:
                    sources.append(
                        {
                            "name": source,
                            "confidence": confidence,
                            "last_updated": datetime.utcnow().isoformat(),
                        }
                    )
            else:
                # Fallback for merged records
                sources.extend(
                    [
                        {
                            "name": "Yelp",
                            "confidence": confidence,
                            "last_updated": datetime.utcnow().isoformat(),
                        },
                        {
                            "name": "Google Places",
                            "confidence": confidence,
                            "last_updated": datetime.utcnow().isoformat(),
                        },
                    ]
                )
        else:
            # Single source record
            sources.append(
                {
                    "name": source_name,
                    "confidence": confidence if confidence > 0 else 1.0,
                    "last_updated": datetime.utcnow().isoformat(),
                }
            )

        return sources


# Global service instance
cli_bridge_service = CLIBridgeService()
