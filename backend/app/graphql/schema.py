"""
GymIntel GraphQL Schema
Advanced gym discovery platform with intelligent confidence scoring
"""

import strawberry
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass


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
    source_zipcode: Optional[str] = None  # Origin ZIP for batch searches
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
    zip_codes: List[str]
    
    # Computed fields
    statistics: MetroStatistics


@strawberry.type
class SearchResult:
    """Results from gym search operations"""
    zipcode: str
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
    zipcode: str
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
    status: str  # pending, searching_yelp, searching_google, merging, complete
    progress_percentage: float
    current_step: str
    estimated_completion: Optional[datetime] = None


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
    zipcode: str
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
class Query:
    """GraphQL query operations"""
    
    @strawberry.field
    async def search_gyms(
        self,
        zipcode: str,
        radius: float = 10.0,
        limit: int = 50,
        filters: Optional[SearchFilters] = None
    ) -> SearchResult:
        """Search for gyms in a specific area with intelligent filtering"""
        # Implementation will be in resolver
        pass
    
    @strawberry.field
    async def gym_by_id(self, gym_id: strawberry.ID) -> Optional[Gym]:
        """Get a specific gym by ID"""
        pass
    
    @strawberry.field
    async def metropolitan_area(self, code: str) -> Optional[MetropolitanArea]:
        """Get metropolitan area data by code (nyc, la, etc.)"""
        pass
    
    @strawberry.field
    async def list_metropolitan_areas(self) -> List[MetropolitanArea]:
        """List all available metropolitan areas"""
        pass
    
    @strawberry.field
    async def gym_analytics(self, zipcode: str) -> GymAnalytics:
        """Get comprehensive analytics for a ZIP code area"""
        pass
    
    @strawberry.field
    async def market_gap_analysis(
        self,
        zipcode: str,
        radius: float = 10.0
    ) -> List[MarketGap]:
        """Identify potential market opportunities"""
        pass
    
    @strawberry.field
    async def gyms_by_metro(
        self,
        metro_code: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[Gym]:
        """Get gyms within a metropolitan area with pagination"""
        pass


# Mutation Root  
@strawberry.type
class Mutation:
    """GraphQL mutation operations"""
    
    @strawberry.field
    async def import_gym_data(
        self,
        zipcode: str,
        data: List[GymDataInput]
    ) -> ImportResult:
        """Import gym data from CLI search results"""
        pass
    
    @strawberry.field
    async def save_search(
        self,
        user_id: str,
        zipcode: str,
        radius: float,
        name: Optional[str] = None
    ) -> SavedSearch:
        """Save a user's search preferences"""
        pass
    
    @strawberry.field
    async def trigger_cli_import(
        self,
        zipcode: str,
        radius: float = 10.0
    ) -> str:
        """Trigger a CLI search and import results (returns search_id)"""
        pass


# Subscription Root
@strawberry.type
class Subscription:
    """GraphQL subscription operations for real-time updates"""
    
    @strawberry.subscription
    async def gym_updates(self, zipcode: str):
        """Subscribe to gym data updates for a specific area"""
        # Real-time gym data changes
        yield  # Implementation with async generator
    
    @strawberry.subscription  
    async def search_progress(self, search_id: str):
        """Subscribe to search progress updates"""
        # Real-time progress for long-running searches
        yield  # Implementation with async generator


# Schema definition
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)