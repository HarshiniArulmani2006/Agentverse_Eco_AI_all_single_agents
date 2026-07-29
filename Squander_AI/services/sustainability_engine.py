"""
AI Sustainability Engine
- Calculates 6 AI Sustainability Scores (0-100 each)
- Generates personalized sustainability recommendations
- Provides Circular Economy intelligence
- Produces AI-powered sustainability reports
- Tracks zero-waste progress
"""
from typing import Dict, Any, List


SUSTAINABILITY_RECOMMENDATIONS = {
    "plastic": [
        "🔄 Replace single-use plastics with reusable alternatives (cloth bags, steel bottles).",
        "🛍️ Carry a reusable bag — avoids ~500 plastic bags per person per year.",
        "♻️ Sort and clean plastics before recycling — contamination reduces recyclability by 40%.",
        "📦 Choose products with minimal plastic packaging from eco-certified brands.",
        "💧 Use refill stations for shampoo, soap, and cleaning products.",
    ],
    "organic": [
        "🌱 Start a home compost bin — turns food waste into garden gold.",
        "🍱 Plan meals to reduce food waste — save up to 30% of food purchased.",
        "🥦 Buy in bulk to reduce packaging. Store properly to extend shelf life.",
        "🐛 Use kitchen scraps for vermicomposting — generates premium fertilizer.",
        "🌍 Donate excess food to local food banks before it becomes waste.",
    ],
    "paper": [
        "🌲 Go paperless — digital bills, e-tickets, and online receipts save thousands of trees.",
        "📝 Print double-sided and reuse scrap paper for notes.",
        "📰 Subscribe to digital newspapers — saves 30 kg paper per year per household.",
        "🗒️ Choose recycled-content paper products (FSC certified).",
        "📦 Flatten and dry cardboard boxes before recycling — increases processing efficiency.",
    ],
    "glass": [
        "🫙 Reuse glass jars for food storage, organizing, or craft projects.",
        "🍾 Return glass bottles to refill programs where available.",
        "♻️ Always rinse glass before recycling — remove lids for separate recycling.",
        "🪴 Repurpose glass containers as planters or decorative storage.",
    ],
    "metal": [
        "🥫 Rinse and crush cans before recycling — saves 60% more space in collection trucks.",
        "🔧 Donate working metal appliances to repair cafés instead of discarding.",
        "💎 Scrap metal has value — contact local dealers for old aluminium or copper.",
        "🔩 Repair metal furniture before replacing it — extends product life by years.",
    ],
    "ewaste": [
        "📱 Donate working electronics to schools, NGOs, or refurbishment programs.",
        "🔋 Return batteries to designated collection points — never bin them.",
        "💻 Buy certified refurbished electronics — saves up to 70% of production emissions.",
        "🛠️ Use repair shops to fix devices before replacing them.",
        "🔌 Unplug devices when not in use — reduces phantom energy consumption.",
    ],
    "hazardous": [
        "🧪 Use eco-friendly cleaning alternatives (vinegar, baking soda) instead of harsh chemicals.",
        "🎨 Buy only the amount of paint or chemical you need — avoid leftover disposal.",
        "🏷️ Always read labels and follow safe disposal instructions.",
        "📅 Attend community hazardous waste collection events for safe drop-off.",
        "☠️ Never pour chemicals down drains or into storm drains.",
    ],
    "default": [
        "♻️ Segregate waste at source — organic, recyclable, and general waste.",
        "🌿 Adopt the 5R principle: Refuse → Reduce → Reuse → Recycle → Rot.",
        "📦 Choose products with eco-labels (FSC, Energy Star, EU Ecolabel).",
        "🌍 Calculate your household carbon footprint and set reduction targets.",
        "🌱 Plant a tree — one tree absorbs 21 kg CO2 per year on average.",
    ],
}

