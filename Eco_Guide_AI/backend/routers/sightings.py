"""
WildGuard AI – Sightings Router
CRUD endpoints for wildlife sighting records.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.sighting_service import (
    add_sighting,
    get_all_sightings,
    get_sighting,
    delete_sighting,
    get_sighting_stats,
)

router = APIRouter(prefix="/sightings", tags=["Wildlife Sightings"])


class SightingCreate(BaseModel):
    species_name: str
    scientific_name: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: str = ""
    observer_name: str = "Anonymous"
    notes: str = ""
    conservation_status: str = "Unknown"


@router.post("/")
async def create_sighting(req: SightingCreate):
    """Log a new wildlife sighting."""
    if not req.species_name.strip():
        raise HTTPException(status_code=400, detail="Species name is required")
    sighting = add_sighting(
        species_name=req.species_name,
        scientific_name=req.scientific_name,
        latitude=req.latitude,
        longitude=req.longitude,
        location_name=req.location_name,
        observer_name=req.observer_name,
        notes=req.notes,
        conservation_status=req.conservation_status,
    )
    return sighting


@router.get("/")
async def list_sightings():
    """Get all recorded sightings."""
    return get_all_sightings()


@router.get("/stats")
async def sighting_stats():
    """Get sighting statistics."""
    return get_sighting_stats()


@router.get("/{sighting_id}")
async def get_single_sighting(sighting_id: str):
    """Get a specific sighting by ID."""
    s = get_sighting(sighting_id)
    if not s:
        raise HTTPException(status_code=404, detail="Sighting not found")
    return s


@router.delete("/{sighting_id}")
async def remove_sighting(sighting_id: str):
    """Delete a sighting record."""
    if delete_sighting(sighting_id):
        return {"message": "Sighting deleted", "id": sighting_id}
    raise HTTPException(status_code=404, detail="Sighting not found")
