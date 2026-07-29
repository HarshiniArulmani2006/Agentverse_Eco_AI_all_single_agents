"""
AI Waste Classification Engine
- Classifies waste into 12 categories using rule-based AI with confidence scores
- Provides Explainable AI (XAI) reasoning for every classification
- Returns disposal category, recyclability flags, and hazard indicators
"""
from typing import Dict, Any
from config import WASTE_CATEGORIES

# ──────────────────────────────────────────────────────────────
# Keyword-to-Category Mapping  (waste_type string → category key)
# ──────────────────────────────────────────────────────────────
WASTE_KEYWORD_MAP: Dict[str, str] = {
    # Organic
    "food": "organic", "food waste": "organic", "organic": "organic",
    "fruit": "organic", "vegetable": "organic", "peel": "organic",
    "leftovers": "organic", "coffee grounds": "organic", "eggshell": "organic",
    "garden waste": "organic", "grass": "organic", "leaves": "organic",
    "plant": "organic", "compost": "organic", "meat": "organic", "fish": "organic",
    # Plastic
    "plastic": "plastic", "plastic bottle": "plastic", "plastic bag": "plastic",
    "polythene": "plastic", "styrofoam": "plastic", "foam": "plastic",
    "pet bottle": "plastic", "hdpe": "plastic", "pvc": "plastic",
    "plastic container": "plastic", "straw": "plastic", "zip bag": "plastic",
    "wrapper": "plastic",
    # Paper
    "paper": "paper", "cardboard": "paper", "newspaper": "paper",
    "magazine": "paper", "book": "paper", "carton": "paper",
    "tissue": "paper", "receipt": "paper", "envelope": "paper",
    "box": "paper", "notebook": "paper", "paper bag": "paper",
    # Glass
    "glass": "glass", "glass bottle": "glass", "jar": "glass",
    "window glass": "glass", "mirror": "glass", "wine bottle": "glass",
    "beer bottle": "glass",
    # Metal
    "metal": "metal", "can": "metal", "aluminum": "metal", "aluminium": "metal",
    "tin can": "metal", "steel": "metal", "iron": "metal", "copper": "metal",
    "metal can": "metal", "scrap metal": "metal", "wire": "metal",
    # E-Waste
    "ewaste": "ewaste", "e-waste": "ewaste", "electronic": "ewaste",
    "battery": "ewaste", "phone": "ewaste", "mobile": "ewaste",
    "laptop": "ewaste", "computer": "ewaste", "tv": "ewaste",
    "television": "ewaste", "monitor": "ewaste", "keyboard": "ewaste",
    "charger": "ewaste", "circuit": "ewaste", "circuit board": "ewaste",
    "printer": "ewaste", "appliance": "ewaste", "refrigerator": "ewaste",
    "microwave": "ewaste",
    # Hazardous
    "hazardous": "hazardous", "chemical": "hazardous", "paint": "hazardous",
    "solvent": "hazardous", "pesticide": "hazardous", "herbicide": "hazardous",
    "insecticide": "hazardous", "fertilizer": "hazardous", "acid": "hazardous",
    "bleach": "hazardous", "fuel": "hazardous", "oil": "hazardous",
    "lubricant": "hazardous", "motor oil": "hazardous", "gas cylinder": "hazardous",
    "aerosol": "hazardous", "mercury": "hazardous", "lead": "hazardous",
    # Biomedical
    "biomedical": "biomedical", "medical": "biomedical", "syringe": "biomedical",
    "needle": "biomedical", "bandage": "biomedical", "glove": "biomedical",
    "mask": "biomedical", "medicine": "biomedical", "drug": "biomedical",
    "pills": "biomedical", "surgical": "biomedical", "blood": "biomedical",
    "pathological": "biomedical",
    # Construction
    "construction": "construction", "debris": "construction", "rubble": "construction",
    "brick": "construction", "concrete": "construction", "tile": "construction",
    "wood": "construction", "plaster": "construction", "cement": "construction",
    "renovation": "construction", "drywall": "construction",
    # Industrial
    "industrial": "industrial", "manufacturing": "industrial", "slag": "industrial",
    "ash": "industrial", "fly ash": "industrial", "sludge": "industrial",
    "effluent": "industrial", "factory": "industrial",
    # Agricultural
    "agricultural": "agricultural", "crop": "agricultural", "straw": "agricultural",
    "husk": "agricultural", "manure": "agricultural", "farm": "agricultural",
    "animal waste": "agricultural", "dung": "agricultural",
}

