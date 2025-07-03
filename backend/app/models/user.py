"""
User and saved search database models
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# Import Base from gym module
from .gym import Base


class User(Base):
    """User accounts for saved searches and preferences"""

    __tablename__ = "users"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Profile information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    # Preferences
    default_search_radius = Column(String(20), nullable=True, default="25")  # miles
    email_notifications = Column(Boolean, default=True, nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    last_login = Column(DateTime, nullable=True)

    # Relationships
    saved_searches = relationship(
        "SavedSearch", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class SavedSearch(Base):
    """User's saved gym searches and alert preferences"""

    __tablename__ = "saved_searches"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Search parameters
    name = Column(String(100), nullable=False)  # User-defined name
    location = Column(String(100), nullable=False, index=True)  # City name or zipcode
    radius = Column(String(20), nullable=False, default="25")  # miles

    # Resolved location coordinates (cached from geocoding)
    resolved_latitude = Column(Float, nullable=True)
    resolved_longitude = Column(Float, nullable=True)

    # Filters (stored as JSON)
    filters = Column(JSON, nullable=True)  # rating, price range, amenities, etc.

    # Alert settings
    alert_enabled = Column(Boolean, default=False, nullable=False)
    alert_frequency = Column(String(20), nullable=True)  # "daily", "weekly", "monthly"
    last_alert_sent = Column(DateTime, nullable=True)

    # Search results cache
    last_search_date = Column(DateTime, nullable=True)
    gym_count = Column(String(50), nullable=True)  # e.g., "45 gyms found"

    # Notes
    notes = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="saved_searches")

    # Table constraints
    __table_args__ = (
        CheckConstraint(
            "resolved_latitude IS NULL OR "
            "(resolved_latitude >= -90 AND resolved_latitude <= 90)",
            name="valid_latitude",
        ),
        CheckConstraint(
            "resolved_longitude IS NULL OR "
            "(resolved_longitude >= -180 AND resolved_longitude <= 180)",
            name="valid_longitude",
        ),
    )

    def __repr__(self):
        return f"<SavedSearch(name='{self.name}', location='{self.location}')>"
