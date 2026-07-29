"""
WeatherWise AI - System Configuration
"""

import os

# Open-Meteo API Endpoints (No API key required)
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Default Agent Settings
AGENT_NAME = "weatherwise_agent"
AGENT_SEED = os.getenv("WEATHER_AGENT_SEED", "weatherwise_ai_agent_secret_seed_phrase_2026")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8000"))
WEB_PORT = int(os.getenv("WEB_PORT", "8080"))

# Default Location (Coimbatore, Tamil Nadu, India)
DEFAULT_CITY = "Coimbatore"
DEFAULT_LATITUDE = 11.0168
DEFAULT_LONGITUDE = 76.9558
DEFAULT_TIMEZONE = "auto"

# Cache TTL Settings (in seconds)
WEATHER_CACHE_TTL = 900  # 15 minutes
GEOCODE_CACHE_TTL = 86400  # 24 hours
