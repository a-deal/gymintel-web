"""
Metropolitan area database models
"""

import uuid
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

# Import Base from gym module
from .gym import Base


class MetropolitanArea(Base):
    """Metropolitan Statistical Area (MSA) information"""

    __tablename__ = "metropolitan_areas"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # MSA identification
    code = Column(String(20), unique=True, nullable=False, index=True)  # CBSA code
    name = Column(String(255), nullable=False, index=True)
    title = Column(String(500), nullable=False)  # Full official title

    # Geographic boundaries (PostGIS geometry)
    boundary = Column(Geometry("MULTIPOLYGON", srid=4326), nullable=True)
    center_point = Column(Geometry("POINT", srid=4326), nullable=True)

    # Demographics and statistics
    population = Column(Integer, nullable=True)
    land_area_sq_miles = Column(Float, nullable=True)
    population_density = Column(Float, nullable=True)

    # Economic indicators
    median_household_income = Column(Float, nullable=True)
    unemployment_rate = Column(Float, nullable=True)

    # Gym market intelligence
    total_gyms = Column(Integer, nullable=True, default=0)
    gym_density_per_10k = Column(Float, nullable=True)  # Gyms per 10,000 people
    market_saturation_score = Column(Float, nullable=True)  # 0.0-1.0

    # Data freshness
    census_year = Column(Integer, nullable=True)
    last_gym_count_update = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<MetropolitanArea(code='{self.code}', name='{self.name}')>"
