"""
Conversational AI Engine
- Answers natural language questions about waste management
- Provides context-aware responses using analysis data
- Covers: recyclability, bin selection, composting, disposal, hazard, reuse
"""
from typing import Dict, Any, Optional, List


INTENT_KEYWORDS: Dict[str, List[str]] = {
    "recyclable":    ["recyclable", "recycle", "can i recycle", "is it recyclable"],
    "bin":           ["which bin", "bin", "container", "where do i put", "where should"],
    "compostable":   ["compost", "composting", "can i compost"],
    "disposal":      ["dispose", "disposal", "get rid", "throw away", "best way to dispose"],
    "pollution":     ["pollution", "pollute", "contaminate", "damage environment", "harmful"],
    "hazardous":     ["hazardous", "dangerous", "toxic", "safe", "is it safe"],
    "reuse":         ["reuse", "use again", "repurpose", "upcycle"],
    "product":       ["new product", "become", "made into", "manufactured", "recycled into"],
    "carbon":        ["carbon", "co2", "emissions", "greenhouse", "climate"],
    "impact":        ["impact", "environmental", "affect", "harm", "damage"],
}

RESPONSE_TEMPLATES: Dict[str, str] = {
    "recyclable":  (
        "Based on AI classification, **{label}** is{neg} recyclable. "
        "{eff_text} "
        "Place it in the **{bin}** bin. "
        "{reason}"
    ),
    "bin":        "For **{label}** waste, use the **{bin}** bin. {reason}",
    "compostable":"**{label}** {comp_verb}. {reason}",
    "disposal":   (
        "The recommended disposal method for **{label}** is: **{disposal}**. "
        "This is because {reason_lower}"
    ),
    "pollution":  "**{label}** poses a **{risk_level}** pollution risk (score: {risk_score}/100). {risk_reason}",
    "hazardous":  "{hazard_text}",
    "reuse":      "**{label}** {reuse_text}. Ideas: {upcycling}",
    "product":    "Properly recycled **{label}** can become: {products}.",
    "carbon":     "The most sustainable disposal for **{label}** is **{best_method}**, generating {best_val} kg CO2e. {carbon_reason}",
    "impact":     "**{label}** has an environmental impact score of **{env_score}/100** ({impact_level}). {env_reason}",
    "default":    (
        "Great question about **{label}** waste! "
        "It falls in the **{category}** category. "
        "Recommended disposal: **{disposal}**. "
        "Recycling efficiency: **{eff}%**. "
        "{reason}"
    ),
}


class ConversationalEngine:

    def _detect_intent(self, query: str) -> str:
        q_lower = query.lower()
        for intent, keywords in INTENT_KEYWORDS.items():
            if any(kw in q_lower for kw in keywords):
                return intent
        return "default"

    def answer_query(
        self,
        query: str,
        classification: Dict[str, Any],
        recycling: Dict[str, Any],
        risk: Dict[str, Any],
        environmental: Dict[str, Any],
        carbon: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a context-aware natural language answer to a waste question.
        """
        intent = self._detect_intent(query)
        label  = classification.get("category_label", "this waste")
        cat    = classification.get("category_key", "mixed")
        bin_   = classification.get("bin_type", "General Waste Bin")
        reason = classification.get("xai_reason", "")
        rec    = classification.get("recyclability", {})
        disposal = classification.get("disposal_recommendation", "General Waste Facility")
        risk_level = risk.get("risk_level", "MODERATE")
        risk_score = risk.get("risk_score", 50)
        risk_reason = risk.get("xai_reason", "")
        env_score  = environmental.get("environmental_score", 50)
        impact_lv  = environmental.get("impact_level", "MODERATE")
        env_reason = environmental.get("xai_reason", "")
        best_method= carbon.get("best_method", "Recycling")
        best_val   = carbon.get("best_method_emissions", 0)
        carbon_reason= carbon.get("xai_reason", "")
        eff        = rec.get("recycling_efficiency", 0)
        products   = ", ".join(classification.get("can_become", [])[:3]) or "limited products"
        upcycling  = ", ".join(recycling.get("upcycling_ideas", [])[:3]) or "various creative projects"

        if intent == "recyclable":
            neg      = "" if rec.get("recyclable") else " NOT"
            eff_text = f"Recycling efficiency: **{eff}%**." if rec.get("recyclable") else ""
            answer   = RESPONSE_TEMPLATES["recyclable"].format(
                label=label, neg=neg, eff_text=eff_text, bin=bin_, reason=reason)
        elif intent == "bin":
            answer   = RESPONSE_TEMPLATES["bin"].format(label=label, bin=bin_, reason=reason)
        elif intent == "compostable":
            comp_verb= "IS compostable — an excellent sustainable option!" if rec.get("compostable") else "is NOT directly compostable in standard compost bins."
            answer   = RESPONSE_TEMPLATES["compostable"].format(label=label, comp_verb=comp_verb, reason=reason)
        elif intent == "disposal":
            answer   = RESPONSE_TEMPLATES["disposal"].format(label=label, disposal=disposal, reason_lower=reason[:200].lower())
        elif intent == "pollution":
            answer   = RESPONSE_TEMPLATES["pollution"].format(label=label, risk_level=risk_level, risk_score=risk_score, risk_reason=risk_reason[:200])
        elif intent == "hazardous":
            if cat in ("hazardous", "biomedical", "ewaste"):
                hazard_text = f"⚠️ **{label}** IS considered hazardous! It requires special handling and disposal at a certified facility. {risk_reason}"
            else:
                hazard_text = f"✅ **{label}** is generally NOT considered hazardous under standard conditions. {reason}"
            answer   = RESPONSE_TEMPLATES["hazardous"].format(hazard_text=hazard_text)
        elif intent == "reuse":
            reuse_text = "can be reused or repurposed in several ways" if rec.get("reusable") else "has limited direct reuse potential, but some creative options exist"
            answer     = RESPONSE_TEMPLATES["reuse"].format(label=label, reuse_text=reuse_text, upcycling=upcycling)
        elif intent == "product":
            answer     = RESPONSE_TEMPLATES["product"].format(label=label, products=products)
        elif intent == "carbon":
            answer     = RESPONSE_TEMPLATES["carbon"].format(label=label, best_method=best_method, best_val=best_val, carbon_reason=carbon_reason[:200])
        elif intent == "impact":
            answer     = RESPONSE_TEMPLATES["impact"].format(label=label, env_score=env_score, impact_level=impact_lv, env_reason=env_reason[:200])
        else:
            answer     = RESPONSE_TEMPLATES["default"].format(
                label=label, category=label, disposal=disposal, eff=eff, reason=reason[:200])

        return {
            "query":           query,
            "intent_detected": intent,
            "answer":          answer,
            "waste_type":      label,
            "confidence":      classification.get("confidence", 85),
        }


conversational_engine = ConversationalEngine()
