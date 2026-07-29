"""
Smart Outdoor Activity Analyzer Engine:
Evaluates suitability, risk levels, AI reasoning, and recommendations for 12 activities.
"""
from typing import Dict, Any, List

class ActivityEngine:

    def analyze_activities(self, current: Dict[str, Any]) -> List[Dict[str, Any]]:
        aqi = current.get("aqi", 0)
        pm2_5 = current.get("pm2_5", 0.0)
        pm10 = current.get("pm10", 0.0)
        uv = current.get("uv_index", 0.0)
        dust = current.get("dust", 0.0)

        activities = [
            {"name": "Walking", "strenuous": 2},
            {"name": "Running", "strenuous": 5},
            {"name": "Cycling", "strenuous": 4},
            {"name": "Cricket", "strenuous": 4},
            {"name": "Football", "strenuous": 5},
            {"name": "Hiking", "strenuous": 4},
            {"name": "Trekking", "strenuous": 5},
            {"name": "Camping", "strenuous": 2},
            {"name": "Picnic", "strenuous": 1},
            {"name": "Photography", "strenuous": 1},
            {"name": "Drone Flying", "strenuous": 1},
            {"name": "Morning Yoga", "strenuous": 2}
        ]

        results = []
        for act in activities:
            name = act["name"]
            strenuous = act["strenuous"]

            # Calculate base suitability score (100 is best)
            # High strenuous activities suffer more penalty from elevated PM2.5/AQI
            aqi_penalty = (aqi / 300.0) * 60 * (strenuous / 3.0)
            pm_penalty = (pm2_5 / 50.0) * 30 * (strenuous / 3.0)
            dust_penalty = (dust / 30.0) * 20 if name in ["Drone Flying", "Photography", "Cycling"] else 0
            uv_penalty = 15 if (uv > 8 and name in ["Hiking", "Trekking", "Camping", "Picnic"]) else 0

            score = max(0, min(100, round(100 - (aqi_penalty + pm_penalty + dust_penalty + uv_penalty), 1)))

            if score >= 85:
                risk = "Low"
                rec = "Highly Recommended! Clean air conditions ideal for outdoor performance."
                reason = "Pollutant metrics are well within safe thresholds."
            elif score >= 65:
                risk = "Moderate"
                rec = "Suitable with moderate precautions. Take hydrations breaks."
                reason = "Slightly elevated air pollutants; manageable for healthy individuals."
            elif score >= 40:
                risk = "High"
                rec = "Reduce activity duration or move to indoor venue."
                reason = f"High PM2.5 ({pm2_5} µg/m³) causes increased respiratory exertion."
            else:
                risk = "Critical"
                rec = "Not Recommended. Avoid completely due to air quality hazards."
                reason = f"Hazardous AQI ({aqi}) poses acute inhalation risks during physical effort."

            # Activity specific notes
            if name == "Drone Flying" and dust > 20:
                reason += " Fine dust particles reduce airborne rotor stability and optical clarity."
            if name == "Morning Yoga" and aqi > 100:
                reason += " Deep breathing exercises in polluted ambient air increase pulmonary toxin exposure."

            results.append({
                "activity": name,
                "suitability_score": score,
                "risk_level": risk,
                "ai_reasoning": reason,
                "recommendation": rec
            })

        # Sort by suitability score descending
        results.sort(key=lambda x: x["suitability_score"], reverse=True)
        return results

activity_engine = ActivityEngine()
