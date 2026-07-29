"""
WeatherWise AI - Smart Decision Engine & Conversational Intelligence
Processes natural language queries, generates natural-language daily weather summaries,
makes intelligent lifestyle/planning decisions, and builds multi-agent JSON payloads.
"""

import time
import logging
from typing import Dict, Any, Optional, List
from models.schema import (
    WeatherMetrics,
    RiskAnalysis,
    PersonalizedRecommendations,
    EnvironmentalImpact,
    ForecastDay,
    WeatherResponse,
    MultiAgentHeader,
    MultiAgentPayload
)

logger = logging.getLogger("WeatherWise.DecisionEngine")


def generate_daily_summary(metrics: WeatherMetrics, risk: RiskAnalysis, recs: PersonalizedRecommendations) -> str:
    """
    Generates a natural-language daily weather summary.
    
    Example:
        Today's Weather Summary
        Warm and humid weather is expected throughout the day.
        Light rain is likely during the evening.
        Carry an umbrella if you plan to go outside.
        Outdoor activities are recommended only before noon.
        Travel conditions remain generally safe.
    """
    lines = [f"Today's Weather Summary for {metrics.city}:"]

    # Condition & Temp description
    temp = metrics.temperature_c
    if temp >= 35.0:
        lines.append("Hot and intense heatwave conditions expected throughout the day.")
    elif temp >= 28.0:
        lines.append("Warm and moderately humid weather is expected throughout the day.")
    elif temp >= 18.0:
        lines.append("Mild and pleasant weather conditions are expected across the region.")
    else:
        lines.append("Chilly temperatures expected throughout the day.")

    # Rain outlook
    if metrics.rain_probability >= 70:
        lines.append("Heavy rainfall is very likely. Carry an umbrella and waterproof jacket if stepping outside.")
    elif metrics.rain_probability >= 40:
        lines.append("Light to moderate scattered rain showers likely during the day. Carry an umbrella.")
    else:
        lines.append("Precipitation risk remains low with dry conditions prevailing.")

    # Outdoor activities guidance
    top_activities = [a for a in recs.outdoor_activities if a.status in ["EXCELLENT", "GOOD"]]
    if top_activities:
        act_names = ", ".join([a.activity_name for a in top_activities[:3]])
        lines.append(f"Outdoor activities like {act_names} are highly recommended.")
    else:
        lines.append("Outdoor activities are recommended to be limited or postponed due to weather conditions.")

    # Travel & Safety outlook
    lines.append(f"Travel Advice: {recs.travel_advice}.")

    return "\n".join(lines)