DISPOSAL_MAP: Dict[str, str] = {
    "organic":      "Composting Facility",
    "plastic":      "Recycling Center",
    "paper":        "Paper Recycling Center",
    "glass":        "Glass Recycling Center",
    "metal":        "Metal Scrap Recycling",
    "ewaste":       "Certified E-Waste Collection",
    "hazardous":    "Hazardous Waste Facility",
    "biomedical":   "Biomedical Waste Processing Plant",
    "construction": "Construction Debris Landfill / Reuse Depot",
    "industrial":   "Industrial Waste Treatment Facility",
    "agricultural": "Composting or Biogas Plant",
    "mixed":        "General Waste Landfill",
}

XAI_REASONS: Dict[str, str] = {
    "organic":      "The waste contains biodegradable biological materials. Composting breaks it down safely and returns nutrients to soil, making it the most sustainable disposal path.",
    "plastic":      "Identified as petroleum-derived polymer material. Recycling recovers raw material value and avoids persistent environmental pollution from long degradation times (400+ years).",
    "paper":        "Cellulose-based fibrous material with high recyclability. Paper recycling saves 17 trees and 7,000 gallons of water per ton processed.",
    "glass":        "Inert silica-based material that can be recycled infinitely without quality loss. Glass recycling reduces energy consumption by up to 30% compared to virgin manufacture.",
    "metal":        "Metal alloy with high intrinsic recyclability. Metal recycling saves up to 95% of energy compared to primary smelting from ore.",
    "ewaste":       "Contains valuable rare earth metals (gold, silver, palladium) and toxic substances (lead, mercury, cadmium). Requires certified e-waste processing to recover materials and prevent contamination.",
    "hazardous":    "Contains toxic, flammable, corrosive, or reactive chemical compounds. Improper disposal causes groundwater contamination, soil toxicity, and severe health hazards.",
    "biomedical":   "Contaminated with biological pathogens or pharmaceutical compounds. Requires incineration or autoclaving to eliminate infection risk and prevent disease transmission.",
    "construction": "Inert building materials with moderate reuse potential. Segregating concrete, wood, and metals from construction debris enables partial material recovery.",
    "industrial":   "Industrial process byproducts with complex chemical compositions. Requires specialized treatment to neutralize toxins before safe disposal.",
    "agricultural": "Biomass residue from farming activities. High potential for composting or anaerobic digestion to generate biogas and organic fertilizer.",
    "mixed":        "Mixed waste composition prevents effective single-stream recycling. Manual segregation at source is recommended before disposal.",
}

RECYCLABILITY_MAP: Dict[str, Dict[str, Any]] = {
    "organic":      {"recyclable": False, "reusable": False, "compostable": True,  "recycling_efficiency": 0,  "energy_recovery": True},
    "plastic":      {"recyclable": True,  "reusable": True,  "compostable": False, "recycling_efficiency": 91, "energy_recovery": True},
    "paper":        {"recyclable": True,  "reusable": True,  "compostable": True,  "recycling_efficiency": 87, "energy_recovery": False},
    "glass":        {"recyclable": True,  "reusable": True,  "compostable": False, "recycling_efficiency": 95, "energy_recovery": False},
    "metal":        {"recyclable": True,  "reusable": True,  "compostable": False, "recycling_efficiency": 98, "energy_recovery": False},
    "ewaste":       {"recyclable": True,  "reusable": True,  "compostable": False, "recycling_efficiency": 75, "energy_recovery": False},
    "hazardous":    {"recyclable": False, "reusable": False, "compostable": False, "recycling_efficiency": 20, "energy_recovery": True},
    "biomedical":   {"recyclable": False, "reusable": False, "compostable": False, "recycling_efficiency": 0,  "energy_recovery": False},
    "construction": {"recyclable": True,  "reusable": True,  "compostable": False, "recycling_efficiency": 65, "energy_recovery": False},
    "industrial":   {"recyclable": True,  "reusable": False, "compostable": False, "recycling_efficiency": 55, "energy_recovery": True},
    "agricultural": {"recyclable": False, "reusable": False, "compostable": True,  "recycling_efficiency": 0,  "energy_recovery": True},
    "mixed":        {"recyclable": False, "reusable": False, "compostable": False, "recycling_efficiency": 35, "energy_recovery": False},
}

