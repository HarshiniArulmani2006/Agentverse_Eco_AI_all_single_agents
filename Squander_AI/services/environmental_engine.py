"""
Environmental Impact & Carbon Footprint Engine
- Estimates environmental impact across 8 dimensions
- Calculates carbon footprint for all disposal methods
- Identifies the most sustainable disposal pathway
- Generates environmental impact score with XAI reasoning
"""
from typing import Dict, Any, List
from config import CARBON_FACTORS


IMPACT_WEIGHTS: Dict[str, Dict[str, float]] = {
    "organic":      {"air": 0.2, "water": 0.3, "soil": 0.1, "wildlife": 0.1, "marine": 0.2, "climate": 0.3, "health": 0.1, "biodiversity": 0.2},
    "plastic":      {"air": 0.4, "water": 0.8, "soil": 0.7, "wildlife": 0.9, "marine": 0.95,"climate": 0.6, "health": 0.5, "biodiversity": 0.8},
    "paper":        {"air": 0.2, "water": 0.3, "soil": 0.2, "wildlife": 0.1, "marine": 0.2, "climate": 0.3, "health": 0.1, "biodiversity": 0.1},
    "glass":        {"air": 0.1, "water": 0.1, "soil": 0.3, "wildlife": 0.2, "marine": 0.2, "climate": 0.1, "health": 0.1, "biodiversity": 0.1},
    "metal":        {"air": 0.3, "water": 0.4, "soil": 0.5, "wildlife": 0.3, "marine": 0.4, "climate": 0.4, "health": 0.3, "biodiversity": 0.3},
    "ewaste":       {"air": 0.7, "water": 0.8, "soil": 0.9, "wildlife": 0.8, "marine": 0.7, "climate": 0.7, "health": 0.9, "biodiversity": 0.8},
    "hazardous":    {"air": 0.9, "water": 0.95,"soil": 0.95,"wildlife": 0.9, "marine": 0.9, "climate": 0.8, "health": 0.95,"biodiversity": 0.9},
    "biomedical":   {"air": 0.7, "water": 0.8, "soil": 0.7, "wildlife": 0.6, "marine": 0.6, "climate": 0.5, "health": 0.99,"biodiversity": 0.6},
    "construction": {"air": 0.4, "water": 0.3, "soil": 0.5, "wildlife": 0.3, "marine": 0.2, "climate": 0.2, "health": 0.3, "biodiversity": 0.2},
    "industrial":   {"air": 0.7, "water": 0.7, "soil": 0.8, "wildlife": 0.7, "marine": 0.6, "climate": 0.6, "health": 0.7, "biodiversity": 0.6},
    "agricultural": {"air": 0.3, "water": 0.4, "soil": 0.3, "wildlife": 0.2, "marine": 0.3, "climate": 0.3, "health": 0.2, "biodiversity": 0.3},
    "mixed":        {"air": 0.5, "water": 0.5, "soil": 0.5, "wildlife": 0.4, "marine": 0.4, "climate": 0.4, "health": 0.4, "biodiversity": 0.4},
}

IMPACT_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    "air":         {True: "Releases toxic gases and particulates into the atmosphere during improper disposal or burning.", False: "Minimal air pollution under proper disposal conditions."},
    "water":       {True: "Leachate and runoff contaminate groundwater, rivers, and drinking water supplies.", False: "Low risk of water body contamination under recommended disposal."},
    "soil":        {True: "Toxic compounds persist in soil, degrading fertility and harming microbiota.", False: "Minimal soil contamination risk with proper handling."},
    "wildlife":    {True: "Animals mistake waste for food or become entangled, causing injury and death.", False: "Wildlife impact is minimal with proper containment."},
    "marine":      {True: "Marine plastic and chemical waste devastates aquatic ecosystems and food chains.", False: "Low marine ecosystem risk under correct disposal management."},
    "climate":     {True: "Greenhouse gas emissions from decomposition or burning contribute to climate change.", False: "Low greenhouse gas contribution under proper disposal method."},
    "health":      {True: "Direct exposure to pathogens, toxins, or carcinogens poses acute health risks.", False: "Minimal direct human health exposure risk."},
    "biodiversity":{True: "Toxic pollution and habitat disruption threaten species diversity and ecosystem balance.", False: "Biodiversity impact is contained under proper disposal protocols."},
}


