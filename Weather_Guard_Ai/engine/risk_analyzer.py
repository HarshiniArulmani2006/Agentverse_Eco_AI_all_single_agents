"""
WeatherWise AI - Risk Analyzer Engine
Calculates dynamic Weather Risk Score (0-100), detects severe weather conditions,
and triggers Emergency Safety Alerts.
"""

import logging
from typing import Dict, Any, List
from models.schema import WeatherMetrics, RiskAnalysis

logger = logging.getLogger("WeatherWise.RiskAnalyzer")


def calculate_risk_analysis(metrics: WeatherMetrics) -> RiskAnalysis:
    """
    Evaluates weather telemetry to calculate a Weather Risk Score (0-100),
    assign a Risk Level, enumerate specific reasons, detect weather anomalies,
    and generate emergency safety warnings.
    
    Args:
        metrics: Populated WeatherMetrics object
        
    Returns:
        RiskAnalysis object
    """
    risk_score = 0
    reasons: List[str] = []
    detected_conditions: List[str] = []
    emergency_alerts: List[Dict[str, str]] = []

    temp = metrics.temperature_c
    feels_like = metrics.feels_like_c
    humidity = metrics.relative_humidity
    wind_speed = metrics.wind_speed_kmh
    wmo_code = metrics.wmo_code
    rain_prob = metrics.rain_probability
    uv_index = metrics.uv_index
    visibility = metrics.visibility_m

    # --- 1. Temperature Anomaly Detection ---
    if temp >= 42.0 or feels_like >= 45.0:
        risk_score += 40
        reasons.append(f"Extreme Heatwave detected ({temp}°C, feels like {feels_like}°C)")
        detected_conditions.append("Severe Heatwave")
        emergency_alerts.append({
            "title": "HEATWAVE RED ALERT",
            "warning": "Dangerously high temperatures detected. Avoid direct sun exposure and stay hydrated.",
            "safety": "Stay indoors between 11 AM and 4 PM. Drink electro-water or fluids frequently."
        })
    elif temp >= 38.0 or feels_like >= 40.0:
        risk_score += 25
        reasons.append(f"High Heatwave conditions ({temp}°C)")
        detected_conditions.append("Heatwave")
        emergency_alerts.append({
            "title": "HEATWAVE WARNING",
            "warning": "Elevated temperatures present risk of heat exhaustion.",
            "safety": "Limit outdoor strenuous activity and seek shaded/air-conditioned environments."
        })
    elif temp <= 0.0:
        risk_score += 30
        reasons.append(f"Freezing temperature detected ({temp}°C)")
        detected_conditions.append("Freezing Cold")
        emergency_alerts.append({
            "title": "FREEZE & ICE ALERT",
            "warning": "Sub-zero temperatures may cause black ice on roads and frostbite risk.",
            "safety": "Dress in thermal layers, insulate pipes, and exercise extreme caution when driving."
        })
    elif temp <= 8.0:
        risk_score += 15
        reasons.append(f"Chilly cold weather ({temp}°C)")
        detected_conditions.append("Cold Weather")

    # --- 2. Precipitation & Thunderstorm Detection ---
    if wmo_code in [95, 96, 99]:
        risk_score += 45
        reasons.append("Active Thunderstorm and lightning risk")
        detected_conditions.append("Thunderstorm")
        emergency_alerts.append({
            "title": "THUNDERSTORM & LIGHTNING WARNING",
            "warning": "Severe thunderstorm activity reported in your region.",
            "safety": "Seek sturdy indoor shelter immediately. Avoid metallic objects, tall trees, and open water."
        })
    elif wmo_code in [65, 67, 82]:
        risk_score += 35
        reasons.append("Heavy downpour / violent rain showers")
        detected_conditions.append("Heavy Rain")
        emergency_alerts.append({
            "title": "FLOOD RISK & HEAVY RAIN WARNING",
            "warning": "Torrential rain increases flash flood risks and severely impairs road visibility.",
            "safety": "Avoid low-lying flood-prone roads. Do not drive through flooded underpasses."
        })
    elif wmo_code in [61, 63, 80, 81] or rain_prob >= 70:
        risk_score += 20
        reasons.append(f"Moderate rainfall expected (Rain probability: {rain_prob}%)")
        detected_conditions.append("Moderate Rain")

    # --- 3. Wind Speed & Gale Detection ---
    if wind_speed >= 65.0:
        risk_score += 40
        reasons.append(f"Severe gale wind speed ({wind_speed} km/h)")
        detected_conditions.append("Cyclone / Storm Wind")
        emergency_alerts.append({
            "title": "CYCLONIC WIND ALERT",
            "warning": "Destructive wind speeds can cause structural damage and fallen trees.",
            "safety": "Secure loose outdoor property and remain in safe interior rooms."
        })
    elif wind_speed >= 40.0:
        risk_score += 20
        reasons.append(f"Strong gusts of wind ({wind_speed} km/h)")
        detected_conditions.append("Strong Winds")

    # --- 4. Fog & Visibility Detection ---
    if wmo_code in [45, 48] or visibility < 500:
        risk_score += 25
        reasons.append(f"Dense fog restricting visibility ({visibility:.0f}m)")
        detected_conditions.append("Dense Fog")
        emergency_alerts.append({
            "title": "DENSE FOG ROAD SAFETY ALERT",
            "warning": "Severely reduced visibility creates hazardous driving conditions.",
            "safety": "Use low-beam headlights/fog lights, maintain long follow distances, and reduce speed."
        })

    # --- 5. UV Index Hazard ---
    if uv_index >= 10.0:
        risk_score += 15
        reasons.append(f"Very High UV Index ({uv_index})")
        detected_conditions.append("High UV Hazard")
    elif uv_index >= 7.0:
        risk_score += 10
        reasons.append(f"High UV radiation level ({uv_index})")

    # --- 6. Pleasant Weather Detection ---
    if risk_score == 0 and 18.0 <= temp <= 28.0 and wind_speed < 20.0 and rain_prob < 20 and humidity < 75:
        detected_conditions.append("Pleasant Weather")
        reasons.append("Comfortable temperature, calm winds, pleasant humidity, and low precipitation risk")

    # Ensure risk score is clamped between 0 and 100
    risk_score = min(max(risk_score, 0), 100)

    # Classify Risk Level
    if risk_score <= 25:
        risk_level = "LOW"
    elif risk_score <= 50:
        risk_level = "MEDIUM"
    elif risk_score <= 75:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    primary_reason = (
        "; ".join(reasons)
        if reasons
        else "Optimal weather conditions with negligible environmental hazards."
    )

    return RiskAnalysis(
        risk_score=risk_score,
        risk_level=risk_level,
        primary_reason=primary_reason,
        reasons=reasons,
        detected_conditions=detected_conditions,
        emergency_alerts=emergency_alerts
    )
