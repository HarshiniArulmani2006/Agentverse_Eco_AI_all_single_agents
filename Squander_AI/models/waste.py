"""
models/waste.py – Waste Data Models (Pydantic)
Typed data models for all waste analysis results.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class WasteItem(BaseModel):
    """Input model for a waste analysis request."""
    waste_type:  str   = Field(..., min_length=2, max_length=200, description="Name of the waste item")
    quantity_kg: float = Field(default=1.0, gt=0, le=100_000, description="Quantity in kilograms")
    location:    str   = Field(default="City", max_length=200)
    source:      str   = Field(default="residential", pattern="^(residential|commercial|industrial)$")


class RecyclabilityResult(BaseModel):
    """Recycling assessment for a waste type."""
    is_recyclable:        bool
    is_reusable:          bool
    is_compostable:       bool
    energy_recovery:      bool
    recycling_efficiency: int = Field(ge=0, le=100)
    recycling_steps:      List[str] = []
    upcycling_ideas:      List[str] = []


class ClassificationResult(BaseModel):
    """Full classification result for a single waste item."""
    input_waste_type:            str
    category_key:                str
    category_label:              str
    category_icon:               str
    category_color:              str
    bin_type:                    str
    confidence:                  int = Field(ge=0, le=100)
    disposal_recommendation:     str
    xai_reason:                  str
    recyclability:               Dict[str, Any]
    can_become:                  List[str]
    quantity_kg:                 float
    source:                      str
    is_toxic:                    bool
    is_flammable:                bool
    requires_special_handling:   bool


class CarbonComparison(BaseModel):
    """Single entry in carbon footprint comparison table."""
    method:       str
    method_key:   str
    emissions_kg: float
    label:        str
    is_best:      bool


class CarbonAnalysis(BaseModel):
    """Full carbon footprint analysis."""
    waste_type:                str
    quantity_kg:               float
    best_method:               str
    best_method_key:           str
    best_method_emissions:     float
    savings_vs_incineration:   float
    xai_reason:                str
    comparison:                List[Dict[str, Any]]
    confidence:                int = Field(ge=0, le=100)


class RiskFactor(BaseModel):
    """Single risk factor in the risk assessment."""
    factor:      str
    score:       float
    level:       str
    description: str


class RiskAssessment(BaseModel):
    """Full risk assessment result."""
    risk_score:   float = Field(ge=0, le=100)
    risk_level:   str
    risk_color:   str
    xai_reason:   str
    risk_factors: Dict[str, Any]
    confidence:   int = Field(ge=0, le=100)


class SustainabilityScores(BaseModel):
    """AI sustainability scoring result."""
    waste_score:            float
    recycling_score:        float
    environmental_score:    float
    sustainability_score:   float
    circular_economy_score: float
    carbon_reduction_score: float
    score_confidence:       int
    xai_reason:             str


class FullAnalysisResult(BaseModel):
    """Complete output from the full analysis pipeline."""
    classification:               Dict[str, Any]
    recycling:                    Dict[str, Any]
    environmental_impact:         Dict[str, Any]
    carbon_footprint:             Dict[str, Any]
    risk_assessment:              Dict[str, Any]
    emergency_alerts:             List[Dict[str, Any]]
    pollution_sources:            List[Dict[str, Any]]
    sustainability_scores:        Dict[str, Any]
    sustainability_recommendations: List[str]
    circular_economy_insight:     str
    forecast:                     Dict[str, Any]
    multi_agent_payload:          Dict[str, Any]
