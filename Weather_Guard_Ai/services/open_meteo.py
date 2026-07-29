"""
WeatherWise AI - Open-Meteo Weather Data Service
Retrieves live weather telemetry, hourly, and 7-day forecasts from Open-Meteo API.
"""

import time
import requests
import logging
from typing import Dict, Any, Tuple, Optional, List
from config import WEATHER_API_URL, WEATHER_CACHE_TTL
from models.schema import WeatherMetrics, ForecastDay

logger = logging.getLogger("WeatherWise.OpenMeteo")

# In-memory weather cache: (lat_lon_key) -> (parsed_data, timestamp)
_WEATHER_CACHE: Dict[str, Tuple[Dict[str, Any], float]] = {}

# WMO Weather Code Mapping to human-readable condition descriptions
WMO_CODES: Dict[int, str] = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Dense Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Light Freezing Drizzle",
    57: "Dense Freezing Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Slight Snow Fall",
    73: "Moderate Snow Fall",
    75: "Heavy Snow Fall",
    77: "Snow Grains",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Slight Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail"
}


def get_wmo_condition(wmo_code: int) -> str:
    """Translates WMO weather code to human readable description."""
    return WMO_CODES.get(wmo_code, "Unknown Condition")


def fetch_weather_data(lat: float, lon: float, city_name: str, timezone: str = "auto") -> Dict[str, Any]:
    """
    Fetches live weather metrics, current conditions, hourly, and 7-day daily forecasts from Open-Meteo.
    
    Args:
        lat: Latitude
        lon: Longitude
        city_name: Display city name
        timezone: Timezone string or 'auto'
        
    Returns:
        Dict containing parsed WeatherMetrics, 7-day forecast list, and raw telemetry data.
    """
    cache_key = f"{lat:.3f}_{lon:.3f}"
    now = time.time()
    
    if cache_key in _WEATHER_CACHE:
        cached_data, timestamp = _WEATHER_CACHE[cache_key]
        if now - timestamp < WEATHER_CACHE_TTL:
            logger.info(f"Weather data cache hit for ({lat}, {lon})")
            # Update city name in cached response
            cached_data["metrics"]["city"] = city_name
            return cached_data

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "rain",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m"
        ],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "dew_point_2m",
            "apparent_temperature",
            "precipitation_probability",
            "precipitation",
            "weather_code",
            "visibility",
            "uv_index"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "sunrise",
            "sunset",
            "uv_index_max",
            "precipitation_probability_mean",
            "wind_speed_10m_max"
        ],
        "timezone": timezone
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=12)
        response.raise_for_status()
        data = response.json()

        parsed_metrics, forecast_7day = _parse_open_meteo_response(data, city_name, lat, lon)
        result = {
            "metrics": parsed_metrics.model_dump(),
            "forecast_7day": [f.model_dump() for f in forecast_7day],
            "raw": data
        }

        # Cache result
        _WEATHER_CACHE[cache_key] = (result, now)
        logger.info(f"Successfully fetched live weather data for {city_name} ({lat}, {lon})")
        return result

    except Exception as e:
        logger.error(f"Error fetching weather data from Open-Meteo for ({lat}, {lon}): {e}")
        return _generate_mock_fallback_weather(city_name, lat, lon)


