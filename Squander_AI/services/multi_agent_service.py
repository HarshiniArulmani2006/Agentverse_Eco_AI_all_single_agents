"""
Fetch.ai AgentVerse (uAgents) Framework Integration & Multi-Agent Payload Generator
- Initializes EcoWaste AI as a Fetch.ai uAgent
- Defines message protocol for inter-agent communication
- Builds standardized JSON payload for all partner agents
"""
import time
from typing import Dict, Any, List
from uagents import Agent, Context, Protocol, Model
from pydantic import BaseModel
from config import AGENT_NAME, AGENT_SEED, AGENT_PORT, AGENT_ENDPOINT


# ──────────────────────────────────────────────────────────────
# uAgent Message Protocol Models
# ──────────────────────────────────────────────────────────────
class WasteQueryMessage(Model):
    waste_type: str
    quantity_kg: float
    location: str
    source: str


class WasteResponseMessage(Model):
    sender_agent: str
    target_agents: List[str]
    timestamp: float
    waste_type: str
    category: str
    risk_level: str
    risk_score: float
    sustainability_score: float
    recycling_status: bool
    carbon_estimate: float
    environmental_score: float
    emergency_alerts: List[Dict[str, Any]]
    actionable_triggers: Dict[str, Any]
    recommendations: List[str]


# ──────────────────────────────────────────────────────────────
# Initialize uAgent
# ──────────────────────────────────────────────────────────────
waste_agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
    endpoint=AGENT_ENDPOINT
)

waste_protocol = Protocol(name="EcoWasteProtocol", version="1.0.0")


@waste_protocol.on_message(model=WasteQueryMessage)
async def handle_waste_query(ctx: Context, sender: str, msg: WasteQueryMessage):
    ctx.logger.info(
        f"Received Waste query from {sender}: {msg.waste_type} ({msg.quantity_kg} kg) at {msg.location}"
    )
    response = WasteResponseMessage(
        sender_agent="EcoWaste_AI_Agent",
        target_agents=[
            "WeatherAgent", "AirQualityAgent", "CarbonFootprintAgent",
            "WaterConservationAgent", "EnvironmentalEducationAgent", "CoordinatorAgent"
        ],
        timestamp=time.time(),
        waste_type=msg.waste_type,
        category="plastic",
        risk_level="MODERATE",
        risk_score=55.0,
        sustainability_score=68.0,
        recycling_status=True,
        carbon_estimate=1.53,
        environmental_score=42.0,
        emergency_alerts=[],
        actionable_triggers={
            "recycling_center_dispatch_required": True,
            "collection_route_optimize_required": False,
        },
        recommendations=[
            "Send to nearest plastic recycling MRF.",
            "Reduce single-use plastic consumption.",
        ]
    )
    await ctx.send(sender, response)


waste_agent.include(waste_protocol)


# ──────────────────────────────────────────────────────────────
# Multi-Agent Payload Builder
# ──────────────────────────────────────────────────────────────
class MultiAgentService:

    def build_standardized_payload(
        self,
        classification: Dict[str, Any],
        recycling: Dict[str, Any],
        risk: Dict[str, Any],
        environmental: Dict[str, Any],
        carbon: Dict[str, Any],
        scores: Dict[str, Any],
        emergency_alerts: List[Dict[str, Any]],
        forecast: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Build a standardized multi-agent JSON payload compatible with all partner agents.
        """
        qty     = classification.get("quantity_kg", 1.0)
        cat     = classification.get("category_key", "mixed")
        label   = classification.get("category_label", "Mixed")
        risk_sc = risk.get("risk_score", 50)
        sust_sc = scores.get("sustainability_score", 50)

        actionable_triggers = {
            "recycling_center_dispatch_required":
                recycling.get("is_recyclable", False),
            "hazardous_waste_team_required":
                classification.get("is_toxic", False),
            "emergency_response_required":
                len(emergency_alerts) > 0 and any(a["severity"] == "CRITICAL" for a in emergency_alerts),
            "air_quality_alert_needed":
                cat in ("hazardous", "ewaste", "industrial") or risk_sc > 70,
            "water_contamination_warning":
                environmental.get("dimensions", {}).get("water", {}).get("score", 0) >= 70,
            "carbon_offset_recommended":
                carbon.get("best_method_key") == "recycle",
            "community_education_required":
                sust_sc < 50,
            "collection_route_update_needed":
                risk_sc > 60,
        }

        return {
            "sender_agent":        "EcoWaste_AI_Agent",
            "agent_address":       waste_agent.address,
            "target_agents": [
                "WeatherAgent",
                "AirQualityAgent",
                "CarbonFootprintAgent",
                "WaterConservationAgent",
                "EnvironmentalEducationAgent",
                "CoordinatorAgent",
            ],
            "protocol_version":    "1.0.0",
            "timestamp":           time.time(),
            "waste_type":          classification.get("input_waste_type"),
            "category":            label,
            "category_key":        cat,
            "quantity_kg":         qty,
            "source_type":         classification.get("source", "residential"),
            "location":            forecast.get("location", "Unknown"),
            "recycling_status":    recycling.get("is_recyclable", False),
            "compostable":         recycling.get("is_compostable", False),
            "recycling_efficiency":recycling.get("recycling_efficiency", 0),
            "risk_score":          risk_sc,
            "risk_level":          risk.get("risk_level", "MODERATE"),
            "sustainability_score":sust_sc,
            "recycling_score":     scores.get("recycling_score", 0),
            "environmental_score": environmental.get("environmental_score", 50),
            "circular_economy_score": scores.get("circular_economy_score", 0),
            "carbon_reduction_score": scores.get("carbon_reduction_score", 0),
            "carbon_estimate_kg_co2e": carbon.get("best_method_emissions", 0),
            "best_disposal_method":    carbon.get("best_method", "N/A"),
            "co2_savings_vs_burning":  carbon.get("savings_vs_incineration", 0),
            "emergency_alerts":        emergency_alerts,
            "recommendations":         [
                classification.get("disposal_recommendation"),
                carbon.get("best_method"),
                *(scores.get("xai_reason", "").split(". ")[:2] if scores.get("xai_reason") else []),
            ],
            "actionable_triggers":     actionable_triggers,
            "weather_agent_context": {
                "note": "High temperature accelerates organic waste decomposition. Rainfall increases leachate risk.",
                "request": "Provide temperature and humidity forecast for waste odor and decomposition prediction.",
            },
            "air_quality_agent_context": {
                "note": "Burning or open dumping of this waste generates PM2.5 and toxic gases.",
                "request": "Monitor air quality near waste collection points for pollution spikes.",
            },
            "carbon_footprint_agent_context": {
                "note": f"Estimated carbon savings by choosing {carbon.get('best_method', 'recycling')}: {carbon.get('savings_vs_incineration', 0)} kg CO2e.",
                "request": "Update community carbon footprint with waste disposal emission data.",
            },
            "water_conservation_agent_context": {
                "note": "Landfill leachate and river disposal risks detected.",
                "request": "Monitor groundwater quality near waste disposal sites.",
            },
            "education_agent_context": {
                "note": f"Category: {label}. Recycling efficiency: {recycling.get('recycling_efficiency', 0)}%.",
                "request": "Generate community awareness content for this waste type.",
            },
        }


multi_agent_service = MultiAgentService()
