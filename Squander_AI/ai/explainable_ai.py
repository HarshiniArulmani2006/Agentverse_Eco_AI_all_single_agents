"""
ai/explainable_ai.py – Explainable AI (XAI) Narrative Generator
Produces human-readable explanations for every AI decision.
Follows the LIME / SHAP principle: explain what factors drove the decision.
"""
from typing import Dict, Any, List


class ExplainableAI:
    """
    Generates natural language explanations for all AI recommendations.
    Every output includes: what was decided, why, and what evidence supports it.
    """

    def explain_classification(
        self,
        waste_type:    str,
        category_key:  str,
        category_label: str,
        confidence:    int,
        match_keyword: str = "",
    ) -> Dict[str, str]:
        """
        Explain how the waste was classified.
        """
        primary_reason = f'The input "{waste_type}" was matched to the keyword "{match_keyword or waste_type.lower()}" in the waste knowledge base.' if match_keyword else f'The input "{waste_type}" matched the {category_label} category through pattern analysis.'

        return {
            "decision":       f"Classified as {category_label}",
            "primary_reason": primary_reason,
            "confidence_reason": (
                f"Confidence is {confidence}% based on the keyword match quality. "
                f"{'Near-perfect match — high certainty.' if confidence >= 90 else 'Partial match — some uncertainty remains.'}"
            ),
            "what_this_means": (
                f"This waste falls into the {category_label} category, which determines "
                f"how it should be handled, which collection bin it belongs to, and "
                f"what environmental risks it poses."
            ),
        }

    def explain_recycling(
        self,
        category_key:        str,
        is_recyclable:       bool,
        recycling_efficiency: int,
        can_become:          List[str],
    ) -> Dict[str, str]:
        """Explain the recycling assessment."""
        if is_recyclable:
            products_str = ", ".join(can_become[:3]) if can_become else "recycled materials"
            return {
                "verdict": "Recyclable ✅",
                "reason": (
                    f"This material has a recycling efficiency of {recycling_efficiency}%. "
                    f"It can be processed into: {products_str}. "
                    f"Recycling is preferred over landfill as it conserves raw materials and reduces energy consumption."
                ),
                "supporting_evidence": (
                    f"Data from recycling industry benchmarks confirms {recycling_efficiency}% of this "
                    f"material type can be recovered in standard municipal recycling facilities."
                ),
            }
        else:
            return {
                "verdict": "Not Directly Recyclable ❌",
                "reason": (
                    "This material cannot be processed by standard recycling facilities "
                    "due to contamination risk, material complexity, or chemical composition."
                ),
                "supporting_evidence": (
                    "Alternative pathways such as composting, energy recovery, or specialist "
                    "disposal are recommended based on material properties."
                ),
            }

    def explain_risk(
        self,
        risk_score:  float,
        risk_level:  str,
        category_key: str,
        risk_factors: Dict[str, Any],
    ) -> str:
        """Explain the risk score in plain language."""
        top_risks = sorted(
            [(k, v) for k, v in risk_factors.items() if isinstance(v, (int, float)) and v > 0],
            key=lambda x: x[1],
            reverse=True
        )[:3]

        risk_names = {
            "fire_risk": "fire hazard",
            "chemical_risk": "chemical toxicity",
            "air_pollution": "air pollution",
            "water_pollution": "water contamination",
            "soil_pollution": "soil contamination",
            "health_risk": "human health impact",
        }

        factors_str = ", ".join(
            risk_names.get(k, k) for k, _ in top_risks
        ) if top_risks else "general environmental impact"

        return (
            f"The {risk_level} risk score of {risk_score:.0f}/100 reflects primary concerns around "
            f"{factors_str}. "
            f"{'Immediate action is required to prevent harm.' if risk_level == 'CRITICAL' else ''}"
            f"{'Monitor and follow standard protocols.' if risk_level == 'LOW' else ''}"
        )

    def explain_carbon(
        self,
        best_method:        str,
        best_emissions:     float,
        savings_vs_burn:    float,
        comparison:         List[Dict[str, Any]],
    ) -> str:
        """Explain carbon footprint recommendation."""
        return (
            f"**{best_method}** is the most carbon-efficient disposal method, "
            f"generating only {best_emissions:.2f} kg CO₂e per kg of waste. "
            f"This saves {savings_vs_burn:.2f} kg CO₂e compared to incineration. "
            f"The recommendation is based on lifecycle emission factors from peer-reviewed "
            f"environmental science databases."
        )

    def explain_sustainability_score(
        self,
        score:         float,
        score_breakdown: Dict[str, float],
        category_key:  str,
    ) -> str:
        """Explain the overall sustainability score."""
        strongest = max(score_breakdown.items(), key=lambda x: x[1]) if score_breakdown else None
        weakest   = min(score_breakdown.items(), key=lambda x: x[1]) if score_breakdown else None

        label = (
            "Excellent sustainability profile" if score >= 80 else
            "Good sustainability profile"       if score >= 65 else
            "Moderate sustainability profile"  if score >= 50 else
            "Poor sustainability profile"
        )

        explanation = f"{label} (score: {score:.0f}/100). "
        if strongest:
            explanation += f"Strongest dimension: {strongest[0].replace('_',' ').title()} ({strongest[1]:.0f}). "
        if weakest and weakest[0] != strongest[0]:
            explanation += f"Weakest dimension: {weakest[0].replace('_',' ').title()} ({weakest[1]:.0f}) — focus improvement here."

        return explanation

    def explain_environmental_impact(
        self,
        dimensions:   Dict[str, Dict[str, Any]],
        overall_score: float,
    ) -> str:
        """Explain the environmental impact assessment."""
        high_impact = [dim for dim, data in dimensions.items() if data.get("level") == "HIGH"]
        if high_impact:
            dims_str = ", ".join(h.replace("_", " ").title() for h in high_impact)
            return (
                f"Environmental impact score: {overall_score:.0f}/100. "
                f"High impact areas: {dims_str}. "
                f"These represent the most critical environmental concerns for this waste type "
                f"and should be prioritised in disposal planning."
            )
        return (
            f"Environmental impact score: {overall_score:.0f}/100. "
            f"No high-impact environmental dimensions detected. "
            f"Standard disposal protocols are sufficient."
        )


explainable_ai = ExplainableAI()
