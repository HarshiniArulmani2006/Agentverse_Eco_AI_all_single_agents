"""
Recycling Intelligence Engine
- Determines recyclability, reusability, compostability
- Estimates recycling efficiency and circular economy opportunities
- Provides step-by-step recycling instructions and upcycling ideas
- Locates nearest recycling center type
"""
from typing import Dict, Any, List
from config import WASTE_CATEGORIES


RECYCLING_STEPS: Dict[str, List[str]] = {
    "plastic": [
        "Rinse the plastic item thoroughly to remove food residue.",
        "Check the resin identification code (1–7) on the bottom.",
        "Flatten bottles/containers to save space.",
        "Place in the designated Blue Recycling Bin.",
        "Do NOT include contaminated or food-soiled plastics.",
    ],
    "paper": [
        "Flatten cardboard boxes and remove staples or tape.",
        "Keep paper dry — wet paper cannot be recycled.",
        "Stack newspapers and magazines separately.",
        "Place in the Yellow Paper Recycling Bin.",
        "Shredded paper should be bagged before placing in bin.",
    ],
    "glass": [
        "Rinse glass bottles and jars to remove food or liquid.",
        "Remove metal lids and recycle separately.",
        "Do NOT include broken glass — wrap in newspaper and dispose separately.",
        "Place in the White Glass Recycling Bin.",
        "Mirrors and window glass are NOT recyclable in most facilities.",
    ],
    "metal": [
        "Rinse aluminum cans and steel tins.",
        "Crush cans lightly to save space.",
        "Separate ferrous (iron/steel) from non-ferrous (aluminum/copper).",
        "Place in the Silver Metal Recycling Bin.",
        "Large scrap metal should be taken to a scrap metal dealer.",
    ],
    "ewaste": [
        "Backup and wipe personal data from devices before disposal.",
        "Keep batteries separate from main device components.",
        "Do NOT disassemble — certified facilities handle this safely.",
        "Drop at a certified E-Waste Collection Center.",
        "Check manufacturer take-back programs for free recycling.",
    ],
    "organic": [
        "Separate organic waste from other waste at source.",
        "Use a dedicated compost bin or kitchen caddy.",
        "Layer 'greens' (food waste) with 'browns' (dry leaves) for composting.",
        "Avoid meat, dairy, and oily foods in home compost.",
        "Deposit at community composting facility or biogas plant.",
    ],
    "hazardous": [
        "Do NOT pour chemicals down the drain or into regular bins.",
        "Keep in original, labeled containers.",
        "Store in cool, dry, ventilated area away from children.",
        "Contact your local Hazardous Waste Facility for safe drop-off.",
        "Check household hazardous waste collection events in your area.",
    ],
    "biomedical": [
        "Place sharps (needles, syringes) in puncture-resistant containers immediately.",
        "Use designated red biohazard bags for contaminated items.",
        "Never mix biomedical waste with general household waste.",
        "Contact a licensed biomedical waste disposal service.",
        "Follow local health authority protocols strictly.",
    ],
    "construction": [
        "Sort debris: concrete, wood, metal, and tiles separately.",
        "Donate reusable materials (doors, bricks, tiles) to reuse centers.",
        "Contact a construction debris recycling service for bulk pickup.",
        "Concrete and masonry can be crushed for aggregate reuse.",
        "Hazardous construction materials (asbestos, lead paint) need special handling.",
    ],
    "agricultural": [
        "Collect crop residue and animal manure separately.",
        "Use residues for on-site composting or biogas generation.",
        "Contact local biogas plant or organic fertilizer facility.",
        "Avoid burning crop residue — contributes to air pollution.",
        "Manure can be processed into bio-fertilizer.",
    ],
    "industrial": [
        "Characterize waste composition before disposal.",
        "Engage a licensed industrial waste disposal contractor.",
        "Explore material recovery opportunities within the facility.",
        "Fly ash and slag can be sold to cement manufacturers.",
        "Maintain waste manifests as required by environmental regulations.",
    ],
    "mixed": [
        "Sort waste at source to enable proper recycling.",
        "Separate organics, recyclables, and general waste.",
        "What cannot be sorted goes to a waste-to-energy facility or landfill.",
        "Minimize mixed waste generation by improving segregation habits.",
    ],
}