def process_conversational_query(
    question: str,
    metrics: WeatherMetrics,
    risk: RiskAnalysis,
    recs: PersonalizedRecommendations,
    forecast: List[ForecastDay]
) -> str:
    """
    Processes a natural language query and returns a reasoned, intelligent decision answer.
    
    Supports queries like:
    - Will it rain today?
    - Should I carry an umbrella?
    - Can I go for a bike ride?
    - Is today good for travelling?
    - Can I wash clothes today?
    - Is today suitable for farming?
    - Is it safe to drive?
    - What should I wear today?
    - Is tomorrow better than today?
    - I'm planning a picnic tomorrow.
    """
    q_clean = question.strip().lower()

    # --- Query 1: Rain & Umbrella ---
    if any(k in q_clean for k in ["rain", "umbrella", "shower", "downpour"]):
        if metrics.rain_probability >= 50 or metrics.wmo_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95]:
            return (
                f"Yes, rain is expected in {metrics.city} today with a probability of {metrics.rain_probability}%. "
                f"Condition: {metrics.weather_condition}. You should definitely carry an umbrella and wear waterproof shoes."
            )
        else:
            return (
                f"No heavy rain expected in {metrics.city} today. Rain probability is only {metrics.rain_probability}%. "
                f"Current condition is {metrics.weather_condition}. An umbrella is not strictly necessary, though carrying a light coat is fine."
            )

    # --- Query 2: Bike Ride / Cycling / Running / Walking ---
    if any(k in q_clean for k in ["bike", "cycling", "ride", "cycle"]):
        cycling_act = next((a for a in recs.outdoor_activities if a.activity_name == "Cycling"), None)
        if cycling_act and cycling_act.suitable:
            return (
                f"Yes, conditions for cycling are {cycling_act.status} (Suitability Score: {cycling_act.suitability_score}/100). "
                f"Reason: {cycling_act.reason}"
            )
        else:
            reason = cycling_act.reason if cycling_act else "Weather conditions are unfavorable."
            return f"Cycling is not recommended today ({cycling_act.status if cycling_act else 'UNSUITABLE'}). Reason: {reason}"

    # --- Query 3: Picnic ---
    if "picnic" in q_clean:
        target_day = "tomorrow" if "tomorrow" in q_clean else "today"
        if target_day == "tomorrow" and len(forecast) > 1:
            f_tomorrow = forecast[1]
            if f_tomorrow.rain_probability < 30 and f_tomorrow.max_temp_c <= 32.0:
                return (
                    f"Tomorrow looks like a great day for a picnic in {metrics.city}! "
                    f"Rain probability is only {f_tomorrow.rain_probability}%, temperatures will peak around {f_tomorrow.max_temp_c:.1f}°C, "
                    f"and condition will be {f_tomorrow.weather_condition}. Carry sunscreen and drinking water."
                )
            else:
                return (
                    f"Tomorrow may be challenging for a picnic in {metrics.city}. "
                    f"Rain probability is {f_tomorrow.rain_probability}%, expected condition: {f_tomorrow.weather_condition}, "
                    f"max temperature: {f_tomorrow.max_temp_c:.1f}°C. Consider indoor alternatives or postponing."
                )
        else:
            picnic_act = next((a for a in recs.outdoor_activities if a.activity_name == "Picnics"), None)
            score_text = f"{picnic_act.suitability_score}/100" if picnic_act else "N/A"
            return (
                f"Today's picnic suitability score is {score_text} ({picnic_act.status if picnic_act else 'UNSUITABLE'}). "
                f"Reason: {picnic_act.reason if picnic_act else 'Unfavorable weather'}."
            )

    # --- Query 4: Travel / Driving Safety ---
    if any(k in q_clean for k in ["travel", "driving", "drive", "road", "trip"]):
        return (
            f"Travel Assessment for {metrics.city}: Status is '{recs.travel_advice}'. "
            f"Risk Level: {risk.risk_level} (Score: {risk.risk_score}/100). "
            + " ".join(recs.travel_details)
        )

    # --- Query 5: Laundry / Wash Clothes ---
    if any(k in q_clean for k in ["wash", "laundry", "clothes", "dry"]):
        if metrics.rain_probability < 30 and metrics.relative_humidity < 75 and metrics.cloud_cover < 60:
            return (
                f"Yes, today is a good day to wash clothes in {metrics.city}! "
                f"Cloud cover is low ({metrics.cloud_cover}%), humidity is {metrics.relative_humidity}%, and rain probability is low ({metrics.rain_probability}%). "
                f"Clothes should dry efficiently."
            )
        else:
            return (
                f"Washing clothes outdoor today is NOT recommended. "
                f"Rain probability is {metrics.rain_probability}%, relative humidity is high at {metrics.relative_humidity}%, "
                f"and condition is {metrics.weather_condition}. Drying may take longer or require indoor drying."
            )

    # --- Query 6: Farming / Agriculture ---
    if any(k in q_clean for k in ["farm", "farming", "crop", "irrigation", "agriculture"]):
        if metrics.rain_probability >= 60:
            return (
                f"Rain is expected today ({metrics.rain_probability}% probability). "
                f"Irrigation is NOT required today as natural precipitation will water crops. Hold off on pesticide spraying."
            )
        elif metrics.temperature_c >= 35.0:
            return (
                f"High temperatures ({metrics.temperature_c}°C) and evapotranspiration today. "
                f"Irrigation is HIGHLY recommended to protect crops from heat stress."
            )
        else:
            return (
                f"Farming conditions in {metrics.city}: Moderate irrigation recommended. "
                f"Temperature is {metrics.temperature_c}°C, humidity {metrics.relative_humidity}%, rain probability {metrics.rain_probability}%."
            )

    # --- Query 7: What to wear / Clothing ---
    if any(k in q_clean for k in ["wear", "dress", "outfit", "clothes"]):
        clothing_str = "; ".join(recs.clothing)
        return f"Recommended attire for {metrics.city} today ({metrics.temperature_c}°C, {metrics.weather_condition}): {clothing_str}."

    # --- Query 8: Tomorrow vs Today Comparison ---
    if any(k in q_clean for k in ["tomorrow better", "tomorrow vs", "compare tomorrow"]):
        if len(forecast) > 1:
            f_tom = forecast[1]
            tom_rain = f_tom.rain_probability
            tom_temp = f_tom.max_temp_c
            return (
                f"Comparison for {metrics.city}: Today has temp of {metrics.temperature_c}°C with {metrics.rain_probability}% rain. "
                f"Tomorrow will have a max temp of {tom_temp:.1f}°C, rain probability of {tom_rain}%, and condition '{f_tom.weather_condition}'. "
                + ("Tomorrow looks calmer with less rain." if tom_rain < metrics.rain_probability else "Today has lower rain risk than tomorrow.")
            )

    # --- Default General Decision Response ---
    return (
        f"In {metrics.city}, current weather is {metrics.weather_condition} at {metrics.temperature_c}°C "
        f"(Feels like {metrics.feels_like_c}°C). Risk score: {risk.risk_score}/100 ({risk.risk_level}). "
        f"Primary advice: {recs.travel_advice}. "
        + (" ".join(recs.clothing[:2]) if recs.clothing else "")
    )


