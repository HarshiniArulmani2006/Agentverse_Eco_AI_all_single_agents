"""
AI Health Risk Prediction & Demographic Health Advisory Engine
"""
from typing import Dict, Any, List
from config import WHO_GUIDELINES

class HealthEngine:

    def predict_demographic_risks(self, current: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        pm2_5 = current.get("pm2_5", 0.0)
        pm10 = current.get("pm10", 0.0)
        no2 = current.get("no2", 0.0)
        o3 = current.get("o3", 0.0)
        aqi = current.get("aqi", 0)

        pm25_who_ratio = round(pm2_5 / WHO_GUIDELINES["pm2_5"]["safe"], 1)
        no2_who_ratio = round(no2 / WHO_GUIDELINES["nitrogen_dioxide"]["safe"], 1)

        # Children
        if aqi > 180 or pm25_who_ratio >= 4.0:
            child_risk = "Very High"
            child_reason = f"PM2.5 ({pm2_5} µg/m³) exceeds WHO limits by {pm25_who_ratio}x. Developing lungs are highly susceptible."
            child_rec = "Keep children indoors. Avoid outdoor school breaks and playground activities."
        elif aqi > 100 or pm25_who_ratio >= 2.0:
            child_risk = "High"
            child_reason = f"Fine particulate matter is {pm25_who_ratio}x above safe limit."
            child_rec = "Limit outdoor strenuous play to early morning or indoor facilities."
        elif aqi > 50:
            child_risk = "Moderate"
            child_reason = "Air quality is acceptable but mild irritation can occur during long outdoor play."
            child_rec = "Normal activities safe; keep hydrated."
        else:
            child_risk = "Low"
            child_reason = "Air quality is clean and safe for children."
            child_rec = "Safe for all outdoor activities and sports."

        # Elderly
        if aqi > 160 or pm25_who_ratio >= 3.5:
            elderly_risk = "Very High"
            elderly_reason = f"High PM2.5 & NO2 increase cardiovascular stress and systemic inflammation."
            elderly_rec = "Remain indoors with air purification. Avoid morning walks until AQI improves."
        elif aqi > 100:
            elderly_risk = "High"
            elderly_reason = "Particulate pollution can aggravate pre-existing vascular or pulmonary conditions."
            elderly_rec = "Wear N95 mask if outdoors is required; keep emergency medicine accessible."
        elif aqi > 50:
            elderly_risk = "Moderate"
            elderly_reason = "Slightly elevated pollutants; monitor for coughing or shortness of breath."
            elderly_rec = "Gentle walks in parks with dense foliage recommended."
        else:
            elderly_risk = "Low"
            elderly_reason = "Air purity optimal for senior wellness."
            elderly_rec = "Safe for morning walks and outdoor relaxation."

        # Pregnant Women
        if pm25_who_ratio >= 3.0 or aqi > 150:
            preg_risk = "Very High"
            preg_reason = f"PM2.5 ({pm2_5} µg/m³) translocates to placenta, posing fetal stress risks."
            preg_rec = "Minimize outdoor exposure. Use indoor HEPA air purifiers."
        elif aqi > 90:
            preg_risk = "High"
            preg_reason = f"Air pollution levels exceed safe prenatal exposure targets."
            preg_rec = "Wear protective mask outdoors; stay well hydrated."
        else:
            preg_risk = "Low to Moderate"
            preg_reason = "Pollutants are within manageable baseline thresholds."
            preg_rec = "Safe to venture outdoors; maintain good indoor ventilation."

        # Asthma Patients
        if pm25_who_ratio >= 3.0 or no2_who_ratio >= 2.0 or o3 > 120:
            asthma_risk = "Severe / Very High"
            asthma_reason = f"PM2.5 is {pm25_who_ratio}x WHO limit and NO2 is {no2_who_ratio}x limit, triggering airway constriction."
            asthma_rec = "Strictly remain indoors. Keep rescue inhaler close at all times."
        elif aqi > 100:
            asthma_risk = "High"
            asthma_reason = "Airway irritants elevated. Potential for asthma flare-ups."
            asthma_rec = "Use preventive inhalers as prescribed; wear N95 mask outdoors."
        else:
            asthma_risk = "Low"
            asthma_reason = "Low concentration of bronchoconstrictive pollutants."
            asthma_rec = "Safe for normal outdoors; carry inhaler as standard practice."

        # COPD Patients
        if aqi > 140 or pm25_who_ratio >= 3.0:
            copd_risk = "Very High"
            copd_reason = "High particulate load causes acute alveolar irritation and dyspnea."
            copd_rec = "Avoid all outdoor exposure. Run air purifier continuously."
        elif aqi > 80:
            copd_risk = "High"
            copd_reason = "Moderate to high particulate levels can induce chronic airway inflammation."
            copd_rec = "Limit outdoor physical effort; rest indoors in filtered air."
        else:
            copd_risk = "Low"
            copd_reason = "Ambient air is clean for COPD management."
            copd_rec = "Safe for mild outdoor activity."

        # Heart Patients
        if aqi > 150 or pm25_who_ratio >= 3.5:
            heart_risk = "Very High"
            heart_reason = "Fine particulates cross lung-blood barrier, increasing arterial pressure and heart rate."
            heart_rec = "Avoid physical exertion outdoors. Keep indoor environment dust-free."
        elif aqi > 100:
            heart_risk = "High"
            heart_reason = "Elevated particulate pollution linked to blood vessel constriction."
            heart_rec = "Reduce intense activities; seek medical help if experiencing chest tightness."
        else:
            heart_risk = "Low"
            heart_reason = "Air quality does not pose significant hemodynamic strain."
            heart_rec = "Safe for normal routine."

        # Outdoor Workers
        if aqi > 150 or pm10 > 100:
            worker_risk = "High / Dangerous"
            worker_reason = "Prolonged high volume respiration of polluted air during physical work."
            worker_rec = "Mandatory N95/KN95 respirator usage. Take 15-min indoor breaks every hour."
        elif aqi > 100:
            worker_risk = "Moderate to High"
            worker_reason = "Continuous exposure over 8-hour shift leads to cumulative pollutant intake."
            worker_rec = "Wear dust mask; drink plenty of water to flush toxins."
        else:
            worker_risk = "Low"
            worker_reason = "Workplace ambient air quality is clear."
            worker_rec = "Safe for standard outdoor labor."

        # Athletes
        if aqi > 130 or pm2_5 > 40:
            athlete_risk = "High"
            athlete_reason = "Heavy breathing during intense exercise drastically increases deep lung toxin deposition."
            athlete_rec = "Shift cardio training, running, and heavy workouts indoors."
        elif aqi > 80:
            athlete_risk = "Moderate"
            athlete_reason = "Sub-optimal air purity can lower VO2 max and cause throat dryness."
            athlete_rec = "Reduce training intensity or choose early morning hours."
        else:
            athlete_risk = "Low"
            athlete_reason = "Ideal clean air conditions for peak athletic performance."
            athlete_rec = "Great conditions for outdoor training, running, and sports."

        return {
            "children": {"risk_level": child_risk, "reason": child_reason, "recommendation": child_rec},
            "elderly": {"risk_level": elderly_risk, "reason": elderly_reason, "recommendation": elderly_rec},
            "pregnant_women": {"risk_level": preg_risk, "reason": preg_reason, "recommendation": preg_rec},
            "asthma_patients": {"risk_level": asthma_risk, "reason": asthma_reason, "recommendation": asthma_rec},
            "copd_patients": {"risk_level": copd_risk, "reason": copd_reason, "recommendation": copd_rec},
            "heart_patients": {"risk_level": heart_risk, "reason": heart_reason, "recommendation": heart_rec},
            "outdoor_workers": {"risk_level": worker_risk, "reason": worker_reason, "recommendation": worker_rec},
            "athletes": {"risk_level": athlete_risk, "reason": athlete_reason, "recommendation": athlete_rec}
        }

    def generate_personalized_recommendations(self, current: Dict[str, Any], risk_score: float) -> Dict[str, List[str]]:
        aqi = current.get("aqi", 0)
        pm2_5 = current.get("pm2_5", 0.0)
        dust = current.get("dust", 0.0)

        health_advice = []
        travel_advice = []
        lifestyle_advice = []

        # Health Advice
        if pm2_5 > 35 or aqi > 100:
            health_advice.append("Wear fit-tested N95 or KN95 mask when stepping outdoors.")
            health_advice.append("Use an indoor air purifier equipped with HEPA filter.")
            health_advice.append("Drink plenty of water to help clear respiratory mucosa.")
        else:
            health_advice.append("Air quality is healthy; no protective masks required for general public.")
            health_advice.append("Enjoy fresh ambient air; maintain normal hydration.")

        if dust > 25:
            health_advice.append("Wear protective goggles or anti-dust eyewear to prevent eye irritation.")

        if risk_score > 70:
            health_advice.append("Close all windows and doors to seal against external toxic air.")
            health_advice.append("Avoid all outdoor physical exertion.")

        # Travel Advice
        if dust > 30 or pm2_5 > 80:
            travel_advice.append("Low Visibility Alert: Heavy atmospheric haze or dust reduces road visibility.")
            travel_advice.append("Drive carefully with low-beam fog headlights on.")
            travel_advice.append("Heavy traffic expected due to reduced vehicle speeds.")
        elif aqi > 120:
            travel_advice.append("Moderate travel caution: Recirculate cabin air inside vehicles.")
            travel_advice.append("Avoid long open-air trips on two-wheelers or open vehicles.")
        else:
            travel_advice.append("Safe for travel: Clear roads and high atmospheric visibility.")
            travel_advice.append("Ideal conditions for road trips, cycling, and commuting.")

        # Lifestyle Advice
        if aqi <= 50:
            lifestyle_advice.append("Safe to open windows and let fresh air circulate inside rooms.")
            lifestyle_advice.append("Safe for morning walks, outdoor jogging, and yoga.")
            lifestyle_advice.append("Great day for outdoor sports, picnics, and cycling.")
        elif aqi <= 100:
            lifestyle_advice.append("Windows can be opened briefly during early afternoon when AQI dips.")
            lifestyle_advice.append("Morning walks safe in green parks with low vehicle traffic.")
            lifestyle_advice.append("Light cycling and walking acceptable.")
        else:
            lifestyle_advice.append("Keep windows closed to prevent indoor particulate accumulation.")
            lifestyle_advice.append("Avoid outdoor sports; switch to indoor fitness or treadmill.")
            lifestyle_advice.append("Postpone outdoor picnics, hiking, and long outdoor events.")

        return {
            "health_advice": health_advice,
            "travel_advice": travel_advice,
            "lifestyle_advice": lifestyle_advice
        }

health_engine = HealthEngine()
