"""
models/analytics.py – Community Analytics & Forecast Data Models (Pydantic)
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class DailyForecast(BaseModel):
    """Single day in the daily waste forecast series."""
    day:            str
    day_index:      int
    estimated_kg:   float
    label:          str
    confidence_pct: int


class MonthlyForecast(BaseModel):
    """Single month in the monthly waste forecast series."""
    month:          str
    month_index:    int
    estimated_kg:   float
    label:          str
    confidence_pct: int
    growth_factor:  float


class SeasonalPeak(BaseModel):
    """Festival or seasonal waste surge event."""
    season:       str
    months:       str
    increase_pct: float
    reason:       str


class ForecastData(BaseModel):
    """Full waste generation forecast output."""
    source:          str
    location:        str
    baseline_kg_day: float
    daily_7day:      List[Dict[str, Any]]
    monthly_12month: List[Dict[str, Any]]
    seasonal_peaks:  List[Dict[str, Any]]
    confidence:      int


class WasteBreakdown(BaseModel):
    """Percentage breakdown of waste types in a community."""
    organic:      float
    plastic:      float
    paper:        float
    glass:        float
    metal:        float
    ewaste:       float
    hazardous:    float
    construction: float
    other:        float


class CommunityAnalytics(BaseModel):
    """Community-level waste analytics."""
    source:                      str
    recycling_rate_pct:          float
    landfill_rate_pct:           float
    compost_rate_pct:            float
    zero_waste_progress_pct:     float
    annual_waste_kg:             float
    plastic_reduction_target_pct: float
    household_waste_breakdown:   Dict[str, float]
    top_waste_type:              str
    community_sustainability_score: float


class AnomalyAlert(BaseModel):
    """Single anomaly detected in waste patterns."""
    anomaly:        str
    description:    str
    probable_cause: str
    recommendation: str
    severity:       str   # LOW | MODERATE | HIGH | CRITICAL
    confidence:     int = Field(ge=0, le=100)


class EcoBadge(BaseModel):
    """Achievement badge in the gamification system."""
    badge:            str
    points_required:  int
    description:      str


class EcoChallenge(BaseModel):
    """Sustainability challenge for community engagement."""
    challenge:     str
    description:   str
    reward_points: int
    duration_days: int
