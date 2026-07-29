"""
app/utils.py – Common Utility Helper Functions
"""
import re

def sanitize_string(input_str: str) -> str:
    """Sanitize user text input by stripping whitespace and harmful characters."""
    if not input_str:
        return ""
    cleaned = re.sub(r'[<>{}]', '', str(input_str))
    return cleaned.strip()

def clamp(val: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Clamp a float value within [min_val, max_val]."""
    return max(min_val, min(max_val, val))

def round_safe(val: float, decimals: int = 2) -> float:
    """Safely round numbers."""
    try:
        return round(float(val), decimals)
    except (ValueError, TypeError):
        return 0.0

def format_kg(val: float) -> str:
    """Format quantity in kg or tons for human display."""
    if val >= 1000:
        return f"{val / 1000:.2f} tons"
    return f"{val:.1f} kg"
