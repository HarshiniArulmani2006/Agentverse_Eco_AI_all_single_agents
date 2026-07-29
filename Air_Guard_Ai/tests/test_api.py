"""
Integration tests for FastAPI REST API Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"
    assert json_data["agent"] == "AirGuard AI"

def test_air_quality_endpoint_city():
    response = client.get("/api/air-quality?city=London")
    assert response.status_code == 200
    data = response.json()
    assert "location" in data
    assert data["location"]["name"] == "London"
    assert "current_air_quality" in data
    assert "risk_assessment" in data
    assert "who_compliance" in data
    assert "multi_agent_payload" in data

def test_multi_city_compare_endpoint():
    response = client.post("/api/compare", json={"cities": ["London", "Tokyo"]})
    assert response.status_code == 200
    data = response.json()
    assert "comparison" in data
    assert len(data["comparison"]) == 2
    assert "cleanest_city" in data

def test_conversational_query_endpoint():
    response = client.post("/api/query", json={"query": "Can I go jogging?", "city": "London"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "intent" in data
