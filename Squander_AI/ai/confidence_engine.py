"""
ai/confidence_engine.py – AI Confidence Scoring Engine
Provides calibrated confidence scores (0-100) for every AI-generated prediction.
Uses factors like: match quality, data completeness, category certainty, risk clarity.
"""
from typing import Dict, Any


class ConfidenceEngine:
    """
    Computes calibrated confidence scores for all AI outputs.
    Higher scores indicate more reliable predictions.
    """

    def score_classification(
        self,
        match_length: int,
        input_length: int,
        category_key: str,
    ) -> int:
        """
        Confidence for waste classification based on keyword match quality.
        
        Args:
            match_length: Length of the matched keyword
            input_length:  Length of the full input string
            category_key:  Classified category

        Returns:
            Confidence score 0–100
        """
        if match_length == 0:
            base = 45          # No match found — defaulted to 'mixed'
        elif match_length >= input_length:
            base = 97          # Perfect / near-perfect match
        elif match_length >= input_length * 0.7:
            base = 88          # Strong partial match
        elif match_length >= input_length * 0.4:
            base = 74          # Moderate match
        else:
            base = 60          # Weak match

        # Boost for well-defined categories (lower ambiguity)
        category_boost = {
            "biomedical": 3, "hazardous": 2, "ewaste": 2,
            "organic": 1, "plastic": 1, "glass": 1,
            "mixed": -5,  # Penalise mixed — least certain
        }
        return min(99, max(40, base + category_boost.get(category_key, 0)))

    def score_recycling(
        self,
        recycling_efficiency: int,
        is_recyclable: bool,
        category_key: str,
    ) -> int:
        """Confidence for recyclability prediction."""
        if not is_recyclable:
            return 95   # Non-recyclable categories are well-defined
        if recycling_efficiency >= 90:
            return 92
        elif recycling_efficiency >= 70:
            return 84
        elif recycling_efficiency >= 50:
            return 76
        else:
            return 68

    def score_risk(self, risk_score: float, category_key: str) -> int:
        """Confidence for risk assessment."""
        # High-risk categories have well-established risk profiles
        high_certainty = {"hazardous", "biomedical", "ewaste"}
        low_certainty  = {"mixed", "construction"}
        if category_key in high_certainty:
            return 95
        elif category_key in low_certainty:
            return 72
        # Scale with risk score — extreme values are more certain
        if risk_score >= 80 or risk_score <= 20:
            return 88
        return 80

    def score_carbon(self, category_key: str, quantity_kg: float) -> int:
        """Confidence for carbon footprint estimation."""
        # Carbon factors are well-established for clean streams
        high_confidence = {"plastic", "paper", "glass", "metal", "organic"}
        if category_key in high_confidence:
            base = 90
        else:
            base = 78
        # More data (larger quantity) = more certainty
        if quantity_kg >= 10:
            return min(96, base + 4)
        return base

    def score_sustainability(
        self,
        recycling_score: float,
        environmental_score: float,
        carbon_score: float,
    ) -> int:
        """Confidence for overall sustainability score."""
        avg = (recycling_score + environmental_score + carbon_score) / 3
        # More balanced scores = higher confidence
        spread = max(recycling_score, environmental_score, carbon_score) - \
                 min(recycling_score, environmental_score, carbon_score)
        base = 88
        if spread > 40:
            base -= 8    # Wide spread = less certain
        return min(96, int(base))

    def score_forecast(self, source: str, days_ahead: int) -> int:
        """Confidence for waste generation forecast."""
        # Shorter horizon = higher confidence
        base = {
            1: 92, 3: 87, 7: 82, 14: 75, 30: 68, 90: 60, 365: 50
        }
        # Find nearest key
        nearest = min(base.keys(), key=lambda k: abs(k - days_ahead))
        score = base[nearest]
        # Source adjustment — industrial is most predictable
        adjustment = {"industrial": 3, "commercial": 1, "residential": -1}
        return min(96, max(45, score + adjustment.get(source, 0)))

    def aggregate_confidence(self, *scores: int) -> int:
        """
        Aggregate multiple confidence scores into a single overall confidence.
        Uses harmonic mean to penalise low-confidence outliers.
        """
        valid = [s for s in scores if s > 0]
        if not valid:
            return 50
        harmonic_mean = len(valid) / sum(1 / s for s in valid)
        return round(min(99, max(40, harmonic_mean)))

    def confidence_label(self, score: int) -> str:
        """Human-readable label for a confidence score."""
        if score >= 92:
            return "Very High"
        elif score >= 80:
            return "High"
        elif score >= 65:
            return "Moderate"
        elif score >= 50:
            return "Low"
        else:
            return "Very Low"


confidence_engine = ConfidenceEngine()