def _parse_open_meteo_response(data: Dict[str, Any], city_name: str, lat: float, lon: float) -> Tuple[WeatherMetrics, List[ForecastDay]]:
    """Parses Open-Meteo raw JSON into structured WeatherMetrics and 7-Day ForecastDay models."""
    current = data.get("current", {})
    hourly = data.get("hourly", {})
    daily = data.get("daily", {})
    tz = data.get("timezone", "UTC")

    # Extracts current hourly index or first hour for hourly params like UV & Visibility & Rain Probability
    current_uv = 0.0
    current_visibility = 10000.0
    current_rain_prob = 0

    if hourly.get("uv_index") and len(hourly["uv_index"]) > 0:
        current_uv = float(hourly["uv_index"][0] or 0.0)
    if hourly.get("visibility") and len(hourly["visibility"]) > 0:
        current_visibility = float(hourly["visibility"][0] or 10000.0)
    if hourly.get("precipitation_probability") and len(hourly["precipitation_probability"]) > 0:
        current_rain_prob = int(hourly["precipitation_probability"][0] or 0)

    # Sunrise & Sunset
    sunrise_str = "06:00"
    sunset_str = "18:30"
    if daily.get("sunrise") and len(daily["sunrise"]) > 0:
        sunrise_str = str(daily["sunrise"][0]).split("T")[-1]
    if daily.get("sunset") and len(daily["sunset"]) > 0:
        sunset_str = str(daily["sunset"][0]).split("T")[-1]

    wmo_code = int(current.get("weather_code", 0))

    metrics = WeatherMetrics(
        city=city_name,
        latitude=lat,
        longitude=lon,
        timezone=tz,
        temperature_c=float(current.get("temperature_2m", 25.0)),
        feels_like_c=float(current.get("apparent_temperature", 25.5)),
        relative_humidity=int(current.get("relative_humidity_2m", 65)),
        wind_speed_kmh=float(current.get("wind_speed_10m", 12.0)),
        wind_direction_deg=int(current.get("wind_direction_10m", 180)),
        weather_condition=get_wmo_condition(wmo_code),
        wmo_code=wmo_code,
        rain_probability=current_rain_prob,
        cloud_cover=int(current.get("cloud_cover", 20)),
        pressure_hpa=float(current.get("pressure_msl", 1013.25)),
        visibility_m=current_visibility,
        uv_index=current_uv,
        sunrise=sunrise_str,
        sunset=sunset_str,
        is_day=bool(current.get("is_day", 1) == 1)
    )

    # Parse 7-day daily forecast
    forecast_list: List[ForecastDay] = []
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    rain_probs = daily.get("precipitation_probability_mean", [])
    weather_codes = daily.get("weather_code", [])
    uv_maxs = daily.get("uv_index_max", [])
    wind_maxs = daily.get("wind_speed_10m_max", [])

    day_names = ["Today", "Tomorrow", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]

    for i in range(min(len(dates), 7)):
        w_code = int(weather_codes[i]) if i < len(weather_codes) else 0
        forecast_list.append(
            ForecastDay(
                date=str(dates[i]),
                day_name=day_names[i] if i < len(day_names) else f"Day {i+1}",
                max_temp_c=float(max_temps[i]) if i < len(max_temps) else 30.0,
                min_temp_c=float(min_temps[i]) if i < len(min_temps) else 20.0,
                rain_probability=int(rain_probs[i]) if i < len(rain_probs) and rain_probs[i] is not None else 10,
                weather_condition=get_wmo_condition(w_code),
                max_uv_index=float(uv_maxs[i]) if i < len(uv_maxs) and uv_maxs[i] is not None else 5.0,
                max_wind_speed_kmh=float(wind_maxs[i]) if i < len(wind_maxs) and wind_maxs[i] is not None else 15.0
            )
        )

    return metrics, forecast_list


def _generate_mock_fallback_weather(city_name: str, lat: float, lon: float) -> Dict[str, Any]:
    """Generates realistic fallback weather metrics when internet/API is disconnected."""
    metrics = WeatherMetrics(
        city=city_name,
        latitude=lat,
        longitude=lon,
        timezone="Asia/Kolkata",
        temperature_c=29.5,
        feels_like_c=31.0,
        relative_humidity=68,
        wind_speed_kmh=14.0,
        wind_direction_deg=210,
        weather_condition="Partly Cloudy",
        wmo_code=2,
        rain_probability=20,
        cloud_cover=35,
        pressure_hpa=1012.0,
        visibility_m=10000.0,
        uv_index=6.5,
        sunrise="06:12",
        sunset="18:38",
        is_day=True
    )
    forecast_7day = [
        ForecastDay(date="2026-07-27", day_name="Today", max_temp_c=31.0, min_temp_c=22.0, rain_probability=20, weather_condition="Partly Cloudy", max_uv_index=7.0, max_wind_speed_kmh=15.0),
        ForecastDay(date="2026-07-28", day_name="Tomorrow", max_temp_c=32.0, min_temp_c=23.0, rain_probability=15, weather_condition="Mainly Clear", max_uv_index=7.5, max_wind_speed_kmh=12.0),
        ForecastDay(date="2026-07-29", day_name="Day 3", max_temp_c=30.0, min_temp_c=21.0, rain_probability=60, weather_condition="Moderate Rain", max_uv_index=4.5, max_wind_speed_kmh=22.0),
        ForecastDay(date="2026-07-30", day_name="Day 4", max_temp_c=28.0, min_temp_c=20.0, rain_probability=75, weather_condition="Heavy Rain", max_uv_index=3.0, max_wind_speed_kmh=30.0),
        ForecastDay(date="2026-07-31", day_name="Day 5", max_temp_c=29.0, min_temp_c=21.0, rain_probability=30, weather_condition="Partly Cloudy", max_uv_index=6.0, max_wind_speed_kmh=14.0),
        ForecastDay(date="2026-08-01", day_name="Day 6", max_temp_c=31.0, min_temp_c=22.0, rain_probability=10, weather_condition="Clear Sky", max_uv_index=8.0, max_wind_speed_kmh=10.0),
        ForecastDay(date="2026-08-02", day_name="Day 7", max_temp_c=32.0, min_temp_c=23.0, rain_probability=10, weather_condition="Clear Sky", max_uv_index=8.5, max_wind_speed_kmh=11.0),
    ]
    return {
        "metrics": metrics.model_dump(),
        "forecast_7day": [f.model_dump() for f in forecast_7day],
        "raw": {}
    }
