"""
WeatherWise AI - FastAPI Web Server & API Gateway
Exposes web endpoints and serves the interactive dashboard UI.
"""

import os
import logging
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.weather_agent import execute_weather_analysis
from models.schema import WeatherQueryRequest

logger = logging.getLogger("WeatherWise.WebServer")

app = FastAPI(
    title="WeatherWise AI - Intelligent Weather Decision Agent",
    description="AgentVerse uAgents powered environmental weather analysis, risk scoring, and smart decision engine.",
    version="1.0.0"
)

# Enable CORS for frontend interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get current script path for mounting static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class NaturalLanguageQueryPayload(BaseModel):
    city: str = "Coimbatore"
    latitude: float = None
    longitude: float = None
    question: str = None


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serves the main WeatherWise interactive dashboard HTML."""
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Dashboard index.html not found.")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/weather")
async def get_weather(
    city: str = Query("Coimbatore", description="City name to search"),
    lat: float = Query(None, description="Optional latitude"),
    lon: float = Query(None, description="Optional longitude"),
    question: str = Query(None, description="Optional conversational question")
):
    """
    REST API endpoint executing live weather retrieval, risk scoring, recommendations,
    and decision synthesis.
    """
    response = execute_weather_analysis(city=city, lat=lat, lon=lon, question=question)
    return JSONResponse(content=response.model_dump())


@app.post("/api/ask")
async def ask_decision_engine(payload: NaturalLanguageQueryPayload):
    """
    REST API endpoint for conversational smart decision engine queries.
    """
    response = execute_weather_analysis(
        city=payload.city,
        lat=payload.latitude,
        lon=payload.longitude,
        question=payload.question
    )
    return JSONResponse(content=response.model_dump())


@app.get("/api/health")
async def health_check():
    """System health check endpoint."""
    return {"status": "healthy", "service": "WeatherWise AI Agent", "uagents_protocol": "WeatherWiseProtocol/1.0.0"}