CIRCULAR_ECONOMY_INSIGHTS: Dict[str, str] = {
    "plastic":      "Closed-loop plastic recycling can recover 91% of material value. Advanced chemical recycling can convert plastic back to virgin-quality feedstock.",
    "organic":      "Anaerobic digestion converts organic waste to biogas (energy) and digestate (fertilizer), creating a complete circular nutrient cycle.",
    "paper":        "Paper fibers can be recycled 5–7 times before quality degrades. Each cycle saves 17 trees and 7,000 gallons of water per ton.",
    "glass":        "Glass is 100% recyclable infinitely without quality loss. Using recycled glass (cullet) reduces furnace energy by 30%.",
    "metal":        "Aluminum recycling requires only 5% of the energy needed for primary smelting. Circular metal loops can run indefinitely.",
    "ewaste":       "Urban mining of e-waste recovers gold, silver, and palladium — more concentrated than natural ore deposits.",
    "hazardous":    "Solvent recovery systems can reclaim 85–95% of used solvents for reuse in industrial processes.",
    "construction": "Crushed concrete aggregate can replace up to 30% of virgin aggregate in new construction, reducing quarrying impact.",
    "agricultural": "Crop residue biogas plants generate renewable energy while returning nutrient-rich slurry to farmland.",
    "mixed":        "Refuse-Derived Fuel (RDF) from mixed waste can substitute coal in industrial furnaces, diverting waste from landfill.",
}

ECO_BADGES = [
    {"badge": "🌱 Green Starter",      "points_required": 50,  "description": "Completed first waste analysis"},
    {"badge": "♻️ Recycler Hero",       "points_required": 150, "description": "Recycled 10+ waste items correctly"},
    {"badge": "🌍 Planet Protector",    "points_required": 300, "description": "Prevented 50 kg CO2e through smart disposal"},
    {"badge": "🔋 Zero Waste Warrior",  "points_required": 500, "description": "Achieved 60%+ recycling rate for 30 days"},
    {"badge": "🏆 Eco Champion",        "points_required": 750, "description": "Completed all eco challenges"},
    {"badge": "🌟 Sustainability Expert","points_required":1000, "description": "Top 10% in community recycling leaderboard"},
]

ECO_CHALLENGES = [
    {"challenge": "Plastic-Free Week",        "reward_points": 100, "description": "Go 7 days without buying single-use plastic."},
    {"challenge": "Compost 5 kg of Organics", "reward_points": 80,  "description": "Divert 5 kg of food waste from landfill via composting."},
    {"challenge": "E-Waste Drop-Off",         "reward_points": 120, "description": "Drop off at least one e-waste item at a certified center."},
    {"challenge": "Zero Food Waste Day",      "reward_points": 60,  "description": "Plan meals to eliminate food waste for one full day."},
    {"challenge": "Recycling Streak (7 Days)","reward_points": 90,  "description": "Correctly segregate and recycle waste for 7 consecutive days."},
    {"challenge": "Green Purchase",           "reward_points": 50,  "description": "Buy one product with eco-certification or recycled content."},
]


