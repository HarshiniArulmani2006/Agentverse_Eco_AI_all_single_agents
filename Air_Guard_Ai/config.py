"""
AirGuard AI Configuration Settings & Thresholds
"""
import os

# Server Configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

# Open-Meteo Endpoints (Free, No API Key Required)
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
AIR_QUALITY_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Cache Configuration
CACHE_TTL_SECONDS = 900  # 15 Minutes Location/Data Cache

# uAgent Configuration
AGENT_NAME = "airguard_ai"
AGENT_SEED = os.getenv("AGENT_SEED", "airguard_ai_secret_seed_phrase_2026")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8001"))
AGENT_ENDPOINT = f"http://127.0.0.1:{AGENT_PORT}/submit"

# WHO Guideline Limits (24-Hour Mean in µg/m³, CO in mg/m³)
WHO_GUIDELINES = {
    "pm2_5": {"safe": 15.0, "critical": 35.0, "unit": "µg/m³"},
    "pm10": {"safe": 45.0, "critical": 75.0, "unit": "µg/m³"},
    "nitrogen_dioxide": {"safe": 25.0, "critical": 50.0, "unit": "µg/m³"},
    "sulphur_dioxide": {"safe": 40.0, "critical": 80.0, "unit": "µg/m³"},
    "ozone": {"safe": 100.0, "critical": 160.0, "unit": "µg/m³"},
    "carbon_monoxide": {"safe": 4.0, "critical": 10.0, "unit": "mg/m³"},  # converted to mg/m3 if needed
}

# US AQI Categories
AQI_CATEGORIES = [
    (50, "Excellent", "#10B981"),
    (100, "Good / Moderate", "#F59E0B"),
    (150, "Unhealthy for Sensitive Groups", "#F97316"),
    (200, "Unhealthy", "#EF4444"),
    (300, "Very Unhealthy", "#8B5CF6"),
    (500, "Hazardous / Emergency", "#7C3AED")
]
