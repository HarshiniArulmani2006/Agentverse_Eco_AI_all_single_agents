"""
WildGuard AI – Species Identification Router
Image upload endpoint for species identification.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import logging

from services.vision_service import identify_species_from_image

router = APIRouter(prefix="/identify", tags=["Species Identification"])
logger = logging.getLogger(__name__)

MAX_SIZE_MB = 25


class IdentifyResponse(BaseModel):
    result: str
    filename: str
    file_size_kb: float


@router.post("/", response_model=IdentifyResponse)
async def identify_species(file: UploadFile = File(...)):
    """Upload an image to identify the species in it."""
    mime_type = file.content_type or "image/jpeg"
    if not mime_type.startswith("image/") and mime_type != "application/octet-stream":
        mime_type = "image/jpeg"

    image_bytes = await file.read()
    size_mb = len(image_bytes) / (1024 * 1024)

    if size_mb > MAX_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.1f} MB). Maximum allowed: {MAX_SIZE_MB} MB",
        )

    result = identify_species_from_image(image_bytes, mime_type)

    return IdentifyResponse(
        result=result,
        filename=file.filename or "uploaded_image",
        file_size_kb=round(len(image_bytes) / 1024, 1),
    )
