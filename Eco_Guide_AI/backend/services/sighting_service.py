"""
WildGuard AI – Sighting Service
Manages wildlife sighting records: CRUD + AI analysis + Analytics.
"""
import json
import uuid
import time
import logging
from typing import List, Dict, Optional, Any
from core.config import settings

logger = logging.getLogger(__name__)

INITIAL_SIGHTINGS = [
    {
        "id": "sighting-001",
        "species_name": "Bengal Tiger",
        "scientific_name": "Panthera tigris tigris",
        "location": {"name": "Bandipur National Park, India", "latitude": 11.6674, "longitude": 76.6276},
        "observer_name": "Dr. Rajesh Kumar",
        "notes": "Spotted adult male near waterhole during evening patrol.",
        "conservation_status": "Endangered",
        "timestamp": time.time() - 86400 * 3,
        "timestamp_readable": "2026-07-25 16:30:00 UTC",
        "analysis": {
            "rarity_score": 85,
            "conservation_priority": True,
            "flags": ["⚠️ Endangered species detected"],
            "habitat_suitability": "Optimal core forest habitat",
            "significance": "High conservation significance – immediate reporting recommended",
        },
    },
    {
        "id": "sighting-002",
        "species_name": "Nilgiri Tahr",
        "scientific_name": "Nilgiritragus hylocrius",
        "location": {"name": "Eravikulam National Park, Kerala", "latitude": 10.2000, "longitude": 77.0500},
        "observer_name": "Ananya Sharma",
        "notes": "Herd of 12 grazing on cliff edge.",
        "conservation_status": "Endangered",
        "timestamp": time.time() - 86400 * 2,
        "timestamp_readable": "2026-07-26 09:15:00 UTC",
        "analysis": {
            "rarity_score": 82,
            "conservation_priority": True,
            "flags": ["⚠️ Endangered endemic species detected"],
            "habitat_suitability": "High-altitude shola grassland",
            "significance": "High conservation significance – immediate reporting recommended",
        },
    },
    {
        "id": "sighting-003",
        "species_name": "Indian Peafowl",
        "scientific_name": "Pavo cristatus",
        "location": {"name": "Coimbatore, Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558},
        "observer_name": "Vikram Patel",
        "notes": "Male displaying plumage near agricultural edge.",
        "conservation_status": "Least Concern",
        "timestamp": time.time() - 86400 * 1,
        "timestamp_readable": "2026-07-27 11:00:00 UTC",
        "analysis": {
            "rarity_score": 25,
            "conservation_priority": False,
            "flags": [],
            "habitat_suitability": "Common suburban edge habitat",
            "significance": "Standard observation – contribute to citizen science",
        },
    },
]


def _load_sightings() -> List[Dict]:
    try:
        if not os.path.exists(settings.SIGHTINGS_DB_PATH):
            _save_sightings(INITIAL_SIGHTINGS)
            return INITIAL_SIGHTINGS
        with open(settings.SIGHTINGS_DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data:
                _save_sightings(INITIAL_SIGHTINGS)
                return INITIAL_SIGHTINGS
            return data
    except Exception:
        return INITIAL_SIGHTINGS


def _save_sightings(sightings: List[Dict]):
    try:
        os.makedirs(os.path.dirname(settings.SIGHTINGS_DB_PATH), exist_ok=True)
        with open(settings.SIGHTINGS_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(sightings, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save sightings: {e}")


def add_sighting(
    species_name: str,
    scientific_name: str,
    latitude: Optional[float],
    longitude: Optional[float],
    location_name: str,
    observer_name: str,
    notes: str = "",
    conservation_status: str = "Unknown",
    image_filename: str = "",
) -> Dict:
    """Add a new sighting record."""
    sighting = {
        "id": str(uuid.uuid4()),
        "species_name": species_name,
        "scientific_name": scientific_name,
        "location": {
            "name": location_name,
            "latitude": latitude,
            "longitude": longitude,
        },
        "observer_name": observer_name,
        "notes": notes,
        "conservation_status": conservation_status,
        "image_filename": image_filename,
        "timestamp": time.time(),
        "timestamp_readable": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "analysis": None,
    }

    sighting["analysis"] = _analyze_sighting(sighting)

    sightings = _load_sightings()
    sightings.append(sighting)
    _save_sightings(sightings)
    return sighting


def _analyze_sighting(sighting: Dict) -> Dict:
    """Generate AI analysis for a sighting."""
    status = sighting.get("conservation_status", "Unknown")
    rare_statuses = {"Critically Endangered", "Endangered", "Vulnerable"}

    rarity_flags = []
    if status in rare_statuses:
        rarity_flags.append(f"⚠️ {status} species detected")

    rarity_scores = {
        "Critically Endangered": 95,
        "Endangered": 80,
        "Vulnerable": 65,
        "Near Threatened": 45,
        "Least Concern": 20,
        "Unknown": 50,
    }
    rarity_score = rarity_scores.get(status, 50)

    return {
        "rarity_score": rarity_score,
        "conservation_priority": status in rare_statuses,
        "flags": rarity_flags,
        "habitat_suitability": "Confirmed suitable ecological niche",
        "significance": (
            "High conservation significance – immediate reporting recommended"
            if rarity_score >= 65
            else "Standard observation – contribute to citizen science"
        ),
    }


def get_all_sightings() -> List[Dict]:
    return _load_sightings()


def get_sighting(sighting_id: str) -> Optional[Dict]:
    for s in _load_sightings():
        if s["id"] == sighting_id:
            return s
    return None


def delete_sighting(sighting_id: str) -> bool:
    sightings = _load_sightings()
    filtered = [s for s in sightings if s["id"] != sighting_id]
    if len(filtered) < len(sightings):
        _save_sightings(filtered)
        return True
    return False


def get_sighting_stats() -> Dict:
    sightings = _load_sightings()
    statuses = {}
    species_counts: Dict[str, int] = {}
    location_counts: Dict[str, int] = {}
    
    for s in sightings:
        st = s.get("conservation_status", "Unknown")
        statuses[st] = statuses.get(st, 0) + 1
        sp = s.get("species_name", "Unknown")
        species_counts[sp] = species_counts.get(sp, 0) + 1
        loc = s.get("location", {}).get("name", "Unknown")
        if loc:
            location_counts[loc] = location_counts.get(loc, 0) + 1

    return {
        "total_sightings": len(sightings),
        "unique_species": len(species_counts),
        "by_status": statuses,
        "top_species": sorted(species_counts.items(), key=lambda x: x[1], reverse=True)[:5],
        "top_locations": sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:5],
    }
