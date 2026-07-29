"""
EcoWaste AI – Configuration Settings, Thresholds & Constants
"""
import os

# ──────────────────────────────────────────────
# Server Configuration
# ──────────────────────────────────────────────
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8002"))

# ──────────────────────────────────────────────
# uAgent Configuration
# ──────────────────────────────────────────────
AGENT_NAME     = "ecowaste_ai"
AGENT_SEED     = os.getenv("AGENT_SEED", "ecowaste_ai_secret_seed_phrase_2026")
AGENT_PORT     = int(os.getenv("AGENT_PORT", "8003"))
AGENT_ENDPOINT = f"http://127.0.0.1:{AGENT_PORT}/submit"

# ──────────────────────────────────────────────
# Cache Configuration
# ──────────────────────────────────────────────
CACHE_TTL_SECONDS = 600   # 10 minutes

# ──────────────────────────────────────────────
# Waste Category Definitions
# ──────────────────────────────────────────────
WASTE_CATEGORIES = {
    "organic":       {"label": "Organic",          "color": "#22c55e", "icon": "🌿", "bin": "Green Bin"},
    "plastic":       {"label": "Plastic",           "color": "#3b82f6", "icon": "🧴", "bin": "Blue Bin"},
    "paper":         {"label": "Paper / Cardboard", "color": "#f59e0b", "icon": "📄", "bin": "Yellow Bin"},
    "glass":         {"label": "Glass",             "color": "#06b6d4", "icon": "🫙", "bin": "White Bin"},
    "metal":         {"label": "Metal",             "color": "#6366f1", "icon": "🥫", "bin": "Silver Bin"},
    "ewaste":        {"label": "E-Waste",           "color": "#8b5cf6", "icon": "💻", "bin": "Purple Bin"},
    "hazardous":     {"label": "Hazardous",         "color": "#ef4444", "icon": "☢️",  "bin": "Red Bin"},
    "biomedical":    {"label": "Biomedical",        "color": "#f43f5e", "icon": "🏥", "bin": "Red Biohazard Bin"},
    "construction":  {"label": "Construction",      "color": "#78716c", "icon": "🧱", "bin": "Skip / Debris Bin"},
    "industrial":    {"label": "Industrial",        "color": "#71717a", "icon": "🏭", "bin": "Industrial Container"},
    "agricultural":  {"label": "Agricultural",      "color": "#16a34a", "icon": "🌾", "bin": "Compost / Farm Bin"},
    "mixed":         {"label": "Mixed / Unknown",   "color": "#94a3b8", "icon": "🗑️", "bin": "General Waste Bin"},
}

# ──────────────────────────────────────────────
# Risk Level Thresholds (0-100 scale)
# ──────────────────────────────────────────────
RISK_LEVELS = [
    (25,  "LOW",      "#22c55e"),
    (50,  "MODERATE", "#f59e0b"),
    (75,  "HIGH",     "#f97316"),
    (100, "CRITICAL", "#ef4444"),
]

# ──────────────────────────────────────────────
# Carbon Emission Factors (kg CO2e per kg waste)
# ──────────────────────────────────────────────
CARBON_FACTORS = {
    "plastic":      {"burn": 2.93, "bury": 0.04, "recycle": -1.53, "energy": 0.85},
    "paper":        {"burn": 1.57, "bury": 0.90, "recycle": -0.98, "compost": -0.07},
    "organic":      {"burn": 0.62, "bury": 1.10, "compost": -0.22, "energy": 0.40},
    "glass":        {"burn": 0.02, "bury": 0.01, "recycle": -0.31, "energy": 0.01},
    "metal":        {"burn": 0.10, "bury": 0.02, "recycle": -3.70, "energy": 0.05},
    "ewaste":       {"burn": 4.50, "bury": 2.80, "recycle": -3.20, "energy": 1.20},
    "hazardous":    {"burn": 5.10, "bury": 3.60, "recycle": -1.50, "energy": 2.20},
    "biomedical":   {"burn": 3.80, "bury": 4.20, "recycle": 0.00,  "energy": 2.90},
    "construction": {"burn": 0.30, "bury": 0.15, "recycle": -0.18, "energy": 0.12},
    "agricultural": {"burn": 0.72, "bury": 0.95, "compost": -0.30, "energy": 0.35},
    "mixed":        {"burn": 1.80, "bury": 0.85, "recycle": -0.75, "energy": 0.65},
}

# ──────────────────────────────────────────────
# Smart Bin Thresholds (fill %)
# ──────────────────────────────────────────────
BIN_THRESHOLDS = {
    "empty":    (0,  30,  "#22c55e"),
    "partial":  (30, 60,  "#f59e0b"),
    "high":     (60, 85,  "#f97316"),
    "overflow": (85, 100, "#ef4444"),
}

# ──────────────────────────────────────────────
# Waste Generation Baseline (kg/household/day)
# ──────────────────────────────────────────────
DAILY_BASELINE = {
    "residential":  1.8,
    "commercial":   8.5,
    "industrial":  42.0,
}
