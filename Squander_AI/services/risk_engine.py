"""
Risk Analysis & Emergency Alert Engine
- Calculates Waste Risk Score (0–100) across 7 hazard dimensions
- Detects emergency conditions requiring immediate action
- Estimates pollution sources with confidence percentages
- Provides XAI reasoning for every risk decision
"""
import random
from typing import Dict, Any, List
from config import RISK_LEVELS


HAZARD_PROFILES: Dict[str, Dict[str, float]] = {
    # (toxicity, fire, air, water, soil, health, wildlife) – all 0.0–1.0
    "organic":      {"toxicity": 0.1, "fire": 0.1, "air": 0.2, "water": 0.3, "soil": 0.1, "health": 0.1, "wildlife": 0.1},
    "plastic":      {"toxicity": 0.5, "fire": 0.4, "air": 0.5, "water": 0.8, "soil": 0.7, "health": 0.4, "wildlife": 0.9},
    "paper":        {"toxicity": 0.1, "fire": 0.6, "air": 0.2, "water": 0.2, "soil": 0.2, "health": 0.1, "wildlife": 0.1},
    "glass":        {"toxicity": 0.1, "fire": 0.1, "air": 0.1, "water": 0.1, "soil": 0.2, "health": 0.2, "wildlife": 0.3},
    "metal":        {"toxicity": 0.3, "fire": 0.2, "air": 0.3, "water": 0.4, "soil": 0.5, "health": 0.3, "wildlife": 0.3},
    "ewaste":       {"toxicity": 0.9, "fire": 0.5, "air": 0.7, "water": 0.8, "soil": 0.9, "health": 0.9, "wildlife": 0.8},
    "hazardous":    {"toxicity": 0.95,"fire": 0.9, "air": 0.9, "water": 0.95,"soil": 0.95,"health": 0.95,"wildlife": 0.9},
    "biomedical":   {"toxicity": 0.9, "fire": 0.4, "air": 0.6, "water": 0.8, "soil": 0.7, "health": 0.99,"wildlife": 0.6},
    "construction": {"toxicity": 0.3, "fire": 0.2, "air": 0.5, "water": 0.3, "soil": 0.5, "health": 0.3, "wildlife": 0.2},
    "industrial":   {"toxicity": 0.7, "fire": 0.5, "air": 0.7, "water": 0.7, "soil": 0.8, "health": 0.7, "wildlife": 0.6},
    "agricultural": {"toxicity": 0.2, "fire": 0.3, "air": 0.3, "water": 0.4, "soil": 0.2, "health": 0.2, "wildlife": 0.2},
    "mixed":        {"toxicity": 0.4, "fire": 0.4, "air": 0.4, "water": 0.4, "soil": 0.4, "health": 0.4, "wildlife": 0.4},
}

EMERGENCY_RULES = [
    {
        "categories": ["hazardous", "biomedical"],
        "type": "Toxic Waste Detected",
        "severity": "CRITICAL",
        "message": "Toxic or biohazardous waste detected. Immediate containment and professional removal required.",
        "recommendation": "Do NOT handle without PPE. Contact hazardous waste disposal service immediately.",
    },
    {
        "categories": ["hazardous"],
        "keywords": ["battery", "gas cylinder", "aerosol"],
        "type": "Fire & Explosion Hazard",
        "severity": "CRITICAL",
        "message": "Flammable or explosive material detected. Risk of fire or explosion if improperly stored.",
        "recommendation": "Store in cool, dry, ventilated area. Contact fire safety authority.",
    },
    {
        "categories": ["biomedical"],
        "type": "Infection Control Alert",
        "severity": "HIGH",
        "message": "Biomedical waste poses disease transmission risk. Standard disposal bins must NOT be used.",
        "recommendation": "Use sealed biohazard containers. Call licensed biomedical waste collector.",
    },
    {
        "categories": ["ewaste"],
        "type": "E-Waste Heavy Metal Contamination Risk",
        "severity": "HIGH",
        "message": "E-waste contains lead, mercury, and cadmium. Improper disposal contaminates soil and groundwater.",
        "recommendation": "Drop at certified E-Waste center. Never burn or crush e-waste.",
    },
    {
        "categories": ["industrial"],
        "type": "Industrial Effluent Leachate Risk",
        "severity": "HIGH",
        "message": "Industrial waste may leach toxic chemicals into groundwater if landfilled without treatment.",
        "recommendation": "Engage licensed industrial waste contractor for proper chemical stabilization.",
    },
]

