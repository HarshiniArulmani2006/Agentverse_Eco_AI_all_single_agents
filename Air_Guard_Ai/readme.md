# AirGuard AI – Intelligent Air Quality Monitoring, Health Advisory & Environmental Intelligence Agent

[![Fetch.ai uAgents](https://img.shields.io/badge/Fetch.ai-uAgents_Framework-purple.svg)](https://fetch.ai/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-emerald.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**AirGuard AI** is a production-grade AI-powered Air Quality Agent built using the **Fetch.ai AgentVerse (uAgents)** framework, **FastAPI**, and **Open-Meteo Air Quality & Geocoding APIs** (no API key required).

It provides real-time air quality monitoring, AI pollution pattern detection, demographic health risk prediction, dynamic risk scoring (0-100), outdoor activity suitability analysis, WHO guideline compliance checking, pollution trend forecasting, environmental intelligence, emergency alert generation, multi-city comparison, conversational Q&A, and standardized multi-agent JSON communication format.

---

## 🌟 Key Features

1. **Open-Meteo API Integration**:
   - Automatic City-to-Coordinates resolution via Open-Meteo Geocoding API with location caching.
   - Satellite & ground telemetry retrieval (US AQI, PM2.5, PM10, CO, NO₂, SO₂, O₃, Aerosol Optical Depth, Dust, UV Index).

2. **AI Pollution Pattern & Source Detection**:
   - Detects Industrial Pollution, Traffic Pollution, Smog, Dust Storms, Wildfire Smoke, and Construction Dust with confidence probabilities.
   - Estimates likely emission sources (Vehicle Emissions, Industrial Facilities, Garbage Burning, Crop Burning, Forest Fires, Power Plants).

3. **Demographic Health Risk Prediction**:
   - Tailored risk predictions and recommendations for 8 groups: Children, Elderly, Pregnant Women, Asthma Patients, COPD Patients, Heart Patients, Outdoor Workers, Athletes.

4. **Dynamic Risk Score (0-100)**:
   - Weighted risk score with classifications: Excellent, Good, Moderate, Poor, Unhealthy, Hazardous, Emergency.

5. **Smart Outdoor Activity Analyzer**:
   - Evaluates suitability for 12 activities: Walking, Running, Cycling, Cricket, Football, Hiking, Trekking, Camping, Picnic, Photography, Drone Flying, Morning Yoga.

6. **WHO Standards Compliance**:
   - Evaluates pollutant levels against WHO 2026 guidelines (Safe, Above WHO Limit, Critical, Dangerous).

7. **Pollution Trend Forecasting & Anomaly Detection**:
   - Next Hour, Next 6 Hours, Tomorrow, Next 3 Days, Next 7 Days trends (Improving, Stable, Worsening).
   - Automatic detection of sudden particulate spikes.

8. **Environmental Intelligence**:
   - Explains impact on Agriculture, Solar/Wind Energy, Wildlife, Human Health, Water Bodies, Climate Change, Electricity Grid Demand.

9. **Conversational AI Q&A Assistant**:
   - Natural language query parser ("Should I wear a mask?", "Can I go jogging?", "Can children play outside?", etc.).

10. **Multi-Agent Inter-Agent Communication**:
    - Generates standardized JSON payload for seamless integration with Weather Agent, Waste Management Agent, Carbon Footprint Agent, Water Conservation Agent, Environmental Education Agent, and Coordinator Agent.

11. **Modern Glassmorphic Interactive Dashboard**:
    - Dark mode UI with Chart.js visualization, Lucide icons, live search, multi-city ranking modal, and PDF report export.

---

## 🏗 Project Architecture

```text
Air_quality_agent/
├── config.py                   # App parameters, WHO thresholds, API endpoints
├── main.py                     # Entry point (FastAPI app + uAgent initialization)
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── services/
│   ├── geocoding_service.py    # City to Lat/Lon conversion with TTL caching
│   ├── air_quality_service.py  # Open-Meteo Air Quality API fetcher
│   ├── analysis_engine.py     # AI pollution signature & source detection
│   ├── health_engine.py       # Demographic risk predictions & advisories
│   ├── activity_engine.py     # Outdoor activity suitability analyzer
│   ├── forecast_engine.py     # Pollution trends, anomaly detection & analytics
│   ├── green_engine.py        # Environmental scores, green suggestions & carbon metric
│   ├── conversational_engine.py # Natural language Q&A handler
│   └── multi_agent_service.py # uAgents protocol & JSON payload builder
├── api/
│   └── routes.py               # REST API endpoints
├── static/
│   ├── index.html              # Dashboard HTML template
│   ├── css/style.css           # Premium dark theme glassmorphism CSS
│   └── js/
│       ├── app.js              # Application logic & DOM rendering
│       └── charts.js           # Chart.js graphs
└── tests/                      # Pytest unit & integration test suite
```

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python main.py
```

### 3. Open Web Dashboard
Open your browser and visit:
```text
http://localhost:8000
```

---

## 🧪 Running Automated Tests

Run the full pytest suite:
```bash
pytest
```

---

## 🤖 Multi-Agent Interoperability JSON Payload Example

```json
{
  "sender_agent": "AirGuard_AI_Agent",
  "target_agents": [
    "WeatherAgent",
    "WasteManagementAgent",
    "CarbonFootprintAgent",
    "WaterConservationAgent",
    "CoordinatorAgent"
  ],
  "timestamp": 1774624488.5,
  "location": "Delhi",
  "AQI": 160.0,
  "risk_score": 74.2,
  "health_score": 45.0,
  "dominant_pollution_pattern": "Traffic Pollution",
  "emergency_alerts": [],
  "actionable_triggers": {
    "water_sprinklers_needed": true,
    "traffic_reroute_recommended": true,
    "public_health_warning_active": true
  }
}
```

---

## 📄 License
This project is licensed under the MIT License.
