"""
Fetch.ai AgentVerse (uAgents) Framework Integration & Multi-Agent Payload Generator
"""
import time
from typing import Dict, Any, List
from uagents import Agent, Context, Protocol, Model
from pydantic import BaseModel
from config import AGENT_NAME, AGENT_SEED, AGENT_PORT, AGENT_ENDPOINT

# uAgent Message Protocol Models
class AirQualityQueryMessage(Model):
    city: str
    latitude: float
    longitude: float

class AirQualityResponseMessage(Model):
    sender_agent: str
    target_agents: List[str]
    timestamp: float
    location: str
    aqi: float
    risk_score: float
    health_score: float
    dominant_pattern: str
    emergency_alerts: List[Dict[str, Any]]
    actionable_triggers: Dict[str, Any]

# Initialize uAgent
air_quality_agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
    endpoint=AGENT_ENDPOINT
)

air_quality_protocol = Protocol(name="AirGuardProtocol", version="1.0.0")

@air_quality_protocol.on_message(model=AirQualityQueryMessage)
async def handle_air_query(ctx: Context, sender: str, msg: AirQualityQueryMessage):
    ctx.logger.info(f"Received Air Quality query from {sender} for location: {msg.city}")
    # Respond with standardized message payload
    response = AirQualityResponseMessage(
        sender_agent="AirGuard_AI_Agent",
        target_agents=["WeatherAgent", "WasteManagementAgent", "CarbonFootprintAgent", "WaterConservationAgent", "CoordinatorAgent"],
        timestamp=time.time(),
        location=msg.city,
        aqi=120.0,
        risk_score=68.5,
        health_score=55.0,
        dominant_pattern="Traffic Pollution",
        emergency_alerts=[],
        actionable_triggers={"water_sprinklers_needed": True, "traffic_reroute_recommended": True}
    )
    await ctx.send(sender, response)

air_quality_agent.include(air_quality_protocol)

class MultiAgentService:

    def build_standardized_payload(
        self,
        city: str,
        air_data: Dict[str, Any],
        risk_data: Dict[str, Any],
        scores: Dict[str, float],
        alerts: List[Dict[str, Any]],
        patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        aqi = air_data.get("current", {}).get("aqi", 0)
        pm2_5 = air_data.get("current", {}).get("pm2_5", 0.0)
        pm10 = air_data.get("current", {}).get("pm10", 0.0)

        actionable_triggers = {
            "water_sprinklers_needed": pm10 > 80 or patterns.get("probabilities", {}).get("dust_storm", 0) > 50,
            "traffic_reroute_recommended": patterns.get("probabilities", {}).get("traffic_pollution", 0) > 70,
            "industrial_emissions_audit_required": patterns.get("probabilities", {}).get("industrial_pollution", 0) > 75,
            "public_health_warning_active": aqi > 150,
            "open_burning_ban_enforced": patterns.get("probabilities", {}).get("wildfire_smoke", 0) > 40
        }

        return {
            "sender_agent": "AirGuard_AI_Agent",
            "agent_address": air_quality_agent.address,
            "target_agents": [
                "WeatherAgent",
                "WasteManagementAgent",
                "CarbonFootprintAgent",
                "WaterConservationAgent",
                "EnvironmentalEducationAgent",
                "CoordinatorAgent"
            ],
            "timestamp": time.time(),
            "location": city,
            "coordinates": {
                "latitude": air_data.get("latitude"),
                "longitude": air_data.get("longitude")
            },
            "AQI": aqi,
            "risk_score": risk_data.get("score"),
            "health_score": scores.get("health_safety_score"),
            "environmental_score": scores.get("environmental_score"),
            "sustainability_index": scores.get("sustainability_score"),
            "dominant_pollution_pattern": patterns.get("dominant_pattern"),
            "emergency_alerts": alerts,
            "recommendations": {
                "health": risk_data.get("reason"),
                "mask_required": pm2_5 > 35 or aqi > 100
            },
            "actionable_triggers": actionable_triggers
        }

multi_agent_service = MultiAgentService()
