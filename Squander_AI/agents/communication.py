"""
agents/communication.py – Inter-Agent Communication Utilities
Provides helper functions for EcoWaste AI to notify partner agents
using the standardized Fetch.ai uAgents message protocol.

All notifications are fire-and-forget (non-blocking) and include
rich context payloads so partner agents can act autonomously.
"""
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("ecowaste.communication")


# ──────────────────────────────────────────────────────────────
# Known Partner Agent Addresses (set via environment / config)
# These will be populated when agents are deployed to AgentVerse
# ──────────────────────────────────────────────────────────────
PARTNER_AGENTS = {
    "WeatherAgent":              None,  # Set agent address when available
    "AirQualityAgent":           None,
    "CarbonFootprintAgent":      None,
    "WaterConservationAgent":    None,
    "EnvironmentalEducationAgent": None,
    "CoordinatorAgent":          None,
}


async def notify_carbon_agent(
    ctx,
    waste_type: str,
    quantity_kg: float,
    carbon_data: Dict[str, Any],
) -> bool:
    """
    Notify the Carbon Footprint Agent about waste-related CO₂ emissions.

    Args:
        ctx:          uAgent context (provides send capability)
        waste_type:   Type of waste analyzed
        quantity_kg:  Quantity in kilograms
        carbon_data:  Output from environmental_engine.estimate_carbon_footprint()

    Returns:
        True if message sent, False if agent address not configured.
    """
    from agents.protocol import CarbonNotificationMessage

    agent_addr = PARTNER_AGENTS.get("CarbonFootprintAgent")
    if not agent_addr:
        logger.debug("[Communication] Carbon Footprint Agent address not configured — skipping notification.")
        return False

    msg = CarbonNotificationMessage(
        sender_agent      = "EcoWaste_AI_Agent",
        waste_type        = waste_type,
        quantity_kg       = quantity_kg,
        best_method       = carbon_data.get("best_method", "Unknown"),
        emissions_kg_co2e = float(carbon_data.get("best_method_emissions", 0.0)),
        savings_vs_burn   = float(carbon_data.get("savings_vs_incineration", 0.0)),
        timestamp         = time.time(),
    )
    await ctx.send(agent_addr, msg)
    logger.info(f"[Communication] Carbon notification sent: {waste_type} → {carbon_data.get('best_method')} ({quantity_kg} kg)")
    return True


async def notify_water_agent(
    ctx,
    waste_type: str,
    risk_level: str,
    environmental_data: Dict[str, Any],
) -> bool:
    """
    Notify the Water Conservation Agent if water contamination risk is detected.
    Triggered when water impact score >= 70 or hazardous/biomedical waste is detected.
    """
    from agents.protocol import WaterAlertMessage

    agent_addr = PARTNER_AGENTS.get("WaterConservationAgent")
    if not agent_addr:
        logger.debug("[Communication] Water Conservation Agent not configured.")
        return False

    water_score = (environmental_data.get("dimensions", {})
                   .get("water", {}).get("score", 0))
    contamination_risk = water_score >= 70 or risk_level in ("HIGH", "CRITICAL")

    msg = WaterAlertMessage(
        sender_agent        = "EcoWaste_AI_Agent",
        waste_type          = waste_type,
        risk_level          = risk_level,
        contamination_risk  = contamination_risk,
        affected_body       = "groundwater" if contamination_risk else "none",
        recommendation      = "Immediately divert waste from water proximity areas." if contamination_risk else "No immediate threat.",
        timestamp           = time.time(),
    )
    await ctx.send(agent_addr, msg)
    logger.info(f"[Communication] Water alert sent: {waste_type} | Risk: {risk_level} | Contamination: {contamination_risk}")
    return True


async def notify_air_quality_agent(
    ctx,
    waste_type: str,
    category_key: str,
    is_burning: bool = False,
) -> bool:
    """
    Notify the Air Quality Agent if open burning or hazardous air pollutants are detected.
    """
    from agents.protocol import AirAlertMessage

    agent_addr = PARTNER_AGENTS.get("AirQualityAgent")
    if not agent_addr:
        return False

    high_air_risk_categories = {"hazardous", "ewaste", "industrial", "biomedical"}
    pm25_risk = "HIGH" if (is_burning or category_key in high_air_risk_categories) else "LOW"

    msg = AirAlertMessage(
        sender_agent     = "EcoWaste_AI_Agent",
        waste_type       = waste_type,
        burning_detected = is_burning,
        pm25_risk        = pm25_risk,
        toxic_gas_risk   = "HIGH" if category_key in ("hazardous", "ewaste") else "LOW",
        recommendation   = "Increase AQI monitoring near waste collection points." if pm25_risk == "HIGH" else "Normal monitoring.",
        timestamp        = time.time(),
    )
    await ctx.send(agent_addr, msg)
    logger.info(f"[Communication] Air quality alert sent: {waste_type} | PM2.5 risk: {pm25_risk}")
    return True


