"""
Conversational AI Query Engine for Air Quality Questions
"""
from typing import Dict, Any

class ConversationalEngine:

    def answer_query(self, query: str, air_data: Dict[str, Any], health_data: Dict[str, Any], activity_data: list) -> Dict[str, Any]:
        q = query.lower().strip()
        current = air_data.get("current", {})
        aqi = current.get("aqi", 0)
        pm2_5 = current.get("pm2_5", 0.0)
        pm10 = current.get("pm10", 0.0)
        no2 = current.get("no2", 0.0)

        # Categorize query
        if "mask" in q or "n95" in q:
            if pm2_5 > 35 or aqi > 100:
                answer = f"Yes, wearing an N95 or KN95 mask is strongly recommended today. Fine particulate matter (PM2.5) is at {pm2_5} µg/m³, which exceeds WHO safety limits."
            else:
                answer = f"No mask is necessary for general outdoor exposure today. Current AQI is {aqi} (PM2.5: {pm2_5} µg/m³), which is in the safe range."
            intent = "mask_inquiry"

        elif "jog" in q or "run" in q or "exercise" in q or "workout" in q:
            running_info = next((a for a in activity_data if a["activity"] == "Running"), None)
            if running_info and running_info["suitability_score"] >= 65:
                answer = f"Yes, jogging is suitable today! Suitability Score: {running_info['suitability_score']}/100. {running_info['ai_reasoning']}"
            else:
                score = running_info["suitability_score"] if running_info else "Low"
                answer = f"Outdoor jogging is not recommended today (Suitability Score: {score}/100). Heavy breathing increases particulate inhalation. Consider indoor treadmill workouts."
            intent = "exercise_inquiry"

        elif "child" in q or "kids" in q or "play" in q:
            child_info = health_data.get("children", {})
            risk = child_info.get("risk_level", "Moderate")
            rec = child_info.get("recommendation", "")
            answer = f"Child Health Risk Level: {risk}. {rec}"
            intent = "children_inquiry"

        elif "window" in q or "open" in q or "ventilat" in q:
            if aqi <= 60:
                answer = f"Yes! Air quality is good (AQI: {aqi}). Opening windows will bring fresh air and improve indoor ventilation."
            else:
                answer = f"Keep windows closed today. AQI is {aqi} and outdoor particulate matter could enter and compromise indoor air quality. Use an air purifier instead."
            intent = "window_inquiry"

        elif "pollutant" in q or "highest" in q or "worst" in q or "cause" in q:
            pollutants = [("PM2.5", pm2_5 / 15.0), ("PM10", pm10 / 45.0), ("NO2", no2 / 25.0)]
            pollutants.sort(key=lambda x: x[1], reverse=True)
            top_pollutant = pollutants[0]
            answer = f"The primary pollutant causing concern today is {top_pollutant[0]}, which is currently at {round(top_pollutant[1], 1)}x the WHO safe threshold."
            intent = "pollutant_inquiry"

        elif "travel" in q or "drive" in q or "trip" in q:
            if aqi > 150 or current.get("dust", 0) > 30:
                answer = f"Travel with caution today. Reduced visibility and high particulate pollution detected. Recirculate cabin air inside vehicles."
            else:
                answer = f"Safe for travel today! Roads have clear visibility and atmospheric pollutants are low."
            intent = "travel_inquiry"

        elif "safe" in q or "clean" in q or "good" in q:
            if aqi <= 50:
                answer = f"Yes, today's air quality is excellent and completely safe (AQI: {aqi}). All pollutants meet clean air standards."
            elif aqi <= 100:
                answer = f"Today's air quality is moderate (AQI: {aqi}). Safe for most people, but sensitive individuals should monitor symptoms."
            else:
                answer = f"No, today's air quality is unhealthful (AQI: {aqi}). Precautionary health measures should be taken."
            intent = "safety_inquiry"

        elif "worse" in q or "yesterday" in q or "trend" in q:
            answer = f"Current AQI is {aqi}. Peak pollution hours generally occur during morning/evening commute times. Check the forecast panel for hour-by-hour trends."
            intent = "trend_inquiry"

        else:
            answer = f"Currently in {air_data.get('location', 'your area')}, the AQI is {aqi} (PM2.5: {pm2_5} µg/m³). Primary advice: {health_data.get('asthma_patients', {}).get('recommendation', 'Maintain clean air practices.')}"
            intent = "general_inquiry"

        return {
            "query": query,
            "intent": intent,
            "answer": answer,
            "voice_assistant_response": answer
        }

conversational_engine = ConversationalEngine()
