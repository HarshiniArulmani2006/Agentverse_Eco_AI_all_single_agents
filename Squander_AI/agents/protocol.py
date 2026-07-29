"""
agents/protocol.py – uAgents Protocol Definitions & Message Models
Defines all message types used between the EcoWaste AI Agent and partner agents.
"""
from typing import List, Dict, Any, Optional
from uagents import Model


# ──────────────────────────────────────────────────────────────
# Inbound Message Models (messages EcoWaste AI receives)
# ──────────────────────────────────────────────────────────────

class WasteQueryMessage(Model):
    """Sent by a coordinator or user agent to request waste analysis."""
    waste_type:   str
    quantity_kg:  float
    location:     str
    source:       str       # residential | commercial | industrial


class WeatherContextMessage(Model):
    """Sent by Weather Agent to provide environmental conditions."""
    temperature_c:   float
    humidity_pct:    float
    rainfall_mm:     float
    wind_speed_kmh:  float
    location:        str
    forecast_hours:  int = 24


class AirQualityContextMessage(Model):
    """Sent by Air Quality Agent with current AQI data."""
    aqi_value:       int
    aqi_category:    str   # Good | Moderate | Unhealthy | etc.
    pm25_ugm3:       float
    co_ppm:          float
    location:        str


# ──────────────────────────────────────────────────────────────
# Outbound Message Models (messages EcoWaste AI sends)
# ──────────────────────────────────────────────────────────────

class WasteResponseMessage(Model):
    """Standardized response from EcoWaste AI to any requesting agent."""
    sender_agent:         str
    target_agents:        List[str]
    timestamp:            float
    waste_type:           str
    category:             str
    risk_level:           str
    risk_score:           float
    sustainability_score: float
    recycling_status:     bool
    carbon_estimate:      float
    environmental_score:  float
    emergency_alerts:     List[Dict[str, Any]]
    actionable_triggers:  Dict[str, Any]
    recommendations:      List[str]


class CarbonNotificationMessage(Model):
    """Sent to Carbon Footprint Agent with emissions estimate."""
    sender_agent:      str
    waste_type:        str
    quantity_kg:       float
    best_method:       str
    emissions_kg_co2e: float
    savings_vs_burn:   float
    timestamp:         float


class WaterAlertMessage(Model):
    """Sent to Water Conservation Agent if water contamination risk detected."""
    sender_agent:     str
    waste_type:       str
    risk_level:       str
    contamination_risk: bool
    affected_body:    str    # groundwater | river | lake | ocean
    recommendation:   str
    timestamp:        float


class AirAlertMessage(Model):
    """Sent to Air Quality Agent if burning/dumping hazard detected."""
    sender_agent:    str
    waste_type:      str
    burning_detected: bool
    pm25_risk:       str
    toxic_gas_risk:  str
    recommendation:  str
    timestamp:       float


class EducationRequestMessage(Model):
    """Sent to Environmental Education Agent to generate awareness content."""
    sender_agent:     str
    waste_type:       str
    category:         str
    recycling_rate:   float
    key_facts:        List[str]
    target_audience:  str    # residential | school | commercial
    timestamp:        float


class CoordinatorNotificationMessage(Model):
    """Sent to Coordinator Agent for critical events."""
    sender_agent:    str
    event_type:      str    # EMERGENCY | OVERFLOW | ILLEGAL_DUMP | CRITICAL_RISK
    severity:        str    # LOW | MODERATE | HIGH | CRITICAL
    waste_type:      str
    location:        str
    description:     str
    recommended_action: str
    timestamp:       float
