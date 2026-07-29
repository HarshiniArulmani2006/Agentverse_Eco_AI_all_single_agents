"""
Green Lifestyle Suggestions, Sustainability Index & Citizen Action Engine
"""
from typing import Dict, Any, List

class GreenEngine:

    def calculate_ai_scores(self, current: Dict[str, Any], risk_score: float) -> Dict[str, float]:
        aqi = current.get("aqi", 0)
        pm2_5 = current.get("pm2_5", 0.0)

        air_quality_score = max(0.0, round(100.0 - (aqi / 300.0 * 100.0), 1))
        health_safety_score = max(0.0, round(100.0 - (risk_score * 0.9), 1))
        environmental_score = max(0.0, round((air_quality_score * 0.6) + (health_safety_score * 0.4), 1))
        outdoor_activity_score = max(0.0, round(100.0 - (pm2_5 / 60.0 * 100.0), 1))
        sustainability_score = max(0.0, round((environmental_score * 0.7) + 30.0 * (1 - (aqi/500.0)), 1))

        return {
            "air_quality_score": air_quality_score,
            "health_safety_score": health_safety_score,
            "environmental_score": environmental_score,
            "outdoor_activity_score": outdoor_activity_score,
            "sustainability_score": sustainability_score
        }

    def generate_green_suggestions(self, current: Dict[str, Any]) -> List[Dict[str, str]]:
        return [
            {
                "title": "Use Electric Vehicles or Public Transit",
                "category": "Mobility",
                "impact": "Reduces urban NO2 and vehicular PM2.5 emissions by up to 40%."
            },
            {
                "title": "Car Pooling & Shared Rides",
                "category": "Mobility",
                "impact": "Decreases individual carbon footprint and cuts peak hour traffic congestion."
            },
            {
                "title": "Plant Native Urban Trees & Green Barriers",
                "category": "Ecology",
                "impact": "Trees act as natural bio-filters, trapping particulate dust and releasing oxygen."
            },
            {
                "title": "Eliminate Open Waste & Biomass Burning",
                "category": "Waste Management",
                "impact": "Prevents toxic dioxins and black carbon smoke from polluting local air."
            },
            {
                "title": "Adopt Renewable Solar Energy",
                "category": "Energy",
                "impact": "Lowers reliance on fossil-fuel thermal power generation during peak demand hours."
            },
            {
                "title": "Promote Green Roofs and Balcony Gardens",
                "category": "Urban Planning",
                "impact": "Cools urban micro-climates and absorbs atmospheric carbon."
            }
        ]

    def generate_citizen_checklist(self) -> List[Dict[str, Any]]:
        return [
            {"task": "Check local AQI before morning workouts", "icon": "check-circle", "status": "Recommended"},
            {"task": "Keep vehicle tire pressure optimal to reduce dust & emissions", "icon": "truck", "status": "Easy Action"},
            {"task": "Replace home HVAC/Air Purifier filters every 3 months", "icon": "wind", "status": "Home Maintenance"},
            {"task": "Report illegal garbage or crop burning to local environmental authorities", "icon": "alert-triangle", "status": "Community Action"},
            {"task": "Water garden and balcony plants during early evening to trap dust", "icon": "sun", "status": "Daily Habit"}
        ]

    def generate_eco_challenges(self) -> List[Dict[str, str]]:
        return [
            {"title": "Zero-Emission Commute Challenge", "period": "7 Days", "reward": "Green Champion Badge", "desc": "Walk, cycle, or take electric transit for 7 consecutive days."},
            {"title": "Indoor Air Oasis Challenge", "period": "3 Days", "reward": "Clean Air Pioneer", "desc": "Add 3 air-purifying plants (Snake Plant, Areca Palm, Peace Lily) to your living room."},
            {"title": "No Open Burning Pledge", "period": "Monthly", "reward": "Eco Sentinel", "desc": "Compost kitchen waste and pledge against open yard burning."}
        ]

    def estimate_carbon_footprint(self, aqi: float, city_name: str) -> Dict[str, Any]:
        # Rough carbon metric estimation from atmospheric soot & AQI density
        co2_equivalent_kg_per_capita = round(12.5 + (aqi * 0.08), 2)
        return {
            "city": city_name,
            "estimated_daily_co2_kg_per_capita": co2_equivalent_kg_per_capita,
            "severity_classification": "High Carbon Intensity" if aqi > 120 else "Moderate Carbon Intensity" if aqi > 60 else "Low Carbon Footprint"
        }

green_engine = GreenEngine()
