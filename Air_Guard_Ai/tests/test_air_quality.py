"""
Unit tests for Air Quality Data Retrieval Service
"""
import pytest
from services.air_quality_service import air_quality_service

@pytest.mark.asyncio
async def test_fetch_air_quality():
    # Fetch air quality for London coords
    data = await air_quality_service.fetch_air_quality(51.5074, -0.1278)
    assert data is not None
    assert "current" in data
    assert "aqi" in data["current"]
    assert "pm2_5" in data["current"]
    assert "pm10" in data["current"]
    assert "hourly" in data
