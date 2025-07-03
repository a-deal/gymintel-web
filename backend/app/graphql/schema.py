"""
GymIntel GraphQL Schema
Advanced gym discovery platform with intelligent confidence scoring
"""

from datetime import datetime
from typing import List, Optional

import strawberry


@strawberry.type
class Coordinates:
    """Geographic coordinates for gym locations"""

    latitude: float
    longitude: float


@strawberry.type
class DataSource:
    """Data source information for gym records"""

    name: str  # "Yelp", "Google Places", "Merged"
    confidence: float
    last_updated: datetime


@strawberry.type
class Review:
    """Gym review data aggregated from multiple sources"""

    rating: float
    review_count: int
    sentiment_score: Optional[float] = None
    source: str
    last_updated: datetime


@strawberry.type
class Gym:
    """Core gym entity with multi-source intelligence"""

    id: strawberry.ID
    name: str
    address: str
    coordinates: Coordinates
    phone: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None

    # Intelligence data
    sources: List[DataSource]
    confidence: float  # Confidence score (0.0-1.0)
    match_confidence: float  # Cross-source matching confidence

    # Review aggregation
    rating: Optional[float] = None
    review_count: Optional[int] = None
    reviews: List[Review]

    # Metadata
    source_city: Optional[str] = None  # Origin city for batch searches
    metropolitan_area_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime


@strawberry.type
class MetroStatistics:
    """Statistical analysis for metropolitan areas"""

    total_gyms: int
    merged_gyms: int
    merge_rate: float
    average_confidence: float
    source_distribution: str  # JSON string of source counts
    gyms_per_zip: str  # JSON string of distribution stats
    deduplication_rate: float


@strawberry.type
class MetropolitanArea:
    """Metropolitan area with comprehensive gym data"""

    id: strawberry.ID
    name: str
    code: str
    description: str
    state: str
    population: Optional[int] = None
    density_category: str  # low, medium, high, very_high
    market_characteristics: List[str]
    cities: List[str]  # Cities within this metro area

    # Computed fields
    statistics: MetroStatistics


@strawberry.type
class SearchResult:
    """Results from gym search operations"""

    location: str  # City name or location searched
    coordinates: Coordinates
    radius_miles: float
    timestamp: datetime

    # Results
    gyms: List[Gym]
    total_results: int
    yelp_results: int
    google_results: int
    merged_count: int
    avg_confidence: float

    # Performance metrics
    execution_time_seconds: float
    use_google: bool


@strawberry.type
class GymAnalytics:
    """Advanced analytics for gym market analysis"""

    location: str  # City or area name
    total_gyms: int
    confidence_distribution: str  # JSON histogram
    source_breakdown: str  # JSON source counts
    rating_analysis: str  # JSON rating statistics
    density_score: float  # Gyms per square mile
    market_saturation: str  # low, medium, high


@strawberry.type
class MarketGap:
    """Identified market opportunities"""

    area_description: str
    coordinates: Coordinates
    gap_score: float  # 0.0-1.0, higher = better opportunity
    population_density: float
    nearest_gym_distance: float
    reasoning: str


@strawberry.type
class SearchProgress:
    """Real-time search progress updates"""

    search_id: str
    status: str  # pending, searching_yelp, searching_google, merging, complete, error
    progress_percentage: float
    current_step: str
    estimated_completion: Optional[datetime] = None
    message: Optional[str] = None
    location_info: Optional[str] = None  # JSON with city, state info


@strawberry.type
class ImportResult:
    """Results from CLI data import operations"""

    success: bool
    gyms_imported: int
    gyms_updated: int
    errors: List[str]
    import_duration_seconds: float


@strawberry.type
class SavedSearch:
    """User's saved search preferences"""

    id: strawberry.ID
    user_id: str
    location: str  # City name
    radius: float
    name: Optional[str] = None
    created_at: datetime
    last_run: Optional[datetime] = None


# Input Types
@strawberry.input
class GymDataInput:
    """Input for importing gym data from CLI"""

    name: str
    address: str
    latitude: float
    longitude: float
    phone: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    source: str
    confidence: float
    raw_data: str  # JSON string of original API response


@strawberry.input
class SearchFilters:
    """Advanced search filtering options"""

    min_rating: Optional[float] = None
    max_distance: Optional[float] = None
    min_confidence: Optional[float] = None
    sources: Optional[List[str]] = None
    has_website: Optional[bool] = None
    has_instagram: Optional[bool] = None


# Query Root
@strawberry.type
class CityAutocomplete:
    """City autocomplete suggestion"""

    place_id: str
    description: str
    main_text: str
    secondary_text: str


