"""
WildGuard AI – FastAPI Application Entry Point
"""
import os
import logging
from pathlib import Path

from dotenv import load_dotenv

# Load .env before any other imports that read settings
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from core.config import settings
from core.gemini_client import gemini
from services.species_service import list_all_species, get_species_detail, search

from routers import chat, identify, habitat, location, sightings, education

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(name)-25s | %(levelname)-7s | %(message)s",
)
logger = logging.getLogger("wildguard")

# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="WildGuard AI",
    description=(
        "🌿 World-class Wildlife Conservation & Biodiversity Intelligence Agent. "
        "Powered by Gemini 2.5 Pro with RAG, Vision, and Expert Knowledge."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Include Routers ─────────────────────────────────────────────────────────
app.include_router(chat.router)
app.include_router(identify.router)
app.include_router(habitat.router)
app.include_router(location.router)
app.include_router(sightings.router)
app.include_router(education.router)


# ─── Species Knowledge Base Endpoints ─────────────────────────────────────────
@app.get("/species", tags=["Species Database"])
async def get_all_species():
    """List all species in the knowledge base."""
    return list_all_species()


@app.get("/species/search", tags=["Species Database"])
async def search_species(q: str):
    """Search species by name or keyword."""
    return search(q)


@app.get("/species/{species_id}", tags=["Species Database"])
async def get_species(species_id: str):
    """Get detailed information about a species."""
    detail = get_species_detail(species_id)
    if not detail:
        return JSONResponse(status_code=404, content={"error": "Species not found"})
    return detail


# ─── Health & Status ──────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "WildGuard AI",
        "version": "1.0.0",
        "gemini_configured": gemini.is_ready,
        "model": settings.GEMINI_MODEL,
    }


@app.get("/status", tags=["System"])
async def system_status():
    return {
        "gemini_ready": gemini.is_ready,
        "gemini_model": settings.GEMINI_MODEL,
        "iucn_configured": bool(settings.IUCN_API_TOKEN),
        "species_count": len(list_all_species()),
    }


# ─── Serve Frontend ──────────────────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")



# ─── Startup ──────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    logger.info("=" * 60)
    logger.info("🌿 WildGuard AI starting up...")
    logger.info(f"   Gemini Model  : {settings.GEMINI_MODEL}")
    logger.info(f"   Gemini Ready  : {gemini.is_ready}")
    logger.info(f"   IUCN Token    : {'✅' if settings.IUCN_API_TOKEN else '❌ (optional)'}")
    logger.info(f"   Species DB    : {len(list_all_species())} entries")
    logger.info(f"   Frontend      : {'✅' if FRONTEND_DIR.exists() else '❌'}")
    logger.info(f"   Docs          : http://localhost:{settings.APP_PORT}/docs")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
    )
