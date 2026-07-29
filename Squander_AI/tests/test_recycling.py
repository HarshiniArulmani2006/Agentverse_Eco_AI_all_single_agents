"""
Unit tests for Recycling Engine
"""
from services.waste_classification_engine import waste_classification_engine
from services.recycling_engine import recycling_engine

def test_recycling_analysis():
    cls = waste_classification_engine.classify("Cardboard Box", 1.5, "residential")
    rec = recycling_engine.analyze(cls)
    assert rec["is_recyclable"] is True
    assert rec["recycling_efficiency"] > 70
    assert len(rec["recycling_steps"]) > 0
