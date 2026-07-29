"""
EcoWaste AI – Application Entry Point
Mounts FastAPI routes, serves static dashboard files, and launches uAgent runner.
"""
import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from config import HOST, PORT
from api.routes import router as api_router
from services.multi_agent_service import waste_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("==================================================")
    print("  EcoWaste AI Agent Initialized")
    print(f"  Web Dashboard & REST API: http://localhost:{PORT}")
    print(f"  Fetch.ai uAgent Address : {waste_agent.address}")
    print("==================================================")
    yield  # Application runs here

app = FastAPI(
    title="EcoWaste AI Agent",
    description="Intelligent Waste Management, Recycling, Sustainability & Circular Economy Decision Agent using Fetch.ai uAgents Framework",
    version="1.0.0",
    lifespan=lifespan
)

# Include REST API Routes
app.include_router(api_router, prefix="/api")

# Serve Static Web Files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
async def serve_dashboard():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"status": "EcoWaste AI backend running."})

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False)
