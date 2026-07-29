"""
WeatherWise AI - Fetch.ai uAgents Weather Agent
Implements the Fetch.ai uAgents Agent and Protocol for P2P inter-agent communication.
Extendable for AgentVerse deployment and multi-agent environmental orchestration.
"""

import logging
from uagents import Agent, Context, Protocol
from config import AGENT_NAME, AGENT_SEED, AGENT_PORT, DEFAULT_CITY
from models.schema import WeatherQueryRequest, WeatherResponse
from services.geocoding import geocode_city
from services.open_meteo import fetch_weather_data, WeatherMetrics, ForecastDay
from engine.risk_analyzer import calculate_risk_analysis
from engine.recommendation_engine import generate_recommendations
from engine.environmental_engine import generate_environmental_impact
from engine.decision_engine import build_full_weather_response

logger = logging.getLogger("WeatherWise.uAgent")

# Initialize Fetch.ai uAgent
weather_agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
    endpoint=[f"http://127.0.0.1:{AGENT_PORT}/submit"]
)

# Define uAgents Inter-Agent Protocol
weather_protocol = Protocol(name="WeatherWiseProtocol", version="1.0.0")


def execute_weather_analysis(
    city: str = None,
    lat: float = None,
    lon: float = None,
    question: str = None
) -> WeatherResponse:
    """
    Core business logic helper executing the full AI weather pipeline:
    Geocoding -> Open-Meteo Retrieval -> Risk Scoring -> Recommendations -> Environmental Analysis -> Smart Decision Engine.
    
    Args:
        city: Optional city name
        lat: Optional latitude
        lon: Optional longitude
        question: Optional natural language prompt
        
    Returns:
        WeatherResponse model object
    """
    try:
        # Step 1: Geocoding / Location Normalization
        if lat is None or lon is None:
            location_info = geocode_city(city or DEFAULT_CITY)
            target_city = location_info["name"]
            target_lat = location_info["latitude"]
            target_lon = location_info["longitude"]
            tz = location_info.get("timezone", "auto")
        else:
            target_city = city or f"Coordinates ({lat:.2f}, {lon:.2f})"
            target_lat = lat
            target_lon = lon
            tz = "auto"

        # Step 2: Open-Meteo Weather Data Fetching
        weather_raw = fetch_weather_data(target_lat, target_lon, target_city, timezone=tz)
        metrics = WeatherMetrics(**weather_raw["metrics"])
        forecast_7day = [ForecastDay(**f) for f in weather_raw["forecast_7day"]]

        # Step 3: Weather Risk Engine Analysis (0-100 Risk Score)
        risk = calculate_risk_analysis(metrics)

        # Step 4: Personalized Recommendations (Clothing, Travel, Health, 9 Activities)
        recs = generate_recommendations(metrics, risk)

        # Step 5: Environmental Intelligence Generation
        env = generate_environmental_impact(metrics)

        # Step 6: Smart Decision Engine & Output Assembly
        response = build_full_weather_response(
            metrics=metrics,
            risk=risk,
            recs=recs,
            env=env,
            forecast=forecast_7day,
            question=question
        )
        return response

    except Exception as e:
        logger.error(f"Error in execute_weather_analysis: {e}", exc_info=True)
        return WeatherResponse(
            success=False,
            timestamp="",
            location=city or "Unknown",
            latitude=lat or 0.0,
            longitude=lon or 0.0,
            metrics={},
            risk_analysis={},
            recommendations={},
            environmental_intelligence={},
            daily_summary="",
            error=str(e)
        )


@weather_agent.on_event("startup")
async def startup_handler(ctx: Context):
    """Handler triggered when the WeatherWise uAgent starts up."""
    ctx.logger.info("==================================================")
    ctx.logger.info(f"WeatherWise AI Agent Started!")
    ctx.logger.info(f"Agent Name: {weather_agent.name}")
    ctx.logger.info(f"Agent Address: {weather_agent.address}")
    ctx.logger.info(f"Listening on Port: {AGENT_PORT}")
    ctx.logger.info("==================================================")


@weather_protocol.on_message(model=WeatherQueryRequest, replies={WeatherResponse})
async def handle_weather_query(ctx: Context, sender: str, msg: WeatherQueryRequest):
    """
    uAgents Message Handler for processing incoming WeatherQueryRequest messages from other agents or clients.
    """
    ctx.logger.info(f"Received Weather Query from {sender}. City: '{msg.city}', Question: '{msg.question}'")

    # Run weather pipeline
    response = execute_weather_analysis(
        city=msg.city,
        lat=msg.latitude,
        lon=msg.longitude,
        question=msg.question
    )

    ctx.logger.info(f"Analysis completed for '{response.location}'. Risk Score: {response.risk_analysis.get('risk_score')}/100")
    
    # Send structured WeatherResponse back to requesting agent
    await ctx.send(sender, response)


@weather_agent.on_interval(period=60.0)
async def periodic_telemetry_broadcast(ctx: Context):
    """
    Autonomous interval handler simulating periodic environmental weather telemetry broadcast
    for multi-agent coordinator nodes.
    """
    telemetry = execute_weather_analysis(city=DEFAULT_CITY)
    risk_score = telemetry.risk_analysis.get("risk_score", 0)
    ctx.logger.info(
        f"[Autonomous Telemetry Broadcast] {DEFAULT_CITY} Weather: "
        f"{telemetry.metrics.get('temperature_c')}°C, {telemetry.metrics.get('weather_condition')}. "
        f"Risk Score: {risk_score}/100 ({telemetry.risk_analysis.get('risk_level')})"
    )


# Include protocol in agent
weather_agent.include(weather_protocol)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    weather_agent.run()