async def notify_education_agent(
    ctx,
    waste_type: str,
    category_label: str,
    recycling_efficiency: float,
    sustainability_score: float,
) -> bool:
    """
    Notify the Environmental Education Agent to generate awareness content.
    Triggered when sustainability score is low (< 50).
    """
    from agents.protocol import EducationRequestMessage

    agent_addr = PARTNER_AGENTS.get("EnvironmentalEducationAgent")
    if not agent_addr:
        return False

    key_facts = [
        f"{category_label} has a recycling efficiency of {recycling_efficiency}%.",
        f"The sustainability score for this waste type is {sustainability_score:.0f}/100.",
        "Proper disposal reduces landfill burden and carbon emissions.",
    ]

    msg = EducationRequestMessage(
        sender_agent    = "EcoWaste_AI_Agent",
        waste_type      = waste_type,
        category        = category_label,
        recycling_rate  = recycling_efficiency,
        key_facts       = key_facts,
        target_audience = "residential",
        timestamp       = time.time(),
    )
    await ctx.send(agent_addr, msg)
    logger.info(f"[Communication] Education request sent for: {waste_type}")
    return True


async def notify_coordinator_agent(
    ctx,
    event_type: str,
    severity: str,
    waste_type: str,
    location: str,
    description: str,
    recommended_action: str,
) -> bool:
    """
    Notify the Coordinator Agent about critical environmental events.
    Used for emergency alerts, overflow events, and critical risk detections.
    """
    from agents.protocol import CoordinatorNotificationMessage

    agent_addr = PARTNER_AGENTS.get("CoordinatorAgent")
    if not agent_addr:
        return False

    msg = CoordinatorNotificationMessage(
        sender_agent        = "EcoWaste_AI_Agent",
        event_type          = event_type,
        severity            = severity,
        waste_type          = waste_type,
        location            = location,
        description         = description,
        recommended_action  = recommended_action,
        timestamp           = time.time(),
    )
    await ctx.send(agent_addr, msg)
    logger.info(f"[Communication] Coordinator notified: {event_type} | Severity: {severity}")
    return True


def build_multi_agent_context(
    classification: Dict[str, Any],
    carbon: Dict[str, Any],
    environmental: Dict[str, Any],
    risk: Dict[str, Any],
    recycling: Dict[str, Any],
    scores: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build the multi-agent context block that is attached to every API response.
    Provides partner agents with pre-computed data they need for autonomous decisions.
    """
    cat       = classification.get("category_key", "mixed")
    risk_sc   = risk.get("risk_score", 0)
    sust_sc   = scores.get("sustainability_score", 0)
    water_sc  = environmental.get("dimensions", {}).get("water", {}).get("score", 0)

    return {
        "weather_agent_context": {
            "note": "High temperature accelerates organic waste decomposition and increases odour risk.",
            "request": "Provide temperature, humidity, and rainfall forecast to optimise collection schedule.",
            "relevant_fields": ["temperature_c", "humidity_pct", "rainfall_mm"],
        },
        "air_quality_agent_context": {
            "note": f"{'HIGH' if cat in ('hazardous','ewaste','industrial') else 'LOW'} air pollution risk from this waste type.",
            "burning_risk": cat in ("hazardous", "ewaste"),
            "request": "Monitor PM2.5 and CO levels near collection and disposal points.",
            "relevant_fields": ["aqi_value", "pm25_ugm3", "co_ppm"],
        },
        "carbon_footprint_agent_context": {
            "note": f"Best disposal ({carbon.get('best_method','N/A')}) saves {carbon.get('savings_vs_incineration',0)} kg CO₂e.",
            "emissions_kg": carbon.get("best_method_emissions", 0),
            "savings_kg":   carbon.get("savings_vs_incineration", 0),
            "request": "Update community carbon ledger with this waste disposal event.",
        },
        "water_conservation_agent_context": {
            "note": "Leachate and river disposal risks detected based on waste category.",
            "water_risk_score": water_sc,
            "contamination_risk": water_sc >= 70 or risk_sc > 75,
            "request": "Monitor groundwater quality near identified waste disposal sites.",
        },
        "education_agent_context": {
            "note": f"Category: {classification.get('category_label')}. Recycling efficiency: {recycling.get('recycling_efficiency',0)}%.",
            "sustainability_score": sust_sc,
            "education_needed": sust_sc < 50,
            "request": "Generate community recycling awareness content for this waste category.",
        },
        "coordinator_agent_context": {
            "note": "EcoWaste AI notifying coordinator of current waste event.",
            "risk_level":  risk.get("risk_level", "LOW"),
            "urgent":      risk_sc > 75,
            "request": "Update environmental dashboard and alert relevant field teams if critical.",
        },
    }
