"""
WeatherWise AI - Comprehensive Test Suite
Tests geocoding, Open-Meteo fetching, risk scoring, recommendations,
conversational decision engine, and multi-agent protocol payload export.
"""

import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.geocoding import geocode_city
from services.open_meteo import fetch_weather_data, WeatherMetrics
from engine.risk_analyzer import calculate_risk_analysis
from engine.recommendation_engine import generate_recommendations
from engine.environmental_engine import generate_environmental_impact
from engine.decision_engine import process_conversational_query, build_full_weather_response
from agents.weather_agent import execute_weather_analysis


def test_geocoding():
    """Test geocoding service converts city names to valid coordinates."""
    res = geocode_city("Coimbatore")
    assert res["name"] == "Coimbatore"
    assert 10.5 <= res["latitude"] <= 11.5
    assert 76.0 <= res["longitude"] <= 77.5
    print("[PASSED] Geocoding test passed!")


def test_weather_retrieval():
    """Test Open-Meteo API weather retrieval and metrics parsing."""
    data = fetch_weather_data(11.0168, 76.9558, "Coimbatore")
    assert "metrics" in data
    assert "forecast_7day" in data
    metrics = WeatherMetrics(**data["metrics"])
    assert metrics.temperature_c is not None
    assert metrics.relative_humidity >= 0
    assert len(data["forecast_7day"]) >= 1
    print("[PASSED] Weather retrieval test passed!")


def test_risk_scoring():
    """Test Risk Engine calculates risk scores and detects severe conditions."""
    mock_metrics = WeatherMetrics(
        city="TestCity",
        latitude=11.0,
        longitude=76.9,
        timezone="Asia/Kolkata",
        temperature_c=40.0,
        feels_like_c=43.0,
        relative_humidity=70,
        wind_speed_kmh=45.0,
        wind_direction_deg=180,
        weather_condition="Thunderstorm",
        wmo_code=95,
        rain_probability=90,
        cloud_cover=90,
        pressure_hpa=1008.0,
        visibility_m=2000.0,
        uv_index=9.0,
        sunrise="06:00",
        sunset="18:30",
        is_day=True
    )
    risk = calculate_risk_analysis(mock_metrics)
    assert risk.risk_score >= 50
    assert risk.risk_level in ["HIGH", "CRITICAL"]
    assert any("Thunderstorm" in cond for cond in risk.detected_conditions)
    assert len(risk.emergency_alerts) >= 1
    print("[PASSED] Risk scoring test passed!")


def test_recommendation_and_activities():
    """Test recommendations and evaluation of 9 outdoor activities."""
    mock_metrics = WeatherMetrics(
        city="TestCity",
        latitude=11.0,
        longitude=76.9,
        timezone="Asia/Kolkata",
        temperature_c=24.0,
        feels_like_c=24.0,
        relative_humidity=50,
        wind_speed_kmh=10.0,
        wind_direction_deg=180,
        weather_condition="Clear Sky",
        wmo_code=0,
        rain_probability=5,
        cloud_cover=10,
        pressure_hpa=1013.0,
        visibility_m=10000.0,
        uv_index=4.0,
        sunrise="06:00",
        sunset="18:30",
        is_day=True
    )
    risk = calculate_risk_analysis(mock_metrics)
    recs = generate_recommendations(mock_metrics, risk)
    
    assert len(recs.clothing) > 0
    assert recs.travel_advice == "Safe for travel"
    assert len(recs.outdoor_activities) == 9
    
    # Check picnic suitability
    picnic = next((a for a in recs.outdoor_activities if a.activity_name == "Picnics"), None)
    assert picnic is not None
    assert picnic.suitable is True
    print("[PASSED] Recommendation & 9 activity evaluation test passed!")


def test_smart_decision_engine():
    """Test Conversational AI processing natural language queries."""
    full_resp = execute_weather_analysis(city="Coimbatore", question="Will it rain today?")
    assert full_resp.success is True
    assert full_resp.decision_answer is not None
    assert "rain" in full_resp.decision_answer.lower() or "coimbatore" in full_resp.decision_answer.lower()
    print("[PASSED] Smart decision engine conversational test passed!")


def test_multi_agent_payload_export():
    """Test structured Multi-Agent JSON payload compliance for future agents."""
    full_resp = execute_weather_analysis(city="Coimbatore")
    payload = full_resp.multi_agent_payload
    assert "header" in payload
    assert payload["header"]["sender_agent"] == "WeatherWise_AI_Agent"
    assert "AirQualityAgent" in payload["header"]["target_agents"]
    assert "actionable_triggers" in payload
    print("[PASSED] Multi-agent protocol payload export test passed!")


if __name__ == "__main__":
    print("Running WeatherWise AI Test Suite...")
    test_geocoding()
    test_weather_retrieval()
    test_risk_scoring()
    test_recommendation_and_activities()
    test_smart_decision_engine()
    test_multi_agent_payload_export()
    print("\nALL TESTS PASSED SUCCESSFULLY!")
