"""
FastAPI REST API Routes for AirGuard AI
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from services.geocoding_service import geocoding_service
from services.air_quality_service import air_quality_service
from services.analysis_engine import analysis_engine
from services.health_engine import health_engine
from services.activity_engine import activity_engine
from services.forecast_engine import forecast_engine
from services.green_engine import green_engine
from services.conversational_engine import conversational_engine
from services.multi_agent_service import multi_agent_service

router = APIRouter()

class MultiCityRequest(BaseModel):
    cities: List[str]

class ConversationalRequest(BaseModel):
    query: str
    city: Optional[str] = "Delhi"
    lat: Optional[float] = None
    lon: Optional[float] = None

async def build_full_report_for_location(city_name: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None) -> Dict[str, Any]:
    location_meta = {}
    
    if city_name:
        coords = await geocoding_service.get_coordinates(city_name)
        if not coords:
            raise HTTPException(status_code=404, detail=f"City '{city_name}' not found.")
        lat = coords["latitude"]
        lon = coords["longitude"]
        location_meta = coords
    elif lat is not None and lon is not None:
        location_meta = {
            "name": f"Location ({lat:.2f}, {lon:.2f})",
            "latitude": lat,
            "longitude": lon,
            "country": "Coordinates",
            "timezone": "UTC"
        }
    else:
        # Default fallback to Delhi if neither provided
        coords = await geocoding_service.get_coordinates("Delhi")
        lat, lon = coords["latitude"], coords["longitude"]
        location_meta = coords

    air_raw = await air_quality_service.fetch_air_quality(lat, lon)
    if not air_raw:
        raise HTTPException(status_code=502, detail="Failed to fetch air quality data from Open-Meteo API.")

    current = air_raw["current"]
    hourly = air_raw["hourly"]

    # Compute engine results
    risk_data = analysis_engine.calculate_risk_score(current)
    patterns = analysis_engine.detect_pollution_patterns(current)
    sources = analysis_engine.estimate_pollution_sources(current)
    who_compliance = analysis_engine.evaluate_who_compliance(current)
    env_intelligence = analysis_engine.generate_environmental_intelligence(current)
    emergency_alerts = analysis_engine.detect_emergency_alerts(current)

    demographic_health = health_engine.predict_demographic_risks(current)
    recommendations = health_engine.generate_personalized_recommendations(current, risk_data["score"])

    activities = activity_engine.analyze_activities(current)

    trends = forecast_engine.predict_trends(hourly, current["aqi"])
    anomalies = forecast_engine.detect_anomalies(hourly)
    analytics = forecast_engine.generate_analytics(hourly)

    ai_scores = green_engine.calculate_ai_scores(current, risk_data["score"])
    green_suggestions = green_engine.generate_green_suggestions(current)
    checklist = green_engine.generate_citizen_checklist()
    eco_challenges = green_engine.generate_eco_challenges()
    carbon_info = green_engine.estimate_carbon_footprint(current["aqi"], location_meta.get("name", "Target Location"))

    multi_agent_json = multi_agent_service.build_standardized_payload(
        location_meta.get("name", "Unknown"),
        air_raw,
        risk_data,
        ai_scores,
        emergency_alerts,
        patterns
    )

    return {
        "location": location_meta,
        "current_air_quality": current,
        "risk_assessment": risk_data,
        "pollution_patterns": patterns,
        "pollution_sources": sources,
        "who_compliance": who_compliance,
        "environmental_intelligence": env_intelligence,
        "emergency_alerts": emergency_alerts,
        "health_advisory": {
            "demographics": demographic_health,
            "recommendations": recommendations
        },
        "activity_analyzer": activities,
        "forecasting": {
            "trends": trends,
            "anomalies": anomalies,
            "analytics": analytics
        },
        "green_sustainability": {
            "scores": ai_scores,
            "suggestions": green_suggestions,
            "citizen_checklist": checklist,
            "eco_challenges": eco_challenges,
            "carbon_footprint": carbon_info
        },
        "multi_agent_payload": multi_agent_json
    }

@router.get("/air-quality")
async def get_air_quality(
    city: Optional[str] = Query(None, description="City Name (e.g., Delhi, London, New York)"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    return await build_full_report_for_location(city, lat, lon)

@router.post("/compare")
async def compare_cities(req: MultiCityRequest):
    if not req.cities or len(req.cities) < 2:
        raise HTTPException(status_code=400, detail="Please provide at least 2 cities for comparison.")

    results = []
    for city_name in req.cities:
        try:
            report = await build_full_report_for_location(city_name=city_name)
            results.append({
                "city": report["location"]["name"],
                "country": report["location"]["country"],
                "aqi": report["current_air_quality"]["aqi"],
                "pm2_5": report["current_air_quality"]["pm2_5"],
                "pm10": report["current_air_quality"]["pm10"],
                "risk_score": report["risk_assessment"]["score"],
                "risk_level": report["risk_assessment"]["level"],
                "dominant_pattern": report["pollution_patterns"]["dominant_pattern"],
                "health_score": report["green_sustainability"]["scores"]["health_safety_score"],
                "sustainability_score": report["green_sustainability"]["scores"]["sustainability_score"]
            })
        except Exception as e:
            results.append({"city": city_name, "error": str(e)})

    # Sort rankings
    valid_results = [r for r in results if "aqi" in r]
    valid_results.sort(key=lambda x: x["aqi"])

    cleanest_city = valid_results[0]["city"] if valid_results else "N/A"
    most_polluted_city = valid_results[-1]["city"] if valid_results else "N/A"

    return {
        "comparison": valid_results,
        "cleanest_city": cleanest_city,
        "most_polluted_city": most_polluted_city,
        "summary": f"Out of {len(valid_results)} cities evaluated, {cleanest_city} registered the cleanest air quality, while {most_polluted_city} exhibits the highest pollution load."
    }

@router.post("/query")
async def process_conversational_query(req: ConversationalRequest):
    report = await build_full_report_for_location(city_name=req.city, lat=req.lat, lon=req.lon)
    answer = conversational_engine.answer_query(
        req.query,
        {
            "current": report["current_air_quality"],
            "location": report["location"]["name"]
        },
        report["health_advisory"]["demographics"],
        report["activity_analyzer"]
    )
    return answer

@router.get("/multi-agent-payload")
async def get_multi_agent_payload(city: str = "Delhi"):
    report = await build_full_report_for_location(city_name=city)
    return report["multi_agent_payload"]

@router.get("/health")
async def health_check():
    return {"status": "online", "agent": "AirGuard AI", "framework": "Fetch.ai uAgents + FastAPI"}
