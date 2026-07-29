"""
AI Analysis Engine for Air Quality:
- Pollution pattern detection with confidence probabilities
- Source estimation
- WHO standards compliance checking
- Environmental intelligence assessment
- Emergency alert detection
- AI Risk Score calculation
"""
from typing import Dict, Any, List
from config import WHO_GUIDELINES

class AnalysisEngine:

    def calculate_risk_score(self, current: Dict[str, Any]) -> Dict[str, Any]:
        aqi = current.get("aqi", 0)
        pm2_5 = current.get("pm2_5", 0.0)
        pm10 = current.get("pm10", 0.0)
        no2 = current.get("no2", 0.0)

        # Base score derived from US AQI (normalized to 0-100 scale)
        base_score = min(100, (aqi / 300.0) * 100)
        
        # Pollutant multiplier bonuses for severe WHO breaches
        who_pm25_ratio = pm2_5 / WHO_GUIDELINES["pm2_5"]["safe"]
        who_pm10_ratio = pm10 / WHO_GUIDELINES["pm10"]["safe"]
        
        weighted_score = min(100.0, round((base_score * 0.6) + (min(who_pm25_ratio, 5.0) * 8.0) + (min(who_pm10_ratio, 5.0) * 4.0) + (min(no2 / 25.0, 4.0) * 4.0), 1))

        if weighted_score <= 15:
            level = "Excellent"
            reason = "Air quality is clean and clear. All pollutants are within WHO safe daily thresholds."
        elif weighted_score <= 35:
            level = "Good"
            reason = "Air quality is acceptable with low environmental health risks."
        elif weighted_score <= 50:
            level = "Moderate"
            reason = "Moderate pollution level. Sensitive individuals may experience mild discomfort."
        elif weighted_score <= 68:
            level = "Poor"
            reason = "Particulate matter and chemical concentrations exceed WHO recommended safety levels."
        elif weighted_score <= 82:
            level = "Unhealthy"
            reason = "Significant pollution detected. High fine particulate matter (PM2.5) concentrations."
        elif weighted_score <= 92:
            level = "Hazardous"
            reason = "Severe pollution hazard. Continuous exposure poses critical health risks to all age groups."
        else:
            level = "Emergency"
            reason = "Toxic pollution emergency level. Urgent environmental health advisories active."

        return {
            "score": weighted_score,
            "level": level,
            "reason": reason
        }

    def detect_pollution_patterns(self, current: Dict[str, Any]) -> Dict[str, Any]:
        pm2_5 = current.get("pm2_5", 0.0)
        pm10 = current.get("pm10", 0.0)
        no2 = current.get("no2", 0.0)
        so2 = current.get("so2", 0.0)
        co = current.get("co", 0.0)
        dust = current.get("dust", 0.0)
        aod = current.get("aod", 0.0)

        pm_ratio = pm2_5 / (pm10 + 0.1)

        # Industrial Pollution: elevated SO2, NO2, high fine PM
        industrial_prob = min(99, int((so2 / 20.0 * 45) + (no2 / 30.0 * 35) + (pm2_5 / 35.0 * 20)))
        
        # Traffic Pollution: elevated NO2, CO, PM2.5
        traffic_prob = min(99, int((no2 / 25.0 * 50) + (co / 400.0 * 30) + (pm_ratio * 20)))

        # Smog: high AOD, high PM2.5, elevated NO2
        smog_prob = min(99, int((aod / 0.5 * 40) + (pm2_5 / 45.0 * 40) + (no2 / 35.0 * 20)))

        # Dust Storm: very high PM10, coarse dust, low PM2.5/PM10 ratio
        dust_storm_prob = min(99, int((dust / 15.0 * 50) + ((1 - min(pm_ratio, 1.0)) * 30) + (pm10 / 80.0 * 20)))

        # Wildfire Smoke: very high PM2.5, elevated CO, high AOD
        wildfire_prob = min(99, int((pm2_5 / 50.0 * 50) + (co / 500.0 * 30) + (aod / 0.6 * 20)))

        # Construction Dust: high PM10 with moderate PM2.5 and low SO2
        construction_prob = min(99, int((pm10 / 60.0 * 60) + ((1 - min(pm_ratio, 0.8)) * 30) + 10))

        # Overall condition tag
        dominant_pattern = max(
            [
                ("Industrial Pollution", industrial_prob),
                ("Traffic Pollution", traffic_prob),
                ("Smog", smog_prob),
                ("Dust Storm", dust_storm_prob),
                ("Wildfire Smoke", wildfire_prob),
                ("Construction Dust", construction_prob)
            ],
            key=lambda x: x[1]
        )

        return {
            "dominant_pattern": dominant_pattern[0] if dominant_pattern[1] > 40 else "Clean / Diffuse Air",
            "probabilities": {
                "industrial_pollution": industrial_prob,
                "traffic_pollution": traffic_prob,
                "smog": smog_prob,
                "dust_storm": dust_storm_prob,
                "wildfire_smoke": wildfire_prob,
                "construction_dust": construction_prob
            }
        }

    def estimate_pollution_sources(self, current: Dict[str, Any]) -> List[Dict[str, Any]]:
        patterns = self.detect_pollution_patterns(current)["probabilities"]
        
        sources = [
            {"source": "Vehicle Emissions", "confidence": patterns["traffic_pollution"], "category": "Mobile"},
            {"source": "Industrial Facilities", "confidence": patterns["industrial_pollution"], "category": "Point Source"},
            {"source": "Construction & Road Dust", "confidence": patterns["construction_dust"], "category": "Fugitive Dust"},
            {"source": "Garbage & Biomass Burning", "confidence": min(99, int(patterns["wildfire_smoke"] * 0.8 + patterns["smog"] * 0.2)), "category": "Open Burning"},
            {"source": "Crop Stubble Burning", "confidence": min(99, int(patterns["wildfire_smoke"] * 0.75 + patterns["industrial_pollution"] * 0.25)), "category": "Agricultural"},
            {"source": "Forest Fires / Brush Smoke", "confidence": patterns["wildfire_smoke"], "category": "Natural Fire"},
            {"source": "Thermal Power Plants", "confidence": min(99, int(patterns["industrial_pollution"] * 0.85 + 10)), "category": "Energy Generation"},
            {"source": "Sand & Regional Dust", "confidence": patterns["dust_storm"], "category": "Meteorological"}
        ]
        
        # Sort by confidence descending
        sources.sort(key=lambda x: x["confidence"], reverse=True)
        return sources

    def evaluate_who_compliance(self, current: Dict[str, Any]) -> Dict[str, Any]:
        compliance = {}
        for pollutant, info in WHO_GUIDELINES.items():
            val = current.get(pollutant, 0.0)
            if pollutant == "carbon_monoxide" and val > 100:
                # convert µg/m³ to mg/m³ for CO
                val = round(val / 1000.0, 2)

            safe = info["safe"]
            critical = info["critical"]

            if val <= safe:
                status = "Safe"
                class_color = "success"
                desc = f"{val} {info['unit']} is within WHO safe guideline ({safe} {info['unit']})."
            elif val <= critical:
                status = "Above WHO Limit"
                class_color = "warning"
                multiple = round(val / safe, 1)
                desc = f"Exceeds WHO limit by {multiple}x. Moderate exposure concern."
            elif val <= critical * 1.8:
                status = "Critical"
                class_color = "orange"
                multiple = round(val / safe, 1)
                desc = f"Critical levels! Exceeds WHO safe threshold by {multiple}x."
            else:
                status = "Dangerous"
                class_color = "danger"
                multiple = round(val / safe, 1)
                desc = f"Dangerous toxicity! {multiple}x above WHO limit. Acute health threat."

            compliance[pollutant] = {
                "value": val,
                "unit": info["unit"],
                "safe_limit": safe,
                "status": status,
                "color_class": class_color,
                "description": desc
            }
        return compliance

    def generate_environmental_intelligence(self, current: Dict[str, Any]) -> Dict[str, Any]:
        aqi = current.get("aqi", 0)
        pm2_5 = current.get("pm2_5", 0.0)
        dust = current.get("dust", 0.0)
        so2 = current.get("so2", 0.0)
        no2 = current.get("no2", 0.0)
        uv = current.get("uv_index", 0.0)

        return {
            "human_health": "Respiratory irritation risk elevated due to particulate inhalation." if aqi > 100 else "Minimal immediate health risk from air pollutants.",
            "agriculture": "Acid deposition risk increases with elevated SO2/NO2 levels, impairing crop yields." if (so2 > 30 or no2 > 35) else "Current atmospheric chemistry is safe for crop vegetation.",
            "wildlife": "Sensitive avian and mammalian species experience reduced respiratory capacity in polluted air." if aqi > 120 else "Wildlife ecosystems operating under baseline atmospheric conditions.",
            "water_bodies": "Atmospheric fallout of heavy particulates can lead to surface water acidification." if pm2_5 > 40 else "Low particulate deposition risk to freshwater systems.",
            "solar_energy": f"Solar panel photovoltaic efficiency reduced by ~{min(35, int(pm2_5 * 0.4 + dust * 0.8))}% due to particulate atmospheric scattering." if (pm2_5 > 25 or dust > 10) else "Optimal solar irradiance and panel efficiency.",
            "wind_energy": "Aerosol optical density slightly alters micro-boundary wind currents." if dust > 20 else "Normal wind turbine aerodynamics and generation capacity.",
            "climate_change": "High black carbon and aerosol fraction contributes to radiative atmospheric warming." if pm2_5 > 35 else "Particulate radiative forcing is currently minimal.",
            "urban_ecosystems": "Urban heat island effect intensified by trapped thermal particulate layers." if aqi > 140 else "Urban air flow and thermal exchange within normal parameters.",
            "electricity_demand": "Increased HVAC and indoor air purification energy consumption expected." if aqi > 110 else "Baseline grid energy demand for ventilation.",
            "wildfire_risk": "Dry aerosol haze and low humidity exacerbate localized vegetation combustibility." if (uv > 6 and aqi > 100) else "Low environmental fire ignition indicator from air quality metrics."
        }

    def detect_emergency_alerts(self, current: Dict[str, Any]) -> List[Dict[str, Any]]:
        alerts = []
        aqi = current.get("aqi", 0)
        pm2_5 = current.get("pm2_5", 0.0)
        pm10 = current.get("pm10", 0.0)
        dust = current.get("dust", 0.0)
        co = current.get("co", 0.0)

        if aqi >= 250:
            alerts.append({
                "type": "Hazardous AQI Emergency",
                "severity": "CRITICAL",
                "message": f"Hazardous Air Quality Index ({aqi}) recorded! Severe risk to whole population.",
                "recommendation": "Avoid all outdoor exertion. Keep air purifiers running on max setting."
            })
        if pm2_5 >= 100:
            alerts.append({
                "type": "Extreme Fine Particulate Spike (PM2.5)",
                "severity": "HIGH",
                "message": f"PM2.5 level reached {pm2_5} µg/m³ (over 6x WHO limits).",
                "recommendation": "Wear fit-tested N95 or KN95 respirators outdoors."
            })
        if dust >= 40 or pm10 >= 200:
            alerts.append({
                "type": "Dust Storm / Coarse Dust Alert",
                "severity": "HIGH",
                "message": f"Heavy dust concentration ({dust} µg/m³) impairing visibility and air purity.",
                "recommendation": "Close all building windows and doors tightly. Avoid driving in low visibility."
            })
        if co >= 5000:
            alerts.append({
                "type": "Toxic Carbon Monoxide Warning",
                "severity": "CRITICAL",
                "message": "Elevated CO gas level detected near urban surface.",
                "recommendation": "Ventilate away from heavy traffic or combustion source zones."
            })

        return alerts

analysis_engine = AnalysisEngine()
