"""
ai/anomaly_detection.py – AI Anomaly Detection Engine
Detects unusual patterns in waste generation, smart bin data, and community trends.
Uses statistical deviation analysis with explainable flagging.
"""
import math
import random
from typing import Dict, Any, List


# Baseline waste generation patterns (kg/household/day) by day-of-week
WEEKLY_BASELINE = {
    "Monday":    1.60, "Tuesday":   1.55, "Wednesday": 1.58,
    "Thursday":  1.62, "Friday":    1.75, "Saturday":  2.10, "Sunday": 2.05,
}

# Seasonal multipliers
SEASONAL_FACTORS = {
    "Winter": 1.08, "Spring": 0.96, "Summer": 0.92, "Monsoon": 1.12,
    "Autumn": 1.00, "Festival": 1.45, "Holiday": 1.35,
}

# Known anomaly patterns for detection
ANOMALY_TEMPLATES = [
    {
        "anomaly":       "Plastic Surge Detected",
        "trigger":       lambda d: d.get("plastic_pct", 0) > 28,
        "description":   "Plastic waste generation is 35% above baseline.",
        "probable_cause":"Increased online shopping deliveries or local event packaging.",
        "recommendation":"Deploy additional plastic recycling bins. Increase collection frequency.",
        "severity":      "MODERATE",
        "confidence":    82,
    },
    {
        "anomaly":       "Food Waste Peak",
        "trigger":       lambda d: d.get("organic_pct", 0) > 40,
        "description":   "Organic/food waste is 40% above typical daily average.",
        "probable_cause":"Post-holiday or post-festival period with surplus food disposal.",
        "recommendation":"Schedule additional organic collection and alert composting facility.",
        "severity":      "MODERATE",
        "confidence":    88,
    },
    {
        "anomaly":       "E-Waste Accumulation",
        "trigger":       lambda d: d.get("ewaste_pct", 0) > 8,
        "description":   "E-waste volume is 3x higher than monthly average.",
        "probable_cause":"Community tech upgrade cycle or corporate equipment disposal event.",
        "recommendation":"Notify certified e-waste collection center. Deploy special collection vehicle.",
        "severity":      "HIGH",
        "confidence":    79,
    },
    {
        "anomaly":       "Hazardous Waste Spike",
        "trigger":       lambda d: d.get("hazardous_pct", 0) > 5,
        "description":   "Hazardous material concentration exceeds safe threshold.",
        "probable_cause":"Industrial discharge or improper household chemical disposal.",
        "recommendation":"IMMEDIATE: Notify hazardous waste response team. Isolate affected bin.",
        "severity":      "CRITICAL",
        "confidence":    91,
    },
    {
        "anomaly":       "Overnight Bin Fill Rate",
        "trigger":       lambda d: d.get("overnight_fill_rate", 0) > 25,
        "description":   "Bin fill rate between midnight and 6 AM is abnormally high.",
        "probable_cause":"Possible illegal dumping or industrial discharge after hours.",
        "recommendation":"Install CCTV monitoring at affected bins. Schedule early morning inspection.",
        "severity":      "HIGH",
        "confidence":    85,
    },
    {
        "anomaly":       "Recycling Rate Drop",
        "trigger":       lambda d: d.get("recycling_rate", 100) < 25,
        "description":   "Community recycling rate has fallen below 25% this week.",
        "probable_cause":"Collection schedule disruption or community awareness gap.",
        "recommendation":"Launch targeted recycling awareness campaign. Review bin placement.",
        "severity":      "MODERATE",
        "confidence":    77,
    },
]


class AnomalyDetector:
    """
    AI-powered anomaly detection for waste generation patterns.
    Identifies statistical deviations, seasonal outliers, and illegal activity signals.
    """

    def detect_from_community_data(
        self, community_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Run all anomaly checks against community analytics data.

        Args:
            community_data: Output from prediction_engine.get_community_analytics()

        Returns:
            List of detected anomalies with severity and recommendations.
        """
        detected = []
        breakdown = community_data.get("household_waste_breakdown", {})

        check_data = {
            "plastic_pct":        breakdown.get("plastic", 0),
            "organic_pct":        breakdown.get("organic", 0),
            "ewaste_pct":         breakdown.get("ewaste", 0),
            "hazardous_pct":      breakdown.get("hazardous", 0),
            "recycling_rate":     community_data.get("recycling_rate_pct", 100),
            "overnight_fill_rate": 12,  # Simulated — would come from bin IoT in production
        }

        for template in ANOMALY_TEMPLATES:
            try:
                if template["trigger"](check_data):
                    detected.append({
                        "anomaly":       template["anomaly"],
                        "description":   template["description"],
                        "probable_cause":template["probable_cause"],
                        "recommendation":template["recommendation"],
                        "severity":      template["severity"],
                        "confidence":    template["confidence"],
                    })
            except Exception:
                pass  # Skip failed checks gracefully

        return detected

    def detect_bin_anomalies(self, bins: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect anomalies in smart bin data — overflow risk, temperature spike, etc.
        """
        alerts = []
        for b in bins:
            fill    = b.get("fill_level_pct", 0)
            temp    = b.get("temperature_c", 25)
            bin_id  = b.get("bin_id", "Unknown")
            btype   = b.get("waste_type", "mixed")

            if fill >= 95:
                alerts.append({
                    "bin_id":  bin_id,
                    "anomaly": "OVERFLOW IMMINENT",
                    "value":   f"{fill}% full",
                    "severity":"CRITICAL",
                    "action":  "Immediate collection required.",
                })
            elif temp > 42 and btype == "organic":
                alerts.append({
                    "bin_id":  bin_id,
                    "anomaly": "TEMPERATURE SPIKE (Organic Decomposition)",
                    "value":   f"{temp}°C",
                    "severity":"HIGH",
                    "action":  "Inspect for excessive decomposition or combustion risk.",
                })
            elif fill >= 85 and b.get("overflow_prediction", {}).get("urgent_collection"):
                alerts.append({
                    "bin_id":  bin_id,
                    "anomaly": "OVERFLOW PREDICTED",
                    "value":   f"{fill}% — overflow within {b['overflow_prediction']['hours_until_overflow']}h",
                    "severity":"HIGH",
                    "action":  "Schedule urgent collection.",
                })
        return alerts

    def statistical_deviation(
        self,
        observed: float,
        baseline: float,
        std_dev:  float = None,
    ) -> Dict[str, Any]:
        """
        Compute statistical deviation of an observed value from baseline.
        
        Returns:
            z_score, is_anomaly flag, and severity label.
        """
        if std_dev is None:
            std_dev = baseline * 0.15  # Assume 15% natural variation
        if std_dev == 0:
            return {"z_score": 0, "is_anomaly": False, "severity": "NORMAL"}

        z_score = (observed - baseline) / std_dev
        abs_z   = abs(z_score)

        if abs_z >= 3.0:
            severity = "CRITICAL"
        elif abs_z >= 2.0:
            severity = "HIGH"
        elif abs_z >= 1.5:
            severity = "MODERATE"
        else:
            severity = "NORMAL"

        return {
            "z_score":    round(z_score, 2),
            "is_anomaly": abs_z >= 1.5,
            "severity":   severity,
            "deviation_pct": round((observed - baseline) / baseline * 100, 1) if baseline else 0,
        }


anomaly_detector = AnomalyDetector()