UPCYCLING_IDEAS: Dict[str, List[str]] = {
    "plastic": [
        "Plastic bottles → Vertical herb garden planters",
        "Plastic bags → Woven mats or tote bags",
        "Yogurt containers → Seedling pots",
        "PET bottles → Bird feeders",
        "Plastic cutlery → DIY plant markers",
    ],
    "paper": [
        "Old newspapers → Gift wrapping paper",
        "Cardboard boxes → Storage organizers or kids' playhouses",
        "Magazines → Decorative paper bowls or collages",
        "Paper rolls → Wall art or pencil holders",
    ],
    "glass": [
        "Wine bottles → Candle holders or vases",
        "Glass jars → Food storage or desk organizers",
        "Broken glass → Mosaic art tiles",
        "Bottle caps → Wall art magnets",
    ],
    "metal": [
        "Tin cans → Flower pots or lanterns",
        "Scrap wire → Sculptures or jewelry",
        "Old pans → Wall-mounted planters",
        "Aluminum cans → Eco-friendly windmills",
    ],
    "ewaste": [
        "Old keyboards → Wall art installation",
        "Circuit boards → Steampunk jewelry or coasters",
        "Old phones → Repurpose as media players or alarm clocks",
        "Hard drives → Magnetic memo boards",
    ],
    "organic": [
        "Coffee grounds → Natural exfoliating scrub or fertilizer",
        "Eggshells → Calcium-rich soil amendment",
        "Citrus peels → Natural air freshener or cleaning agent",
        "Banana peels → Plant fertilizer or shoe polish",
    ],
    "construction": [
        "Old bricks → Garden pathway or raised planter beds",
        "Scrap wood → DIY furniture or garden frames",
        "Old tiles → Mosaic art or garden path",
        "Pallets → Outdoor furniture or vertical gardens",
    ],
    "agricultural": [
        "Rice husks → Eco-friendly packaging material",
        "Corn stalks → Biogas fuel or biodegradable plates",
        "Sugarcane bagasse → Paper and packaging products",
    ],
    "hazardous": [],
    "biomedical": [],
    "industrial": [],
    "mixed": [],
}

NEARBY_CENTERS: Dict[str, str] = {
    "plastic":      "Plastic Recycling Facility / Material Recovery Facility (MRF)",
    "paper":        "Paper Mill Recycling Drop-Off / MRF",
    "glass":        "Glass Cullet Processing Center",
    "metal":        "Scrap Metal Dealer / Metal Recycling Yard",
    "ewaste":       "Authorized E-Waste Collection Center / Manufacturer Take-Back Program",
    "organic":      "Community Compost Site / Biogas Facility",
    "hazardous":    "Municipal Hazardous Waste (HHW) Collection Facility",
    "biomedical":   "Biomedical Waste Treatment Facility (Autoclaving / Incineration)",
    "construction": "C&D Waste Recycling Depot / Concrete Crusher Plant",
    "industrial":   "Industrial Waste Management Contractor",
    "agricultural": "Biogas Plant / Organic Composting Facility",
    "mixed":        "Waste-to-Energy Plant / General Landfill",
}


class RecyclingEngine:

    def analyze(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full recycling intelligence report for a classified waste item.
        """
        cat = classification["category_key"]
        qty = classification.get("quantity_kg", 1.0)

        steps     = RECYCLING_STEPS.get(cat, [])
        upcycling = UPCYCLING_IDEAS.get(cat, [])
        center    = NEARBY_CENTERS.get(cat, "General Waste Facility")
        rec_info  = classification["recyclability"]

        efficiency   = rec_info.get("recycling_efficiency", 0)
        recyclable   = rec_info.get("recyclable", False)
        compostable  = rec_info.get("compostable", False)
        reusable     = rec_info.get("reusable", False)
        energy_rec   = rec_info.get("energy_recovery", False)

        # Estimated recovered material
        recovered_kg = round(qty * efficiency / 100, 3)

        # Circular economy opportunity score (0-100)
        circular_score = min(100, int(
            (efficiency * 0.5) +
            (20 if recyclable else 0) +
            (15 if reusable else 0) +
            (10 if compostable else 0) +
            (5 if energy_rec else 0)
        ))

        xai_reason = (
            f"With a recycling efficiency of {efficiency}%, approximately {recovered_kg} kg "
            f"of recoverable material can be extracted from {qty} kg of this waste. "
            f"{'This material is recyclable and should be sent to the appropriate recycling facility.' if recyclable else ''}"
            f"{'Composting is the recommended sustainable disposal pathway.' if compostable else ''}"
            f"{'Energy recovery through waste-to-energy conversion is possible.' if energy_rec and not recyclable and not compostable else ''}"
        )

        return {
            "is_recyclable":         recyclable,
            "is_reusable":           reusable,
            "is_compostable":        compostable,
            "energy_recovery":       energy_rec,
            "recycling_efficiency":  efficiency,
            "recovered_material_kg": recovered_kg,
            "circular_economy_score": circular_score,
            "recycling_steps":       steps,
            "upcycling_ideas":       upcycling,
            "nearest_center_type":   center,
            "can_become":            classification.get("can_become", []),
            "xai_reason":            xai_reason,
            "confidence":            classification["confidence"],
        }


recycling_engine = RecyclingEngine()
