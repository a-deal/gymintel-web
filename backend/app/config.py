"""
Application configuration using Pydantic settings
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    app_name: str = "GymIntel API"
    version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False

    # Database
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "gymintel"
    database_user: str = "gymintel"
    database_password: str = "gymintel_dev"
    database_url: Optional[str] = None

    # Test Database
    test_database_host: str = "localhost"
    test_database_port: int = 5432
    test_database_name: str = "test_gymintel"
    test_database_user: str = "gymintel_test"
    test_database_password: str = "gymintel_test"
    test_database_url: Optional[str] = None

    # API Keys
    yelp_api_key: Optional[str] = None
    google_places_api_key: Optional[str] = None
    mapbox_access_token: Optional[str] = None

    # Security
    secret_key: str = "your-secret-key-here"
    jwt_secret_key: str = "your-jwt-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # CORS
    frontend_url: str = "http://localhost:3000"

    # Redis (optional)
    redis_url: Optional[str] = None

    model_config = {"env_file": ".env", "case_sensitive": False}

    @property
    def async_database_url(self) -> str:
        """Get async database URL, building from components if needed"""
        if self.database_url:
            # Convert postgresql:// to postgresql+asyncpg://
            if self.database_url.startswith("postgresql://"):
                return self.database_url.replace(
                    "postgresql://", "postgresql+asyncpg://"
                )
            return self.database_url

        # Build from components
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def async_test_database_url(self) -> str:
        """Get async test database URL, building from components if needed"""
        if self.test_database_url:
            # Convert postgresql:// to postgresql+asyncpg://
            if self.test_database_url.startswith("postgresql://"):
                return self.test_database_url.replace(
                    "postgresql://", "postgresql+asyncpg://"
                )
            return self.test_database_url

        # Build from components
        return (
            f"postgresql+asyncpg://"
            f"{self.test_database_user}:{self.test_database_password}"
            f"@{self.test_database_host}:{self.test_database_port}"
            f"/{self.test_database_name}"
        )

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"

    @property
    def is_testing(self) -> bool:
        """Check if running tests"""
        return self.environment.lower() == "testing"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Create a singleton instance
settings = get_settings()
