"""
Air Quality Data Retrieval Service using Open-Meteo Air Quality API
"""
import time
import httpx
from typing import Dict, Any, Optional
from config import AIR_QUALITY_API_URL, CACHE_TTL_SECONDS

class AirQualityService:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    async def fetch_air_quality(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        cache_key = f"{round(latitude, 3)},{round(longitude, 3)}"
        now = time.time()

        if cache_key in self._cache:
            cached_entry = self._cache[cache_key]
            if now - cached_entry["timestamp"] < CACHE_TTL_SECONDS:
                return cached_entry["data"]

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "us_aqi", "european_aqi", "pm10", "pm2_5",
                "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide",
                "ozone", "aerosol_optical_depth", "dust", "uv_index"
            ],
            "hourly": [
                "us_aqi", "pm10", "pm2_5", "carbon_monoxide",
                "nitrogen_dioxide", "sulphur_dioxide", "ozone", "dust", "uv_index"
            ],
            "forecast_days": 7,
            "timezone": "auto"
        }

        async with httpx.AsyncClient(timeout=12.0) as client:
            try:
                response = await client.get(AIR_QUALITY_API_URL, params=params)
                response.raise_for_status()
                raw_data = response.json()

                current = raw_data.get("current", {})
                hourly = raw_data.get("hourly", {})

                processed_data = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "elevation": raw_data.get("elevation", 0),
                    "timezone": raw_data.get("timezone", "UTC"),
                    "current": {
                        "aqi": current.get("us_aqi", 0) or current.get("european_aqi", 0) or 0,
                        "us_aqi": current.get("us_aqi", 0),
                        "european_aqi": current.get("european_aqi", 0),
                        "pm2_5": current.get("pm2_5", 0.0),
                        "pm10": current.get("pm10", 0.0),
                        "co": current.get("carbon_monoxide", 0.0),
                        "no2": current.get("nitrogen_dioxide", 0.0),
                        "so2": current.get("sulphur_dioxide", 0.0),
                        "o3": current.get("ozone", 0.0),
                        "aod": current.get("aerosol_optical_depth", 0.0),
                        "dust": current.get("dust", 0.0),
                        "uv_index": current.get("uv_index", 0.0),
                        "pollen": round((current.get("pm10", 0) * 0.12), 1)  # Estimated pollen indicator
                    },
                    "hourly": hourly
                }

                self._cache[cache_key] = {
                    "data": processed_data,
                    "timestamp": now
                }
                return processed_data
            except Exception as e:
                print(f"[AirQualityService Error] Failed to fetch air quality for ({latitude}, {longitude}): {e}")
                return None

air_quality_service = AirQualityService()
