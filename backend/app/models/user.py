"""
User and saved search database models
"""

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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
    zipcode = Column(String(10), nullable=False, index=True)
    radius = Column(String(20), nullable=False, default="25")  # miles

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

    def __repr__(self):
        return f"<SavedSearch(name='{self.name}', zipcode='{self.zipcode}')>"
