"""
Unit tests for AI Waste Classification Engine
"""
from services.waste_classification_engine import waste_classification_engine

def test_classify_plastic_bottle():
    res = waste_classification_engine.classify("Plastic Bottle", 2.0, "residential")
    assert res["category_key"] == "plastic"
    assert res["confidence"] >= 80
    assert "recycling" in res["disposal_recommendation"].lower() or "recycle" in res["disposal_recommendation"].lower()

def test_classify_food_waste():
    res = waste_classification_engine.classify("Banana Peel leftovers", 1.0, "residential")
    assert res["category_key"] == "organic"
    assert res["recyclability"]["compostable"] is True

def test_classify_battery():
    res = waste_classification_engine.classify("Lithium Battery", 0.5, "commercial")
    assert res["category_key"] in ("ewaste", "hazardous")
    assert res["requires_special_handling"] is True
