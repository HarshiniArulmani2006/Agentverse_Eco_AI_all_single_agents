"""
WeatherWise AI - Data Schema Definitions
Provides Pydantic models for uAgents protocols, Open-Meteo parsing,
risk analysis, recommendations, and multi-agent system communication.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from uagents import Model


# --- uAgents Inter-Agent Request Message ---
class WeatherQueryRequest(Model):
    """uAgents Model for incoming weather query requests."""
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    question: Optional[str] = None
    sender_agent: Optional[str] = None


# --- Weather Metrics Model ---
class WeatherMetrics(BaseModel):
    """Parsed real-time weather metrics from Open-Meteo API."""
    city: str
    latitude: float
    longitude: float
    timezone: str
    temperature_c: float = Field(..., description="Current temperature in °C")
    feels_like_c: float = Field(..., description="Apparent feels-like temperature in °C")
    relative_humidity: int = Field(..., description="Relative humidity percentage (0-100%)")
    wind_speed_kmh: float = Field(..., description="Wind speed in km/h")
    wind_direction_deg: int = Field(..., description="Wind direction in degrees")
    weather_condition: str = Field(..., description="Human readable weather condition description")
    wmo_code: int = Field(..., description="WMO weather code (0-99)")
    rain_probability: int = Field(..., description="Rain probability percentage (0-100%)")
    cloud_cover: int = Field(..., description="Cloud cover percentage (0-100%)")
    pressure_hpa: float = Field(..., description="Atmospheric pressure at sea level in hPa")
    visibility_m: float = Field(..., description="Visibility distance in meters")
    uv_index: float = Field(..., description="UV Index (0-12+)")
    sunrise: str = Field(..., description="Sunrise time string")
    sunset: str = Field(..., description="Sunset time string")
    is_day: bool = Field(True, description="True if currently daytime")


# --- Risk Analysis Model ---
class RiskAnalysis(BaseModel):
    """Weather Risk Engine analysis output."""
    risk_score: int = Field(..., description="Risk score calculated between 0 and 100")
    risk_level: str = Field(..., description="LOW, MEDIUM, HIGH, or CRITICAL")
    primary_reason: str = Field(..., description="Summary explanation of the risk rating")
    reasons: List[str] = Field(default_factory=list, description="Detailed list of detected risk factors")
    detected_conditions: List[str] = Field(default_factory=list, description="List of detected weather anomalies (e.g. Heavy Rain, Heatwave)")
    emergency_alerts: List[Dict[str, str]] = Field(default_factory=list, description="Emergency warning titles and safety guidelines")


# --- Outdoor Activity Evaluation Model ---
class OutdoorActivity(BaseModel):
    """Evaluation of suitability for a specific outdoor activity."""
    activity_name: str
    suitable: bool
    status: str = Field(..., description="EXCELLENT, GOOD, CAUTION, or UNSUITABLE")
    suitability_score: int = Field(..., description="Suitability rating between 0 and 100")
    reason: str = Field(..., description="Reasoning for activity recommendation")


# --- Recommendations Model ---
class PersonalizedRecommendations(BaseModel):
    """Personalized advice across clothing, travel, health, and activities."""
    clothing: List[str] = Field(default_factory=list)
    travel_advice: str
    travel_details: List[str] = Field(default_factory=list)
    health_advice: List[str] = Field(default_factory=list)
    outdoor_activities: List[OutdoorActivity] = Field(default_factory=list)


# --- Environmental Intelligence Model ---
class EnvironmentalImpact(BaseModel):
    """Impact of weather on renewable energy, agriculture, and ecosystem."""
    solar_power_potential: str = Field(..., description="EXCELLENT, HIGH, MODERATE, or LOW")
    solar_details: str
    wind_energy_potential: str = Field(..., description="EXCELLENT, GOOD, MODERATE, or POOR")
    wind_details: str
    irrigation_need: str = Field(..., description="HIGH, MODERATE, LOW, or NONE (RAIN EXPECTED)")
    irrigation_details: str
    electricity_demand_impact: str = Field(..., description="NORMAL, ELEVATED (COOLING LOAD), HIGH (HEATING LOAD)")
    wildfire_risk: str = Field(..., description="LOW, MODERATE, HIGH, EXTREME")
    environmental_summary: str


# --- Forecast Day Model ---
class ForecastDay(BaseModel):
    """Single day forecast item."""
    date: str
    day_name: str
    max_temp_c: float
    min_temp_c: float
    rain_probability: int
    weather_condition: str
    max_uv_index: float
    max_wind_speed_kmh: float


# --- uAgents Response Message / Full Weather Response ---
class WeatherResponse(Model):
    """Complete WeatherWise response object suitable for human reading and uAgents messaging."""
    success: bool = True
    timestamp: str = ""
    location: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    metrics: Dict[str, Any] = {}
    risk_analysis: Dict[str, Any] = {}
    recommendations: Dict[str, Any] = {}
    environmental_intelligence: Dict[str, Any] = {}
    daily_summary: str = ""
    decision_answer: Optional[str] = None
    forecast_7day: List[Dict[str, Any]] = []
    multi_agent_payload: Dict[str, Any] = {}
    error: Optional[str] = None


# --- Multi-Agent Interoperability Protocol Schemas ---
class MultiAgentHeader(BaseModel):
    """Standardized header for multi-agent system communication."""
    sender_agent: str = "WeatherWise_AI_Agent"
    target_agents: List[str] = [
        "AirQualityAgent",
        "WasteManagementAgent",
        "CarbonFootprintAgent",
        "WaterConservationAgent",
        "EnvironmentalEducationAgent",
        "CoordinatorAgent"
    ]
    protocol_version: str = "1.0.0"
    message_type: str = "ENVIRONMENTAL_TELEMETRY"
    timestamp: str


class MultiAgentPayload(BaseModel):
    """Structured payload exported for downstream environmental agents."""
    header: MultiAgentHeader
    location: str
    coordinates: Dict[str, float]
    weather_summary: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    environmental_impacts: Dict[str, Any]
    actionable_triggers: List[str] = Field(default_factory=list, description="Triggers for downstream agents (e.g. REDUCE_IRRIGATION, HIGH_SOLAR_OUTPUT)")
