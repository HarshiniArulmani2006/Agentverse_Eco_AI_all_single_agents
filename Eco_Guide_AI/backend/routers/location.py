"""
WildGuard AI – Location Intelligence Router
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.location_service import get_location_wildlife_report, get_nearby_protected_areas

router = APIRouter(prefix="/location", tags=["Location Intelligence"])


class LocationRequest(BaseModel):
    location: str
    include_protected_areas: bool = True


class LocationResponse(BaseModel):
    location: str
    report: str


@router.post("/", response_model=LocationResponse)
async def location_intelligence(req: LocationRequest):
    """Get wildlife intelligence for a location."""
    if not req.location.strip():
        raise HTTPException(status_code=400, detail="Location cannot be empty")

    report = get_location_wildlife_report(req.location)

    if req.include_protected_areas:
        pa_report = get_nearby_protected_areas(req.location)
        report += "\n\n---\n\n" + pa_report

    return LocationResponse(location=req.location, report=report)
