"""
ai/decision_engine.py – Master AI Decision Orchestrator
Combines outputs from all service modules into a single, unified decision
with explainable reasoning and confidence scoring.
"""
from typing import Dict, Any, List
import time


class DecisionEngine:
    """
    Master decision engine that orchestrates all AI sub-engines.
    Produces a final, auditable, explainable AI decision for every waste analysis.
    """

    def make_final_decision(
        self,
        classification: Dict[str, Any],
        recycling:       Dict[str, Any],
        risk:            Dict[str, Any],
        environmental:   Dict[str, Any],
        carbon:          Dict[str, Any],
        scores:          Dict[str, Any],
        emergency_alerts: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Synthesise all analysis results into a single master decision.

        Decision priority order:
          1. Emergency / Critical safety overrides
          2. Hazardous / Biomedical routing
          3. Recyclability path
          4. Compostability path
          5. Energy recovery path
          6. Landfill (last resort)
        """
        cat       = classification.get("category_key", "mixed")
        is_toxic  = classification.get("is_toxic", False)
        risk_sc   = risk.get("risk_score", 0)
        sust_sc   = scores.get("sustainability_score", 50)
        rec_eff   = recycling.get("recycling_efficiency", 0)

        # ── Decision Logic ──────────────────────────────────────
        if emergency_alerts and any(a["severity"] == "CRITICAL" for a in emergency_alerts):
            primary_action   = "EMERGENCY CONTAINMENT"
            decision_reason  = "Critical emergency detected. Immediate containment and professional handling required."
            decision_priority = "CRITICAL"
            confidence       = 99

        elif is_toxic or cat in ("hazardous", "biomedical"):
            primary_action   = "SPECIALIST DISPOSAL"
            decision_reason  = "Toxic or biomedical waste requires certified specialist disposal to prevent health and environmental harm."
            decision_priority = "HIGH"
            confidence       = 96

        elif recycling.get("is_recyclable") and rec_eff >= 60:
            primary_action   = "RECYCLE"
            decision_reason  = f"High recyclability confirmed ({rec_eff}% efficiency). Recycling maximises material recovery and minimises carbon footprint."
            decision_priority = "OPTIMAL"
            confidence       = max(85, scores.get("recycling_score", 85))

        elif recycling.get("is_compostable"):
            primary_action   = "COMPOST"
            decision_reason  = "Biodegradable organic material. Composting converts it into valuable soil amendment while avoiding methane emissions in landfill."
            decision_priority = "OPTIMAL"
            confidence       = 92

        elif recycling.get("energy_recovery"):
            primary_action   = "ENERGY RECOVERY"
            decision_reason  = "Material is not directly recyclable but has calorific value. Waste-to-energy conversion is preferred over landfill."
            decision_priority = "MODERATE"
            confidence       = 78

        else:
            primary_action   = "CONTROLLED LANDFILL"
            decision_reason  = "No viable recycling or energy recovery pathway identified. Dispose in licensed landfill with proper containment."
            decision_priority = "LOW"
            confidence       = 65

        # ── Alternative Actions ─────────────────────────────────
        alternatives = self._generate_alternatives(cat, recycling, classification)

        # ── Decision Summary ────────────────────────────────────
        return {
            "primary_action":      primary_action,
            "decision_priority":   decision_priority,
            "decision_confidence": confidence,
            "decision_reason":     decision_reason,
            "alternative_actions": alternatives,
            "sustainability_alignment": self._score_alignment(primary_action, sust_sc),
            "carbon_alignment":    self._carbon_alignment(primary_action, carbon),
            "decision_timestamp":  time.time(),
            "decision_metadata": {
                "category":       cat,
                "risk_score":     risk_sc,
                "sustainability": sust_sc,
                "rec_efficiency": rec_eff,
            },
        }

    def _generate_alternatives(
        self,
        cat:          str,
        recycling:    Dict[str, Any],
        classification: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """Generate a ranked list of alternative disposal methods."""
        alternatives = []
        if recycling.get("is_reusable"):
            alternatives.append({"action": "REUSE", "reason": "Direct reuse avoids all disposal impacts."})
        if cat in ("ewaste",):
            alternatives.append({"action": "REFURBISH / DONATE", "reason": "Working devices can be donated to extend product lifecycle."})
        if classification.get("requires_special_handling"):
            alternatives.append({"action": "PROFESSIONAL COLLECTION", "reason": "Special handling required — contact certified waste management."})
        if recycling.get("is_compostable"):
            alternatives.append({"action": "HOME COMPOSTING", "reason": "Small quantities can be home-composted if no contaminants."})
        return alternatives[:3]  # Return top 3

    def _score_alignment(self, action: str, sust_score: float) -> str:
        """Describe how well the primary action aligns with sustainability goals."""
        if action in ("RECYCLE", "COMPOST") and sust_score >= 70:
            return "Excellent — fully aligned with sustainability goals."
        elif action in ("RECYCLE", "COMPOST"):
            return "Good — aligned with circular economy principles."
        elif action == "ENERGY RECOVERY":
            return "Moderate — recovers energy but generates some emissions."
        elif action == "SPECIALIST DISPOSAL":
            return "Necessary — safety overrides sustainability preference."
        else:
            return "Poor — landfill should only be the last resort."

    def _carbon_alignment(self, action: str, carbon: Dict[str, Any]) -> str:
        """Describe carbon footprint alignment of the chosen action."""
        best = carbon.get("best_method", "").lower()
        if "recycle" in action.lower() and "recycle" in best:
            return f"Optimal — saves {carbon.get('savings_vs_incineration', 0)} kg CO₂e vs incineration."
        elif "compost" in action.lower():
            return "Good — composting generates minimal net CO₂."
        else:
            return f"Best available: {carbon.get('best_method', 'N/A')} ({carbon.get('best_method_emissions', 0)} kg CO₂e)."


decision_engine = DecisionEngine()
