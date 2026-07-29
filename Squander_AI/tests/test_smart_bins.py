"""
Unit tests for Smart Bin Collection Engine
"""
from services.collection_engine import collection_engine

def test_smart_bins_summary():
    summary = collection_engine.get_collection_summary()
    assert "smart_bins" in summary
    assert "route_optimization" in summary
    assert len(summary["smart_bins"]) > 0
    assert summary["route_optimization"]["total_bins_monitored"] > 0