POLLUTION_SOURCES: Dict[str, Dict[str, int]] = {
    "plastic":      {"plastic_burning": 80, "open_dumping": 70, "river_disposal": 60, "landfill_gas": 20, "illegal_dumping": 55},
    "organic":      {"landfill_gas": 85, "open_dumping": 40, "river_disposal": 50, "illegal_dumping": 30},
    "ewaste":       {"illegal_dumping": 90, "open_dumping": 85, "river_disposal": 60, "landfill_gas": 40},
    "hazardous":    {"chemical_spill": 95, "industrial_waste": 90, "open_dumping": 85, "river_disposal": 80, "illegal_dumping": 90},
    "biomedical":   {"biomedical_waste": 99, "illegal_dumping": 85, "open_dumping": 80},
    "paper":        {"plastic_burning": 30, "open_dumping": 25, "landfill_gas": 20, "illegal_dumping": 20},
    "metal":        {"industrial_waste": 55, "landfill_gas": 10, "river_disposal": 30, "illegal_dumping": 40},
    "glass":        {"open_dumping": 30, "landfill_gas": 5,  "river_disposal": 20, "illegal_dumping": 25},
    "construction": {"open_dumping": 60, "illegal_dumping": 65, "river_disposal": 35, "landfill_gas": 10},
    "industrial":   {"industrial_waste": 90, "chemical_spill": 70, "river_disposal": 65, "landfill_gas": 50},
    "agricultural": {"open_dumping": 45, "river_disposal": 40, "landfill_gas": 30, "plastic_burning": 35},
    "mixed":        {"open_dumping": 50, "landfill_gas": 45, "illegal_dumping": 50, "river_disposal": 40},
}

POLLUTION_LABELS = {
    "plastic_burning":  "Plastic Burning",
    "open_dumping":     "Open Dumping",
    "illegal_dumping":  "Illegal Dumping",
    "river_disposal":   "River / Waterway Disposal",
    "industrial_waste": "Industrial Discharge",
    "construction_waste":"Construction Site Runoff",
    "biomedical_waste": "Biomedical Waste Leakage",
    "landfill_gas":     "Landfill Gas Emission",
    "chemical_spill":   "Chemical Spill",
}


class RiskEngine:

    def calculate_risk_score(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate composite Waste Risk Score 0–100 with XAI reasoning.
        """
        cat     = classification["category_key"]
        qty     = classification.get("quantity_kg", 1.0)
        profile = HAZARD_PROFILES.get(cat, HAZARD_PROFILES["mixed"])

        # Weighted risk score
        weights = {"toxicity": 0.25, "fire": 0.15, "air": 0.12,
                   "water": 0.15, "soil": 0.12, "health": 0.13, "wildlife": 0.08}
        weighted = sum(profile[k] * w * 100 for k, w in weights.items())

        # Quantity multiplier (non-linear)
        qty_factor = min(1.3, 1.0 + (qty - 1.0) * 0.03)
        risk_score = round(min(100.0, weighted * qty_factor), 1)

        # Risk level
        risk_level = "LOW"
        risk_color = "#22c55e"
        for threshold, level, color in RISK_LEVELS:
            if risk_score <= threshold:
                risk_level = level
                risk_color = color
                break

        # Dimension breakdown
        dimensions = {
            dim: {
                "score": round(val * 100, 1),
                "level": "HIGH" if val >= 0.7 else "MODERATE" if val >= 0.4 else "LOW"
            }
            for dim, val in profile.items()
        }

        xai_reason = (
            f"Risk Score of {risk_score}/100 ({risk_level}) is driven primarily by "
            f"{', '.join([d.replace('_', ' ').title() for d, v in profile.items() if v >= 0.7][:3]) or 'manageable hazard levels'}. "
            f"For {qty} kg of {classification['category_label']}, proper disposal to "
            f"{classification['disposal_recommendation']} is recommended to mitigate these risks."
        )

        return {
            "risk_score":        risk_score,
            "risk_level":        risk_level,
            "risk_color":        risk_color,
            "dimensions":        dimensions,
            "xai_reason":        xai_reason,
            "confidence":        min(99, classification["confidence"] + 2),
        }

    def detect_emergency_alerts(self, classification: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect emergency conditions and generate actionable alerts.
        """
        cat     = classification["category_key"]
        wt      = classification["input_waste_type"].lower()
        alerts  = []

        for rule in EMERGENCY_RULES:
            if cat in rule.get("categories", []):
                kws = rule.get("keywords", [])
                if kws and not any(k in wt for k in kws):
                    continue
                alerts.append({
                    "type":           rule["type"],
                    "severity":       rule["severity"],
                    "message":        rule["message"],
                    "recommendation": rule["recommendation"],
                })

        return alerts

    def detect_pollution_sources(self, classification: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Estimate likely pollution sources with confidence percentages.
        """
        cat     = classification["category_key"]
        sources = POLLUTION_SOURCES.get(cat, POLLUTION_SOURCES["mixed"])

        result = [
            {
                "source":      POLLUTION_LABELS.get(k, k.replace("_", " ").title()),
                "source_key":  k,
                "confidence":  v,
                "risk_level":  "HIGH" if v >= 70 else "MODERATE" if v >= 40 else "LOW",
            }
            for k, v in sources.items()
        ]
        result.sort(key=lambda x: x["confidence"], reverse=True)
        return result


risk_engine = RiskEngine()
