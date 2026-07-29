"""
agents/waste_agent.py – Dedicated EcoWaste AI uAgent Initialization
Extracts the uAgent setup from multi_agent_service.py into a clean module.
"""
import time
from typing import List, Dict, Any

from uagents import Agent, Context, Protocol

from config import AGENT_NAME, AGENT_SEED, AGENT_PORT, AGENT_ENDPOINT
from agents.protocol import (
    WasteQueryMessage, WasteResponseMessage,
    CarbonNotificationMessage, WaterAlertMessage,
    AirAlertMessage, EducationRequestMessage,
    CoordinatorNotificationMessage,
)

# ──────────────────────────────────────────────────────────────
# Initialize the EcoWaste AI uAgent
# ──────────────────────────────────────────────────────────────
waste_agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
    endpoint=AGENT_ENDPOINT,
)

# Register the EcoWaste communication protocol
waste_protocol = Protocol(name="EcoWasteProtocol", version="1.0.0")


# ──────────────────────────────────────────────────────────────
# Message Handlers
# ──────────────────────────────────────────────────────────────

@waste_protocol.on_message(model=WasteQueryMessage)
async def handle_waste_query(ctx: Context, sender: str, msg: WasteQueryMessage):
    """
    Handle incoming waste analysis requests from partner agents.
    Runs the full classification pipeline and returns a standardized response.
    """
    ctx.logger.info(
        f"[EcoWaste AI] Received query from {sender}: "
        f"{msg.waste_type} | {msg.quantity_kg} kg | {msg.location} | {msg.source}"
    )

    # Lazy import to avoid circular imports at module level
    from services.waste_classification_engine import waste_classification_engine
    from services.recycling_engine            import recycling_engine
    from services.environmental_engine        import environmental_engine
    from services.risk_engine                 import risk_engine
    from services.sustainability_engine       import sustainability_engine

    # Run analysis pipeline
    cls      = waste_classification_engine.classify(msg.waste_type, msg.quantity_kg, msg.source)
    rec      = recycling_engine.analyze(cls)
    env      = environmental_engine.calculate_environmental_impact(cls)
    carbon   = environmental_engine.estimate_carbon_footprint(cls)
    risk_data = risk_engine.calculate_risk_score(cls)
    alerts   = risk_engine.detect_emergency_alerts(cls)
    scores   = sustainability_engine.calculate_ai_scores(cls, risk_data["risk_score"])

    response = WasteResponseMessage(
        sender_agent         = "EcoWaste_AI_Agent",
        target_agents        = [sender],
        timestamp            = time.time(),
        waste_type           = msg.waste_type,
        category             = cls["category_label"],
        risk_level           = risk_data["risk_level"],
        risk_score           = float(risk_data["risk_score"]),
        sustainability_score = float(scores.get("sustainability_score", 0)),
        recycling_status     = bool(rec.get("is_recyclable", False)),
        carbon_estimate      = float(carbon.get("best_method_emissions", 0)),
        environmental_score  = float(env.get("environmental_score", 0)),
        emergency_alerts     = alerts,
        actionable_triggers  = {
            "recycling_dispatch": rec.get("is_recyclable", False),
            "hazmat_required":    cls.get("is_toxic", False),
            "emergency_response": len(alerts) > 0,
        },
        recommendations      = [
            cls.get("disposal_recommendation", ""),
            carbon.get("best_method", ""),
        ],
    )
    await ctx.send(sender, response)
    ctx.logger.info(f"[EcoWaste AI] Response sent to {sender}: {cls['category_label']} | Risk: {risk_data['risk_level']}")


# Register protocol with agent
waste_agent.include(waste_protocol)
