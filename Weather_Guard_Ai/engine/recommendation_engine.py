"""
WeatherWise AI - Personalized Recommendation Engine
Generates clothing suggestions, travel advice, health tips,
and outdoor activity suitability ratings for 9 specific activities.
"""

import logging
from typing import Dict, Any, List
from models.schema import WeatherMetrics, RiskAnalysis, PersonalizedRecommendations, OutdoorActivity

logger = logging.getLogger("WeatherWise.RecommendationEngine")


def generate_recommendations(metrics: WeatherMetrics, risk: RiskAnalysis) -> PersonalizedRecommendations:
    """
    Synthesizes tailored recommendations for clothing, travel, health, and 9 outdoor activities.
    
    Args:
        metrics: Weather telemetry metrics
        risk: Weather risk analysis output
        
    Returns:
        PersonalizedRecommendations object
    """
    temp = metrics.temperature_c
    rain_prob = metrics.rain_probability
    wind_speed = metrics.wind_speed_kmh
    uv_index = metrics.uv_index
    humidity = metrics.relative_humidity
    wmo_code = metrics.wmo_code
    visibility = metrics.visibility_m

    # --- 1. Clothing Suggestions ---
    clothing: List[str] = []
    if temp >= 30.0:
        clothing.append("Wear breathable, light-colored cotton or linen clothes")
    elif 18.0 <= temp < 30.0:
        clothing.append("Wear comfortable casual attire")
    elif 10.0 <= temp < 18.0:
        clothing.append("Carry a light jacket or cardigan")
    else:
        clothing.append("Wear heavy thermal layers, jacket, and warm socks")

    if rain_prob >= 40 or wmo_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95]:
        clothing.append("Carry an umbrella and wear a waterproof raincoat")
        clothing.append("Wear waterproof or rubber-soled footwear")

    if uv_index >= 6.0:
        clothing.append("Carry UV-protection sunglasses and wear a wide-brim hat")
        clothing.append("Apply broad-spectrum SPF 30+ sunscreen before stepping out")

    # --- 2. Travel Advice ---
    travel_advice = "Safe for travel"
    travel_details: List[str] = []

    if risk.risk_level in ["HIGH", "CRITICAL"]:
        travel_advice = "Avoid unnecessary travel"
        travel_details.append("Severe weather warnings are active in your area.")
    elif rain_prob >= 60 or wmo_code in [63, 65, 81, 82, 95]:
        travel_advice = "Drive carefully with extra precaution"
        travel_details.append("Roads may be slippery; maintain extra braking distance.")
        travel_details.append("Expect traffic slowdowns due to localized waterlogging.")
    elif wmo_code in [45, 48] or visibility < 1000:
        travel_advice = "Drive carefully using fog lights"
        travel_details.append("Low visibility requires low-beam headlights and reduced speed.")
    else:
        travel_details.append("Traffic and road conditions are generally favorable.")
        travel_details.append("Maintain standard road safety precautions.")

    # --- 3. Health Advice ---
    health_advice: List[str] = []
    if temp >= 32.0 or humidity >= 70:
        health_advice.append("Stay hydrated: drink plenty of water and electrolytes throughout the day.")
    if temp >= 35.0 or uv_index >= 8.0:
        health_advice.append("Avoid strenuous outdoor activities during peak sunlight (11:00 AM – 04:00 PM).")
    if humidity < 35:
        health_advice.append("Air is dry: use lip balm and moisturize skin to avoid dehydration.")
    if risk.risk_score < 25:
        health_advice.append("Weather is pleasant: great day for light outdoor relaxation.")

    # --- 4. Outdoor Activities Evaluation (9 Activities) ---
    activities = _evaluate_outdoor_activities(metrics, risk)

    return PersonalizedRecommendations(
        clothing=clothing,
        travel_advice=travel_advice,
        travel_details=travel_details,
        health_advice=health_advice,
        outdoor_activities=activities
    )


def _evaluate_outdoor_activities(metrics: WeatherMetrics, risk: RiskAnalysis) -> List[OutdoorActivity]:
    """Evaluates suitability scores (0-100) and statuses for 9 specific outdoor activities."""
    temp = metrics.temperature_c
    rain_prob = metrics.rain_probability
    wind_speed = metrics.wind_speed_kmh
    uv_index = metrics.uv_index
    wmo_code = metrics.wmo_code

    is_stormy_or_heavy_rain = wmo_code in [65, 67, 82, 95, 96, 99] or rain_prob >= 75 or wind_speed >= 45.0

    activities_spec = [
        ("Walking", 15.0, 32.0, 30.0, 40),
        ("Cycling", 15.0, 30.0, 25.0, 30),
        ("Running", 12.0, 26.0, 20.0, 25),
        ("Cricket", 18.0, 34.0, 20.0, 20),
        ("Football", 15.0, 32.0, 25.0, 35),
        ("Hiking", 14.0, 28.0, 25.0, 25),
        ("Trekking", 12.0, 26.0, 22.0, 25),
        ("Camping", 15.0, 28.0, 20.0, 20),
        ("Picnics", 18.0, 30.0, 18.0, 20),
    ]

    evaluated: List[OutdoorActivity] = []

    for name, min_temp, max_temp, max_wind, max_rain in activities_spec:
        score = 100
        reasons: List[str] = []

        if is_stormy_or_heavy_rain:
            score = 0
            reasons.append("Severe rain/thunderstorm makes outdoor activity unsafe")
        else:
            # Rain penalty
            if rain_prob > max_rain:
                penalty = (rain_prob - max_rain) * 1.5
                score -= penalty
                reasons.append(f"High rain probability ({rain_prob}%)")

            # Wind penalty
            if wind_speed > max_wind:
                penalty = (wind_speed - max_wind) * 2.0
                score -= penalty
                reasons.append(f"Wind gusts of {wind_speed:.0f} km/h")

            # Temperature penalty
            if temp > max_temp:
                score -= (temp - max_temp) * 4.0
                reasons.append(f"Hot temperature ({temp:.1f}°C)")
            elif temp < min_temp:
                score -= (min_temp - temp) * 3.5
                reasons.append(f"Chilly temperature ({temp:.1f}°C)")

            # UV Penalty for intense outdoor sports/picnics
            if uv_index >= 8.0 and name in ["Picnics", "Cricket", "Trekking", "Camping"]:
                score -= 15
                reasons.append(f"High UV radiation ({uv_index})")

        score = int(min(max(score, 0), 100))

        if score >= 80:
            status = "EXCELLENT"
            suitable = True
            reason_text = "Ideal environmental conditions for " + name.lower() + "."
        elif score >= 55:
            status = "GOOD"
            suitable = True
            reason_text = "Favorable conditions. " + ("; ".join(reasons) if reasons else "Proceed normally.")
        elif score >= 30:
            status = "CAUTION"
            suitable = True
            reason_text = "Exercise caution due to: " + ("; ".join(reasons) if reasons else "marginal weather.")
        else:
            status = "UNSUITABLE"
            suitable = False
            reason_text = "Not recommended today: " + ("; ".join(reasons) if reasons else "unfavorable weather.")

        evaluated.append(
            OutdoorActivity(
                activity_name=name,
                suitable=suitable,
                status=status,
                suitability_score=score,
                reason=reason_text
            )
        )

    return evaluated
