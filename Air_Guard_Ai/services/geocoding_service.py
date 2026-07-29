"""
Geocoding Service using Open-Meteo Geocoding API with In-Memory TTL Caching
"""
import time
import httpx
from typing import Dict, Any, Optional
from config import GEOCODING_API_URL, CACHE_TTL_SECONDS

class GeocodingService:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    async def get_coordinates(self, city_name: str) -> Optional[Dict[str, Any]]:
        normalized_city = city_name.strip().lower()
        now = time.time()

        # Check cache
        if normalized_city in self._cache:
            cached_data, timestamp = self._cache[normalized_city]["data"], self._cache[normalized_city]["timestamp"]
            if now - timestamp < CACHE_TTL_SECONDS:
                return cached_data

        # Fetch from Open-Meteo Geocoding API
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    GEOCODING_API_URL,
                    params={"name": city_name, "count": 1, "language": "en", "format": "json"}
                )
                response.raise_for_status()
                data = response.json()

                if "results" in data and len(data["results"]) > 0:
                    result = data["results"][0]
                    location_info = {
                        "name": result.get("name"),
                        "latitude": result.get("latitude"),
                        "longitude": result.get("longitude"),
                        "country": result.get("country", ""),
                        "country_code": result.get("country_code", ""),
                        "admin1": result.get("admin1", ""),
                        "timezone": result.get("timezone", "UTC")
                    }
                    # Save to cache
                    self._cache[normalized_city] = {
                        "data": location_info,
                        "timestamp": now
                    }
                    return location_info
            except Exception as e:
                print(f"[GeocodingService Error] Failed to geocode '{city_name}': {e}")
                return None

        return None

geocoding_service = GeocodingService()
