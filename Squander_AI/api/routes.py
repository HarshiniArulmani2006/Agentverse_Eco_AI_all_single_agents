"""
FastAPI REST API Routes for EcoWaste AI
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

from services.waste_classification_engine import waste_classification_engine
from services.recycling_engine import recycling_engine
from services.environmental_engine import environmental_engine
from services.collection_engine import collection_engine
from services.prediction_engine import prediction_engine
from services.risk_engine import risk_engine
from services.sustainability_engine import sustainability_engine
from services.conversational_engine import conversational_engine
from services.multi_agent_service import multi_agent_service

router = APIRouter()


# ──────────────────────────────────────────────
# Request Models
# ──────────────────────────────────────────────
class WasteAnalysisRequest(BaseModel):
    waste_type: str
    quantity_kg: float = 1.0
    location: str = "City"
    source: str = "residential"    # residential | commercial | industrial


class ConversationalRequest(BaseModel):
    query: str
    waste_type: Optional[str] = "plastic bottle"
    quantity_kg: Optional[float] = 1.0
    source: Optional[str] = "residential"


# ──────────────────────────────────────────────
# Core Helper: Full Analysis Pipeline
# ──────────────────────────────────────────────
def _run_full_analysis(waste_type: str, quantity_kg: float, location: str, source: str) -> dict:
    # 1. Classify
    cls = waste_classification_engine.classify(waste_type, quantity_kg, source)

    # 2. Recycling intelligence
    rec = recycling_engine.analyze(cls)

    # 3. Environmental impact
    env = environmental_engine.calculate_environmental_impact(cls)

    # 4. Carbon footprint
    carbon = environmental_engine.estimate_carbon_footprint(cls)

    # 5. Risk analysis
    risk_data = risk_engine.calculate_risk_score(cls)

    # 6. Emergency alerts
    alerts = risk_engine.detect_emergency_alerts(cls)

    # 7. Pollution sources
    pollution_sources = risk_engine.detect_pollution_sources(cls)

    # 8. Sustainability scores
    scores = sustainability_engine.calculate_ai_scores(cls, risk_data["risk_score"])

    # 9. Recommendations
    recommendations = sustainability_engine.get_recommendations(cls)

    # 10. Circular economy
    circular_insight = sustainability_engine.get_circular_economy_insight(cls)

    # 11. Forecast
    forecast = prediction_engine.forecast_waste_generation(source=source, location=location)

    # 12. Multi-agent payload
    payload = multi_agent_service.build_standardized_payload(
        classification=cls,
        recycling=rec,
        risk=risk_data,
        environmental=env,
        carbon=carbon,
        scores=scores,
        emergency_alerts=alerts,
        forecast=forecast,
    )

    return {
        "classification":            cls,
        "recycling":                 rec,
        "environmental_impact":      env,
        "carbon_footprint":          carbon,
        "risk_assessment":           risk_data,
        "emergency_alerts":          alerts,
        "pollution_sources":         pollution_sources,
        "sustainability_scores":     scores,
        "sustainability_recommendations": recommendations,
        "circular_economy_insight":  circular_insight,
        "forecast":                  forecast,
        "multi_agent_payload":       payload,
    }


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@router.post("/analyze")
async def analyze_waste(req: WasteAnalysisRequest):
    """
    Full AI Waste Analysis pipeline.
    Accepts waste type, quantity, location, and source.
    """
    if not req.waste_type or len(req.waste_type.strip()) < 2:
        raise HTTPException(status_code=400, detail="Please provide a valid waste type (min 2 characters).")
    if req.quantity_kg <= 0 or req.quantity_kg > 100_000:
        raise HTTPException(status_code=400, detail="Quantity must be between 0 and 100,000 kg.")

    return _run_full_analysis(
        waste_type=req.waste_type.strip(),
        quantity_kg=req.quantity_kg,
        location=req.location,
        source=req.source,
    )


@router.get("/classify")
async def classify_waste(
    waste_type: str = Query(..., description="Waste type, e.g. 'plastic bottle'"),
    quantity_kg: float = Query(1.0, description="Quantity in kg"),
    source: str = Query("residential", description="Source type"),
):
    """Quick waste classification endpoint."""
    return waste_classification_engine.classify(waste_type, quantity_kg, source)


@router.get("/smart-bins")
async def get_smart_bins():
    """Return live smart bin monitoring status."""
    return collection_engine.get_collection_summary()


@router.get("/forecast")
async def get_forecast(
    source: str = Query("residential", description="Source type: residential | commercial | industrial"),
    month: int = Query(7, description="Month number (1-12)"),
    location: str = Query("City", description="Location name"),
):
    """Waste generation forecast (daily, weekly, monthly, seasonal)."""
    return {
        "forecast": prediction_engine.forecast_waste_generation(source, month, location),
        "anomalies": prediction_engine.detect_anomalies(),
        "community_analytics": prediction_engine.get_community_analytics(source),
    }


@router.get("/sustainability-report")
async def get_sustainability_report(
    waste_type: str = Query("plastic bottle", description="Waste type"),
    quantity_kg: float = Query(1.0, description="Quantity in kg"),
    source: str = Query("residential"),
    location: str = Query("City"),
):
    """Generate full AI Sustainability Report."""
    analysis = _run_full_analysis(waste_type, quantity_kg, location, source)
    report   = sustainability_engine.generate_sustainability_report(analysis)
    return {
        "sustainability_report": report,
        "eco_badges":     sustainability_engine.get_eco_badges(),
        "eco_challenges": sustainability_engine.get_eco_challenges(),
        "full_analysis":  analysis,
    }


@router.post("/query")
async def conversational_query(req: ConversationalRequest):
    """Conversational AI Q&A about waste management."""
    cls    = waste_classification_engine.classify(req.waste_type, req.quantity_kg, req.source)
    rec    = recycling_engine.analyze(cls)
    env    = environmental_engine.calculate_environmental_impact(cls)
    carbon = environmental_engine.estimate_carbon_footprint(cls)
    risk_d = risk_engine.calculate_risk_score(cls)
    return conversational_engine.answer_query(
        req.query, cls, rec, risk_d, env, carbon
    )


@router.get("/multi-agent-payload")
async def get_multi_agent_payload(
    waste_type: str = Query("plastic bottle"),
    quantity_kg: float = Query(1.0),
    location: str = Query("City"),
    source: str = Query("residential"),
):
    """Return standardized multi-agent JSON payload."""
    analysis = _run_full_analysis(waste_type, quantity_kg, location, source)
    return analysis["multi_agent_payload"]


@router.get("/eco-challenges")
async def get_eco_challenges():
    """Return AI eco challenges and badges."""
    return {
        "eco_challenges": sustainability_engine.get_eco_challenges(),
        "eco_badges":     sustainability_engine.get_eco_badges(),
    }


@router.get("/dashboard-data")
async def get_dashboard_data():
    """
    Aggregated dashboard data endpoint — called on page load.
    Returns bins, forecast, community analytics, and sample analysis.
    """
    bins_data  = collection_engine.get_collection_summary()
    forecast   = prediction_engine.forecast_waste_generation()
    community  = prediction_engine.get_community_analytics()
    anomalies  = prediction_engine.detect_anomalies()
    badges     = sustainability_engine.get_eco_badges()
    challenges = sustainability_engine.get_eco_challenges()
    sample     = _run_full_analysis("plastic bottle", 1.0, "City", "residential")

    return {
        "smart_bins":           bins_data,
        "forecast":             forecast,
        "community_analytics":  community,
        "anomalies":            anomalies,
        "eco_badges":           badges,
        "eco_challenges":       challenges,
        "sample_analysis":      sample,
    }


@router.get("/health")
async def health_check():
    return {
        "status": "online",
        "agent": "EcoWaste AI",
        "version": "1.0.0",
        "framework": "Fetch.ai uAgents + FastAPI",
    }