class EnvironmentalEngine:

    def calculate_environmental_impact(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate multi-dimensional environmental impact with XAI scoring.
        """
        cat = classification["category_key"]
        qty = classification.get("quantity_kg", 1.0)
        weights = IMPACT_WEIGHTS.get(cat, IMPACT_WEIGHTS["mixed"])

        dimensions = {}
        for dim, w in weights.items():
            score     = round(w * 100, 1)
            high_risk = score >= 50
            dimensions[dim] = {
                "score":       score,
                "level":       "HIGH" if score >= 70 else "MODERATE" if score >= 40 else "LOW",
                "description": IMPACT_DESCRIPTIONS[dim][high_risk],
            }

        # Composite environmental impact score (0–100)
        env_score = round(sum(v["score"] for v in dimensions.values()) / len(dimensions), 1)
        if env_score >= 70:
            impact_level = "CRITICAL"
            impact_color = "#ef4444"
        elif env_score >= 50:
            impact_level = "HIGH"
            impact_color = "#f97316"
        elif env_score >= 30:
            impact_level = "MODERATE"
            impact_color = "#f59e0b"
        else:
            impact_level = "LOW"
            impact_color = "#22c55e"

        xai_reason = (
            f"For {qty} kg of {classification['category_label']} waste, the aggregate environmental "
            f"impact score is {env_score}/100 ({impact_level}). "
            f"The highest risks are {', '.join([d for d, v in dimensions.items() if v['score'] >= 70][:3]) or 'none identified'}."
        )

        return {
            "environmental_score":  env_score,
            "impact_level":         impact_level,
            "impact_color":         impact_color,
            "dimensions":           dimensions,
            "xai_reason":           xai_reason,
            "confidence":           classification["confidence"],
        }

    def estimate_carbon_footprint(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate CO2 emissions (kg CO2e) for each disposal method.
        Returns comparison and best method recommendation.
        """
        cat = classification["category_key"]
        qty = classification.get("quantity_kg", 1.0)
        factors = CARBON_FACTORS.get(cat, CARBON_FACTORS["mixed"])

        emissions: Dict[str, float] = {}
        for method, factor in factors.items():
            emissions[method] = round(factor * qty, 4)

        # Best method = lowest (or most negative) emission
        best_method = min(emissions, key=lambda m: emissions[m])
        best_val    = emissions[best_method]

        method_labels = {
            "burn":    "Incineration / Burning",
            "bury":    "Landfill / Burial",
            "recycle": "Recycling",
            "compost": "Composting",
            "energy":  "Waste-to-Energy",
        }

        comparison = [
            {
                "method":       method_labels.get(m, m.title()),
                "method_key":   m,
                "emissions_kg": v,
                "is_best":      m == best_method,
                "label":        "✅ Most Sustainable" if m == best_method else (
                                "⚠️ Moderate Emissions" if v < 1 else "🔴 High Emissions"),
            }
            for m, v in sorted(emissions.items(), key=lambda x: x[1])
        ]

        savings_vs_burn = round(emissions.get("burn", 0) - best_val, 4)

        xai_reason = (
            f"{method_labels.get(best_method, best_method.title())} is the most sustainable disposal method "
            f"for this {classification['category_label']} waste, generating {best_val} kg CO2e per kg "
            f"(vs {emissions.get('burn', 0)} kg CO2e if burned). "
            f"Choosing this method saves {max(0, savings_vs_burn)} kg CO2e per {qty} kg of waste."
        )

        return {
            "best_method":           method_labels.get(best_method, best_method.title()),
            "best_method_key":       best_method,
            "best_method_emissions": best_val,
            "savings_vs_incineration": max(0, savings_vs_burn * qty),
            "comparison":            comparison,
            "unit":                  "kg CO2e",
            "quantity_kg":           qty,
            "xai_reason":            xai_reason,
            "confidence":            classification["confidence"],
        }


environmental_engine = EnvironmentalEngine()
