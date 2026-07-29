"""
app/logger.py – Structured Logging Module for EcoWaste AI
"""
import logging
import sys

def get_logger(name: str = "ecowaste") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

logger = get_logger()

def log_request(waste_type: str, quantity_kg: float, source: str):
    logger.info(f"Analysis Request -> Waste: '{waste_type}', Qty: {quantity_kg}kg, Source: {source}")

def log_ai_decision(category: str, confidence: int, action: str):
    logger.info(f"AI Decision -> Category: {category}, Confidence: {confidence}%, Action: {action}")
