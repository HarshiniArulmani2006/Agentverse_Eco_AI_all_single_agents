"""
Unit tests for AI analysis, health, activity, forecast, green, and conversational engines
"""
import pytest
from services.analysis_engine import analysis_engine
from services.health_engine import health_engine
from services.activity_engine import activity_engine
from services.forecast_engine import forecast_engine
from services.green_engine import green_engine
from services.conversational_engine import conversational_engine

def test_risk_score_calculation():
    sample_current = {
        "aqi": 160,
        "pm2_5": 65.0,
        "pm10": 110.0,
        "no2": 35.0,
        "so2": 15.0,
        "co": 500.0,
        "dust": 10.0,
        "aod": 0.4
    }

    risk = analysis_engine.calculate_risk_score(sample_current)
    assert "score" in risk
    assert risk["score"] > 50.0
    assert risk["level"] in ["Poor", "Unhealthy", "Hazardous", "Emergency"]

def test_pollution_pattern_detection():
    sample_current = {
        "pm2_5": 80.0,
        "pm10": 150.0,
        "no2": 45.0,
        "so2": 35.0,
        "co": 800.0,
        "dust": 15.0,
        "aod": 0.6
    }
    patterns = analysis_engine.detect_pollution_patterns(sample_current)
    assert "dominant_pattern" in patterns
    assert "probabilities" in patterns
    assert patterns["probabilities"]["industrial_pollution"] > 0

def test_who_compliance_evaluator():
    sample_current = {
        "pm2_5": 45.0,  # 3x WHO safe limit (15)
        "pm10": 90.0,
        "no2": 30.0,
        "so2": 10.0,
        "o3": 50.0,
        "carbon_monoxide": 2000.0
    }
    comp = analysis_engine.evaluate_who_compliance(sample_current)
    assert comp["pm2_5"]["status"] in ["Above WHO Limit", "Critical", "Dangerous"]

def test_demographic_health_prediction():
    sample_current = {"aqi": 185, "pm2_5": 70.0, "pm10": 120.0, "no2": 40.0, "o3": 80.0}
    health = health_engine.predict_demographic_risks(sample_current)
    assert "children" in health
    assert "asthma_patients" in health
    assert health["asthma_patients"]["risk_level"] in ["Severe / Very High", "Very High", "High"]

def test_outdoor_activity_analyzer():
    sample_current = {"aqi": 40, "pm2_5": 10.0, "pm10": 20.0, "uv_index": 3.0, "dust": 2.0}
    activities = activity_engine.analyze_activities(sample_current)
    assert len(activities) == 12
    running = next(a for a in activities if a["activity"] == "Running")
    assert running["suitability_score"] > 70

def test_conversational_engine():
    sample_current = {"aqi": 150, "pm2_5": 55.0, "pm10": 90.0, "no2": 35.0}
    sample_health = health_engine.predict_demographic_risks(sample_current)
    sample_activities = activity_engine.analyze_activities(sample_current)

    ans = conversational_engine.answer_query(
        "Should I wear a mask today?",
        {"current": sample_current, "location": "TestCity"},
        sample_health,
        sample_activities
    )
    assert "Yes" in ans["answer"] or "N95" in ans["answer"]
