"""
Gym-related database models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from datetime import datetime

Base = declarative_base()


class Gym(Base):
    """Main gym entity with multi-source intelligence"""
    __tablename__ = "gyms"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic gym information
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=False)
    phone = Column(String(50), nullable=True)
    website = Column(String(500), nullable=True)
    instagram = Column(String(100), nullable=True)
    
    # Geographic data (PostGIS geometry)
    location = Column(Geometry('POINT', srid=4326), nullable=False, index=True)
    latitude = Column(Float, nullable=False)  # Denormalized for easier access
    longitude = Column(Float, nullable=False)
    
    # Intelligence scoring
    confidence = Column(Float, nullable=False, default=0.0)  # Overall confidence (0.0-1.0)
    match_confidence = Column(Float, nullable=False, default=0.0)  # Cross-source matching
    
    # Review aggregation
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True, default=0)
    
    # Metadata
    source_zipcode = Column(String(10), nullable=True, index=True)  # Origin ZIP for batch searches
    metropolitan_area_code = Column(String(20), nullable=True, index=True)
    raw_data = Column(JSON, nullable=True)  # Store original API responses
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    sources = relationship("DataSource", back_populates="gym", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="gym", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Gym(id={self.id}, name='{self.name}', confidence={self.confidence})>"


class DataSource(Base):
    """Data source information for gym records"""
    __tablename__ = "data_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gym_id = Column(UUID(as_uuid=True), ForeignKey("gyms.id"), nullable=False)
    
    # Source details
    name = Column(String(50), nullable=False)  # "Yelp", "Google Places", "Merged"
    confidence = Column(Float, nullable=False, default=0.0)
    source_id = Column(String(100), nullable=True)  # External API ID
    
    # Metadata
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    api_response = Column(JSON, nullable=True)  # Raw API response
    
    # Relationships
    gym = relationship("Gym", back_populates="sources")
    
    def __repr__(self):
        return f"<DataSource(name='{self.name}', confidence={self.confidence})>"


class Review(Base):
    """Aggregated review data from multiple sources"""
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gym_id = Column(UUID(as_uuid=True), ForeignKey("gyms.id"), nullable=False)
    
    # Review metrics
    rating = Column(Float, nullable=False)
    review_count = Column(Integer, nullable=False, default=1)
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    
    # Source information
    source = Column(String(50), nullable=False)
    source_url = Column(String(500), nullable=True)
    
    # Sample review text (for sentiment analysis)
    sample_review_text = Column(Text, nullable=True)
    
    # Metadata
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    gym = relationship("Gym", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(source='{self.source}', rating={self.rating}, count={self.review_count})>"