"""
Unit tests for Sustainability Engine
"""
from services.waste_classification_engine import waste_classification_engine
from services.sustainability_engine import sustainability_engine

def test_ai_sustainability_scores():
    cls = waste_classification_engine.classify("Aluminium Can", 1.0, "residential")
    scores = sustainability_engine.calculate_ai_scores(cls, risk_score=15.0)
    assert 0 <= scores["sustainability_score"] <= 100
    assert 0 <= scores["recycling_score"] <= 100
    assert "xai_reason" in scores