class SustainabilityEngine:

    def calculate_ai_scores(self, classification: Dict[str, Any], risk_score: float) -> Dict[str, Any]:
        """
        Calculate 6 AI Sustainability Scores (0–100) with XAI reasoning.
        """
        cat  = classification["category_key"]
        conf = classification["confidence"]
        rec  = classification["recyclability"]
        eff  = rec.get("recycling_efficiency", 0)

        # 1. Waste Score: how well the waste type is managed
        waste_score = min(100, round(100 - risk_score * 0.5 + eff * 0.3, 1))

        # 2. Recycling Score
        recycling_score = round(
            eff * 0.6 +
            (20 if rec.get("recyclable") else 0) +
            (10 if rec.get("compostable") else 0) +
            (10 if rec.get("reusable") else 0),
            1
        )
        recycling_score = min(100, recycling_score)

        # 3. Environmental Score: inverse of environmental damage
        env_damage = ENVIRONMENTAL_DAMAGE_INDEX.get(cat, 50)
        environmental_score = round(max(0, 100 - env_damage), 1)

        # 4. Sustainability Score: composite
        sustainability_score = round((waste_score + recycling_score + environmental_score) / 3, 1)

        # 5. Circular Economy Score
        circular_score = round(
            eff * 0.4 +
            (20 if rec.get("recyclable") else 0) +
            (15 if rec.get("reusable") else 0) +
            (15 if rec.get("compostable") else 0) +
            (10 if rec.get("energy_recovery") else 0),
            1
        )
        circular_score = min(100, circular_score)

        # 6. Carbon Reduction Score
        carbon_score = min(100, round(eff * 0.7 + (30 if cat in ("organic", "paper") else 0), 1))

        return {
            "waste_score":            waste_score,
            "recycling_score":        recycling_score,
            "environmental_score":    environmental_score,
            "sustainability_score":   sustainability_score,
            "circular_economy_score": circular_score,
            "carbon_reduction_score": carbon_score,
            "score_confidence":       conf,
            "xai_reason": (
                f"Scores based on {cat} waste category: {eff}% recycling efficiency, "
                f"risk level {round(risk_score, 1)}/100, and material recyclability flags. "
                f"Overall sustainability score of {sustainability_score}/100 reflects combined waste, recycling, and environmental factors."
            ),
        }

    def get_recommendations(self, classification: Dict[str, Any]) -> List[str]:
        cat = classification["category_key"]
        return SUSTAINABILITY_RECOMMENDATIONS.get(cat, SUSTAINABILITY_RECOMMENDATIONS["default"])

    def get_circular_economy_insight(self, classification: Dict[str, Any]) -> str:
        cat = classification["category_key"]
        return CIRCULAR_ECONOMY_INSIGHTS.get(cat, "Implementing circular economy principles for this waste stream reduces landfill dependency and recovers valuable materials.")

    def get_eco_badges(self) -> List[Dict[str, Any]]:
        return ECO_BADGES

    def get_eco_challenges(self) -> List[Dict[str, Any]]:
        return ECO_CHALLENGES

    def generate_sustainability_report(self, full_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI sustainability report from a full waste analysis."""
        scores   = full_analysis.get("sustainability_scores", {})
        cls      = full_analysis.get("classification", {})
        recycling= full_analysis.get("recycling", {})
        carbon   = full_analysis.get("carbon_footprint", {})

        return {
            "title":          f"AI Sustainability Report – {cls.get('category_label', 'Waste')} ({cls.get('quantity_kg', 1)} kg)",
            "overall_grade":  self._grade(scores.get("sustainability_score", 50)),
            "scores":         scores,
            "key_findings": [
                f"Waste classified as {cls.get('category_label')} with {cls.get('confidence')}% confidence.",
                f"Recycling efficiency: {recycling.get('recycling_efficiency', 0)}%.",
                f"Best disposal method: {carbon.get('best_method', 'N/A')} — saves {carbon.get('savings_vs_incineration', 0)} kg CO2e.",
                f"Circular economy potential score: {scores.get('circular_economy_score', 0)}/100.",
            ],
            "recommendations": full_analysis.get("sustainability_recommendations", [])[:5],
            "circular_economy_insight": full_analysis.get("circular_economy_insight", ""),
        }

    def _grade(self, score: float) -> str:
        if score >= 85: return "A+ (Outstanding)"
        if score >= 70: return "A (Excellent)"
        if score >= 55: return "B (Good)"
        if score >= 40: return "C (Moderate)"
        if score >= 25: return "D (Poor)"
        return "F (Critical)"


# Lookup: environmental damage index per category (0–100, higher = more damage)
ENVIRONMENTAL_DAMAGE_INDEX: Dict[str, float] = {
    "organic": 15, "plastic": 75, "paper": 25, "glass": 15,
    "metal": 40, "ewaste": 80, "hazardous": 92, "biomedical": 85,
    "construction": 40, "industrial": 70, "agricultural": 25, "mixed": 50,
}

sustainability_engine = SustainabilityEngine()