def build_full_weather_response(
    metrics: WeatherMetrics,
    risk: RiskAnalysis,
    recs: PersonalizedRecommendations,
    env: EnvironmentalImpact,
    forecast: List[ForecastDay],
    question: Optional[str] = None
) -> WeatherResponse:
    """
    Assembles complete WeatherResponse object containing human summary,
    smart decision answers, risk telemetry, and standardized Multi-Agent payload.
    """
    timestamp_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    daily_summary = generate_daily_summary(metrics, risk, recs)

    decision_ans = None
    if question:
        decision_ans = process_conversational_query(question, metrics, risk, recs, forecast)

    # Build Multi-Agent Interoperability Payload
    ma_header = MultiAgentHeader(timestamp=timestamp_str)
    
    triggers = []
    if risk.risk_score >= 50:
        triggers.append("SEVERE_WEATHER_ALERT")
    if env.solar_power_potential in ["EXCELLENT", "HIGH"]:
        triggers.append("MAXIMIZE_SOLAR_GRID_DISPATCH")
    if "NONE" in env.irrigation_need or "EXPECTED" in env.irrigation_need:
        triggers.append("SUSPEND_MUNICIPAL_IRRIGATION")
    if env.wildfire_risk in ["HIGH", "EXTREME"]:
        triggers.append("WILDFIRE_MONITORING_ALERT")

    ma_payload = MultiAgentPayload(
        header=ma_header,
        location=metrics.city,
        coordinates={"latitude": metrics.latitude, "longitude": metrics.longitude},
        weather_summary={
            "temperature_c": metrics.temperature_c,
            "condition": metrics.weather_condition,
            "humidity": metrics.relative_humidity,
            "wind_speed_kmh": metrics.wind_speed_kmh,
            "rain_probability": metrics.rain_probability,
            "uv_index": metrics.uv_index
        },
        risk_assessment={
            "risk_score": risk.risk_score,
            "risk_level": risk.risk_level,
            "detected_anomalies": risk.detected_conditions
        },
        environmental_impacts=env.model_dump(),
        actionable_triggers=triggers
    )

    return WeatherResponse(
        success=True,
        timestamp=timestamp_str,
        location=metrics.city,
        latitude=metrics.latitude,
        longitude=metrics.longitude,
        metrics=metrics.model_dump(),
        risk_analysis=risk.model_dump(),
        recommendations=recs.model_dump(),
        environmental_intelligence=env.model_dump(),
        daily_summary=daily_summary,
        decision_answer=decision_ans,
        forecast_7day=[f.model_dump() for f in forecast],
        multi_agent_payload=ma_payload.model_dump()
    )
