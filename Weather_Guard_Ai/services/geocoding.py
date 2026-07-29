"""
WeatherWise AI - Geocoding Service
Converts city names to latitude and longitude using Open-Meteo Geocoding API.
"""

import time
import requests
import logging
from typing import Tuple, Dict, Any, Optional
from config import GEOCODING_API_URL, DEFAULT_CITY, DEFAULT_LATITUDE, DEFAULT_LONGITUDE, GEOCODE_CACHE_TTL

logger = logging.getLogger("WeatherWise.Geocoding")

# Simple in-memory cache for geocoding queries
_GEOCODE_CACHE: Dict[str, Tuple[Dict[str, Any], float]] = {}


def geocode_city(city_name: str) -> Dict[str, Any]:
    """
    Geocodes a city name into latitude, longitude, country, and timezone.
    
    Args:
        city_name: Name of the city to convert.
        
    Returns:
        Dict containing latitude, longitude, name, country, and timezone.
    """
    clean_name = city_name.strip()
    cache_key = clean_name.lower()
    
    # Check cache
    now = time.time()
    if cache_key in _GEOCODE_CACHE:
        cached_data, timestamp = _GEOCODE_CACHE[cache_key]
        if now - timestamp < GEOCODE_CACHE_TTL:
            logger.info(f"Geocoding cache hit for '{clean_name}'")
            return cached_data

    params = {
        "name": clean_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(GEOCODING_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("results") and len(data["results"]) > 0:
            result = data["results"][0]
            parsed = {
                "name": result.get("name", clean_name),
                "latitude": float(result.get("latitude")),
                "longitude": float(result.get("longitude")),
                "country": result.get("country", "Unknown"),
                "admin1": result.get("admin1", ""),
                "timezone": result.get("timezone", "auto")
            }
            # Update cache
            _GEOCODE_CACHE[cache_key] = (parsed, now)
            logger.info(f"Geocoded '{clean_name}' to Lat: {parsed['latitude']}, Lon: {parsed['longitude']}")
            return parsed
        else:
            logger.warning(f"City '{clean_name}' not found in Open-Meteo Geocoding API. Falling back to default.")
            return _fallback_location(clean_name)
            
    except Exception as e:
        logger.error(f"Geocoding error for '{clean_name}': {e}. Using fallback.")
        return _fallback_location(clean_name)


def reverse_geocode_label(lat: float, lon: float) -> str:
    """Provides a display label for latitude/longitude coordinates."""
    return f"Coordinates ({lat:.2f}°, {lon:.2f}°)"


def _fallback_location(attempted_name: str) -> Dict[str, Any]:
    """Fallback location details when geocoding fails."""
    return {
        "name": attempted_name.capitalize() if attempted_name else DEFAULT_CITY,
        "latitude": DEFAULT_LATITUDE,
        "longitude": DEFAULT_LONGITUDE,
        "country": "India",
        "admin1": "Tamil Nadu",
        "timezone": "Asia/Kolkata"
    }
