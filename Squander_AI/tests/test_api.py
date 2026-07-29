"""
Integration tests for FastAPI REST API endpoints
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert data["agent"] == "EcoWaste AI"

def test_api_analyze():
    payload = {
        "waste_type": "Plastic Bottle",
        "quantity_kg": 2.5,
        "location": "Central Park",
        "source": "residential"
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "classification" in data
    assert data["classification"]["category_key"] == "plastic"
    assert "multi_agent_payload" in data

def test_api_smart_bins():
    res = client.get("/api/smart-bins")
    assert res.status_code == 200
    data = res.json()
    assert "smart_bins" in data
