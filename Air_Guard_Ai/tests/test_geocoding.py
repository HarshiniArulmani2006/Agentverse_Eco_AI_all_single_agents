"""
Unit tests for Geocoding Service
"""
import pytest
from services.geocoding_service import geocoding_service

@pytest.mark.asyncio
async def test_geocoding_valid_city():
    coords = await geocoding_service.get_coordinates("London")
    assert coords is not None
    assert "latitude" in coords
    assert "longitude" in coords
    assert coords["name"] == "London"

@pytest.mark.asyncio
async def test_geocoding_caching():
    # First call fills cache
    res1 = await geocoding_service.get_coordinates("Delhi")
    # Second call should use cache
    res2 = await geocoding_service.get_coordinates("Delhi")
    assert res1 == res2
