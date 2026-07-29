"""
ai/__init__.py – AI Module Package
Provides access to all AI sub-engines:
  decision_engine, confidence_engine, explainable_ai,
  anomaly_detection, trend_prediction
"""
from ai.decision_engine    import decision_engine
from ai.confidence_engine  import confidence_engine
from ai.explainable_ai     import explainable_ai
from ai.anomaly_detection  import anomaly_detector
from ai.trend_prediction   import trend_predictor

__all__ = [
    "decision_engine",
    "confidence_engine",
    "explainable_ai",
    "anomaly_detector",
    "trend_predictor",
]
