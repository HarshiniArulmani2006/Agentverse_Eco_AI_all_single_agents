"""
WildGuard AI – Application Configuration
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Gemini
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash", env="GEMINI_MODEL")

    # External APIs
    IUCN_API_TOKEN: str = Field(default="", env="IUCN_API_TOKEN")
    IUCN_BASE_URL: str = "https://apiv3.iucnredlist.org/api/v3"
    GBIF_BASE_URL: str = Field(default="https://api.gbif.org/v1", env="GBIF_BASE_URL")

    # App
    APP_HOST: str = Field(default="0.0.0.0", env="APP_HOST")
    APP_PORT: int = Field(default=8000, env="APP_PORT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    CORS_ORIGINS: str = Field(default="*", env="CORS_ORIGINS")

    # Data paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @property
    def SPECIES_DB_PATH(self) -> str:
        return os.path.join(self.BASE_DIR, "data", "species_db.json")

    @property
    def SIGHTINGS_DB_PATH(self) -> str:
        return os.path.join(self.BASE_DIR, "data", "sightings.json")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
