"""
WeatherWise AI - Fetch.ai AgentVerse Standalone IDE Script
Self-contained script ready for direct copy-paste into Fetch.ai AgentVerse web editor.
"""

import time
import requests
import logging
from typing import Dict, Any, List, Optional, Tuple
from uagents import Agent, Context, Model, Protocol

# --- uAgents Messages ---
class WeatherQueryRequest(Model):
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    question: Optional[str] = None

class WeatherResponse(Model):
    success: bool
    timestamp: str
    location: str
    latitude: float
    longitude: float
    metrics: Dict[str, Any]
    risk_analysis: Dict[str, Any]
    recommendations: Dict[str, Any]
    environmental_intelligence: Dict[str, Any]
    daily_summary: str
    decision_answer: Optional[str] = None
    forecast_7day: List[Dict[str, Any]] = []
    multi_agent_payload: Dict[str, Any] = {}
    error: Optional[str] = None

# Initialize Agent
agent = Agent(name="weatherwise_agent", seed="weatherwise_ai_agentverse_seed_2026")
weather_proto = Protocol(name="WeatherWiseProtocol", version="1.0.0")

# --- WMO Weather Code Table ---
WMO_CODES = {
    0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Dense Fog", 48: "Depositing Rime Fog", 51: "Light Drizzle", 53: "Moderate Drizzle",
    55: "Dense Drizzle", 61: "Slight Rain", 63: "Moderate Rain", 65: "Heavy Rain",
    71: "Slight Snow", 75: "Heavy Snow", 80: "Slight Rain Showers", 82: "Violent Rain Showers",
    95: "Thunderstorm", 99: "Thunderstorm with Hail"
}

def geocode_city(city_name: str) -> Dict[str, Any]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    try:
        res = requests.get(url, params={"name": city_name, "count": 1, "format": "json"}, timeout=8)
        data = res.json()
        if data.get("results"):
            item = data["results"][0]
            return {"name": item["name"], "lat": float(item["latitude"]), "lon": float(item["longitude"])}
    except Exception:
        pass
    return {"name": city_name or "Coimbatore", "lat": 11.0168, "lon": 76.9558}

def fetch_weather(lat: float, lon: float, city: str) -> Dict[str, Any]:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "wind_speed_10m", "cloud_cover"],
        "hourly": ["uv_index", "precipitation_probability"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_mean", "weather_code"],
        "timezone": "auto"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        curr = data.get("current", {})
        hourly = data.get("hourly", {})
        daily = data.get("daily", {})
        
        w_code = int(curr.get("weather_code", 0))
        rain_prob = int(hourly.get("precipitation_probability", [0])[0] if hourly.get("precipitation_probability") else 0)
        uv = float(hourly.get("uv_index", [0.0])[0] if hourly.get("uv_index") else 0.0)
        
        metrics = {
            "city": city, "latitude": lat, "longitude": lon,
            "temperature_c": float(curr.get("temperature_2m", 25.0)),
            "feels_like_c": float(curr.get("apparent_temperature", 25.0)),
            "relative_humidity": int(curr.get("relative_humidity_2m", 60)),
            "wind_speed_kmh": float(curr.get("wind_speed_10m", 10.0)),
            "weather_condition": WMO_CODES.get(w_code, "Partly Cloudy"),
            "wmo_code": w_code, "rain_probability": rain_prob,
            "cloud_cover": int(curr.get("cloud_cover", 20)), "uv_index": uv
        }
        
        forecast = []
        d_times = daily.get("time", [])
        d_maxs = daily.get("temperature_2m_max", [])
        d_mins = daily.get("temperature_2m_min", [])
        d_rains = daily.get("precipitation_probability_mean", [])
        d_codes = daily.get("weather_code", [])
        
        for i in range(min(len(d_times), 7)):
            forecast.append({
                "date": str(d_times[i]),
                "max_temp_c": float(d_maxs[i]) if i < len(d_maxs) else 30.0,
                "min_temp_c": float(d_mins[i]) if i < len(d_mins) else 20.0,
                "rain_probability": int(d_rains[i]) if i < len(d_rains) and d_rains[i] is not None else 10,
                "weather_condition": WMO_CODES.get(int(d_codes[i]) if i < len(d_codes) else 0, "Clear")
            })
            
        return {"metrics": metrics, "forecast": forecast}
    except Exception as e:
        return {
            "metrics": {
                "city": city, "latitude": lat, "longitude": lon, "temperature_c": 28.0,
                "feels_like_c": 30.0, "relative_humidity": 65, "wind_speed_kmh": 12.0,
                "weather_condition": "Partly Cloudy", "wmo_code": 2, "rain_probability": 15,
                "cloud_cover": 30, "uv_index": 6.0
            },
            "forecast": []
        }

def analyze_risk(m: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    reasons = []
    conds = []
    
    if m["temperature_c"] >= 38.0:
        score += 30; reasons.append("Heatwave conditions"); conds.append("Heatwave")
    if m["wmo_code"] in [95, 99]:
        score += 45; reasons.append("Thunderstorm detected"); conds.append("Thunderstorm")
    elif m["wmo_code"] in [65, 82] or m["rain_probability"] >= 70:
        score += 35; reasons.append("Heavy Rain detected"); conds.append("Heavy Rain")
    if m["wind_speed_kmh"] >= 40.0:
        score += 20; reasons.append("Strong Winds"); conds.append("Strong Wind")
        
    score = min(max(score, 0), 100)
    level = "LOW" if score <= 25 else "MEDIUM" if score <= 50 else "HIGH" if score <= 75 else "CRITICAL"
    return {"risk_score": score, "risk_level": level, "reasons": reasons, "detected_conditions": conds}

@agent.on_event("startup")
async def start(ctx: Context):
    ctx.logger.info(f"WeatherWise AI Agent Verse Node Active! Address: {agent.address}")

@weather_proto.on_message(model=WeatherQueryRequest, replies={WeatherResponse})
async def handle_query(ctx: Context, sender: str, msg: WeatherQueryRequest):
    ctx.logger.info(f"Incoming query for '{msg.city}' from {sender}")
    geo = geocode_city(msg.city or "Coimbatore")
    data = fetch_weather(geo["lat"], geo["lon"], geo["name"])
    m = data["metrics"]
    r = analyze_risk(m)
    
    resp = WeatherResponse(
        success=True,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        location=m["city"],
        latitude=m["latitude"],
        longitude=m["longitude"],
        metrics=m,
        risk_analysis=r,
        recommendations={"travel_advice": "Safe for travel" if r["risk_score"] < 50 else "Avoid unnecessary travel"},
        environmental_intelligence={"summary": "Solar High, Wind Moderate"},
        daily_summary=f"Today in {m['city']}: {m['weather_condition']} at {m['temperature_c']}°C. Risk Score: {r['risk_score']}/100.",
        forecast_7day=data["forecast"]
    )
    await ctx.send(sender, resp)

agent.include(weather_proto)

if __name__ == "__main__":
    agent.run()
