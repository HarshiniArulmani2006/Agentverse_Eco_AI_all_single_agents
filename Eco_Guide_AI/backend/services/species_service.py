"""
WildGuard AI – Species Service
Direct species search and lookup from the knowledge base.
"""
from typing import List, Dict, Optional
from services.rag_service import get_all_species, get_species_by_id, search_species


def list_all_species() -> List[Dict]:
    """Return all species in the knowledge base."""
    species = get_all_species()
    return [
        {
            "id": s.get("id"),
            "common_name": s.get("common_name"),
            "scientific_name": s.get("scientific_name", s.get("botanical_name", "")),
            "family": s.get("family"),
            "conservation_status": s.get("conservation_status", "Not Evaluated"),
            "iucn_category": s.get("iucn_category", "NE"),
            "type": "animal" if "scientific_name" in s else "plant",
        }
        for s in species
    ]


def get_species_detail(species_id: str) -> Optional[Dict]:
    """Return full detail for a species by its ID."""
    return get_species_by_id(species_id)


def search(query: str) -> List[Dict]:
    """Search species by name or keyword."""
    results = search_species(query)
    return [
        {
            "id": s.get("id"),
            "common_name": s.get("common_name"),
            "scientific_name": s.get("scientific_name", s.get("botanical_name", "")),
            "conservation_status": s.get("conservation_status", "Not Evaluated"),
            "type": "animal" if "scientific_name" in s else "plant",
        }
        for s in results
    ]
