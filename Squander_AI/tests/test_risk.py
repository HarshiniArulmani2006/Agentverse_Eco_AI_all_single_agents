"""
Unit tests for Risk Engine
"""
from services.waste_classification_engine import waste_classification_engine
from services.risk_engine import risk_engine

def test_risk_assessment_low():
    cls = waste_classification_engine.classify("Newspaper", 1.0, "residential")
    risk_data = risk_engine.calculate_risk_score(cls)
    assert risk_data["risk_score"] < 50
    assert risk_data["risk_level"] in ("LOW", "MODERATE")

def test_risk_assessment_critical():
    cls = waste_classification_engine.classify("Chemical Solvent Waste", 5.0, "industrial")
    risk_data = risk_engine.calculate_risk_score(cls)
    assert risk_data["risk_score"] > 60
    assert risk_data["risk_level"] in ("HIGH", "CRITICAL")