@strawberry.type
class Query:
    """GraphQL query operations"""

    @strawberry.field
    async def search_gyms(
        self,
        location: str,  # Can be zipcode or city name
        radius: float = 10.0,
        limit: int = 50,
        filters: Optional[SearchFilters] = None,
    ) -> SearchResult:
        """
        Search for gyms by location (city name).
        If no data exists, automatically fetches from external sources.
        """
        from .resolvers import GymResolvers

        return await GymResolvers.search_gyms_by_location(
            location, radius, limit, filters
        )

    @strawberry.field
    async def city_autocomplete(
        self, input_text: str, country: str = "us"
    ) -> List[CityAutocomplete]:
        """
        Get city autocomplete suggestions from Google Places API
        """
        from ..services.google_places import google_places_service

        suggestions = await google_places_service.autocomplete_cities(
            input_text, country
        )

        return [
            CityAutocomplete(
                place_id=s["place_id"],
                description=s["description"],
                main_text=s["main_text"],
                secondary_text=s["secondary_text"],
            )
            for s in suggestions
        ]

    @strawberry.field
    async def gym_by_id(self, gym_id: strawberry.ID) -> Optional[Gym]:
        """Get a specific gym by ID"""
        from .resolvers import GymResolvers

        return await GymResolvers.gym_by_id(str(gym_id))

    @strawberry.field
    async def metropolitan_area(self, code: str) -> Optional[MetropolitanArea]:
        """Get metropolitan area data by code (nyc, la, etc.)"""
        from .resolvers import MetroResolvers

        return await MetroResolvers.metropolitan_area(code)

    @strawberry.field
    async def list_metropolitan_areas(self) -> List[MetropolitanArea]:
        """List all available metropolitan areas"""
        from .resolvers import MetroResolvers

        return await MetroResolvers.list_metropolitan_areas()

    @strawberry.field
    async def gym_analytics(self, location: str) -> GymAnalytics:
        """Get comprehensive analytics for a city or area"""
        from .resolvers import GymResolvers

        return await GymResolvers.gym_analytics(location)

    @strawberry.field
    async def market_gap_analysis(
        self, location: str, radius: float = 10.0
    ) -> List[MarketGap]:
        """Identify potential market opportunities"""
        from .resolvers import GymResolvers

        return await GymResolvers.market_gap_analysis(location, radius)

    @strawberry.field
    async def gyms_by_metro(
        self, metro_code: str, limit: int = 100, offset: int = 0
    ) -> List[Gym]:
        """Get gyms within a metropolitan area with pagination"""
        from .resolvers import GymResolvers

        return await GymResolvers.gyms_by_metro(metro_code, limit, offset)


# Mutation Root
@strawberry.type
class Mutation:
    """GraphQL mutation operations"""

    @strawberry.field
    async def import_gym_data(
        self, location: str, data: List[GymDataInput]
    ) -> ImportResult:
        """Import gym data from CLI search results"""
        from .resolvers import MutationResolvers

        return await MutationResolvers.import_gym_data(location, data)

    @strawberry.field
    async def save_search(
        self, user_id: str, location: str, radius: float, name: Optional[str] = None
    ) -> SavedSearch:
        """Save a user's search preferences"""
        # TODO: Implement user search saving
        import uuid

        return SavedSearch(
            id=str(uuid.uuid4()),
            user_id=user_id,
            location=location,
            radius=radius,
            name=name,
            created_at=datetime.utcnow(),
            last_run=None,
        )

    @strawberry.field
    async def trigger_gym_search(self, location: str, radius: float = 10.0) -> str:
        """
        Trigger a gym search for a location (city).
        Returns a search_id to track progress via subscription.
        """
        from .resolvers import MutationResolvers

        return await MutationResolvers.trigger_gym_search(location, radius)


# Subscription Root
@strawberry.type
class Subscription:
    """GraphQL subscription operations for real-time updates"""

    @strawberry.subscription
    async def gym_updates(self, location: str) -> Gym:
        """Subscribe to gym data updates for a specific area"""
        # Real-time gym data changes
        # Placeholder implementation - would connect to real-time data source
        import asyncio

        await asyncio.sleep(1)
        # This is a placeholder that would never actually yield
        # In a real implementation, this would connect to a message queue or
        # database changes
        return  # This will never execute, but satisfies the type checker
        yield  # Unreachable code, but keeps the async generator signature

    @strawberry.subscription
    async def search_progress(self, search_id: str) -> SearchProgress:
        """Subscribe to search progress updates"""
        from ..services.search_progress import search_progress_manager

        try:
            # Subscribe to updates for this search
            queue = await search_progress_manager.subscribe(search_id)

            # Yield progress updates until complete
            while True:
                progress = await queue.get()
                yield progress

                # Stop when search is complete or errored
                if progress.status in ["complete", "error"]:
                    break

        except ValueError:
            # Search not found
            yield SearchProgress(
                search_id=search_id,
                status="error",
                progress_percentage=0.0,
                current_step="Search not found",
                message=f"Search ID {search_id} not found",
            )
        finally:
            # Clean up subscription
            if "queue" in locals():
                search_progress_manager.unsubscribe(search_id, queue)


# Schema definition
schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
