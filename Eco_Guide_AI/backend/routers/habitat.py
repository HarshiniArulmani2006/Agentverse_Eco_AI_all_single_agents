"""
WildGuard AI – Habitat Analysis Router
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.vision_service import analyze_habitat_from_image

router = APIRouter(prefix="/habitat", tags=["Habitat Analysis"])


class HabitatResponse(BaseModel):
    result: str
    filename: str


@router.post("/", response_model=HabitatResponse)
async def analyze_habitat(file: UploadFile = File(...)):
    """Upload an ecosystem image to get a habitat health analysis."""
    mime_type = file.content_type or "image/jpeg"
    if not mime_type.startswith("image/") and mime_type != "application/octet-stream":
        mime_type = "image/jpeg"

    image_bytes = await file.read()
    if len(image_bytes) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large (max 25 MB)")

    result = analyze_habitat_from_image(image_bytes, mime_type)
    return HabitatResponse(result=result, filename=file.filename or "habitat_image")