PRODUCT_MAP: Dict[str, list] = {
    "plastic":      ["Polyester Fiber", "New Plastic Bottle", "Furniture Material", "Carpet Fiber", "Drainage Pipe"],
    "paper":        ["Recycled Paper", "Cardboard Packaging", "Newspaper Print", "Tissue Paper"],
    "glass":        ["New Glass Bottle", "Fiberglass Insulation", "Decorative Tiles", "Road Aggregate"],
    "metal":        ["New Metal Products", "Construction Steel", "Automotive Parts", "Cans"],
    "ewaste":       ["Recovered Gold/Silver", "Refurbished Devices", "Circuit Board Materials"],
    "organic":      ["Compost Fertilizer", "Biogas / Biomethane", "Soil Conditioner"],
    "construction": ["Recycled Aggregate", "Road Sub-Base", "Fill Material"],
    "agricultural": ["Biogas", "Organic Fertilizer", "Animal Feed"],
    "hazardous":    ["Recovered Solvents", "Treated Fuel"],
    "industrial":   ["Recovered Fly Ash (Cement)", "Processed Slag"],
    "biomedical":   [],
    "mixed":        ["Refuse-Derived Fuel (RDF)"],
}


class WasteClassificationEngine:

    def classify(self, waste_type: str, quantity_kg: float = 1.0, source: str = "residential") -> Dict[str, Any]:
        """
        Classify waste type and return full classification result with XAI reasoning.
        """
        wt_lower = waste_type.strip().lower()

        # Match keyword
        category_key = "mixed"
        best_match_len = 0
        for keyword, cat in WASTE_KEYWORD_MAP.items():
            if keyword in wt_lower and len(keyword) > best_match_len:
                category_key = cat
                best_match_len = len(keyword)

        # Confidence scoring based on match quality
        if best_match_len == 0:
            confidence = 45
        elif best_match_len >= len(wt_lower) - 1:
            confidence = 97
        elif best_match_len > len(wt_lower) // 2:
            confidence = 88
        else:
            confidence = 72

        category_info   = WASTE_CATEGORIES[category_key]
        recyclability   = RECYCLABILITY_MAP[category_key]
        disposal        = DISPOSAL_MAP[category_key]
        xai_reason      = XAI_REASONS[category_key]
        products        = PRODUCT_MAP.get(category_key, [])

        # Hazard flags
        is_toxic    = category_key in ("hazardous", "biomedical")
        is_flammable= category_key in ("hazardous",) or "fuel" in wt_lower or "paint" in wt_lower

        return {
            "input_waste_type": waste_type,
            "category_key":     category_key,
            "category_label":   category_info["label"],
            "category_icon":    category_info["icon"],
            "category_color":   category_info["color"],
            "bin_type":         category_info["bin"],
            "confidence":       confidence,
            "disposal_recommendation": disposal,
            "xai_reason":       xai_reason,
            "recyclability":    recyclability,
            "can_become":       products,
            "quantity_kg":      quantity_kg,
            "source":           source,
            "is_toxic":         is_toxic,
            "is_flammable":     is_flammable,
            "requires_special_handling": is_toxic or is_flammable or category_key in ("ewaste", "biomedical"),
        }


waste_classification_engine = WasteClassificationEngine()
