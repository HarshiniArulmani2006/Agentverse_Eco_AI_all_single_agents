# WeatherWise AI – Intelligent Weather Decision Agent 🌤️⚡

> **Built with Fetch.ai AgentVerse (uAgents Framework) and Open-Meteo APIs.**

**WeatherWise AI** is an advanced, production-grade AI Weather Agent designed using the Fetch.ai `uagents` framework. Beyond simply displaying weather values, WeatherWise retrieves live environmental telemetry, computes a dynamic **0–100 Weather Risk Score**, generates **Emergency Safety Alerts**, evaluates suitability for **9 Outdoor Activities**, predicts **Environmental & Renewable Energy Impacts**, and powers a **Smart Conversational Decision Engine**.

Designed with clean modular architecture, WeatherWise exports standardized JSON telemetry payloads compatible with future multi-agent environmental systems (Air Quality Agent, Waste Management Agent, Carbon Footprint Agent, Water Conservation Agent, and Coordinator Agent).

---

## 🌟 Core Features

### 1. Multi-Format Input & Geocoding
- Accepts **City Name** (e.g., *Coimbatore*, *London*, *Tokyo*) or direct **Latitude & Longitude** coordinates.
- Automatic city-to-coordinate conversion powered by **Open-Meteo Geocoding API** with in-memory caching.

### 2. Live Weather Telemetry (Open-Meteo API)
Retrieves 13+ real-time metrics without requiring any API key:
- Current Temperature & Apparent Feels-Like Temperature (°C)
- Relative Humidity (%)
- Wind Speed (km/h) & Wind Direction (°)
- Weather Condition Description (WMO Code Translator)
- Rain Probability (%) & Cloud Cover (%)
- Atmospheric Pressure (hPa) & Visibility (m)
- UV Index (0–12+)
- Sunrise & Sunset Times

### 3. AI Weather Analysis & Risk Engine (0–100 Score)
Evaluates composite risk across temperature extremities, severe downpours, gale winds, thunderstorms, dense fog, and UV radiation:
- **0 – 25**: `LOW` Risk Level
- **26 – 50**: `MEDIUM` Risk Level
- **51 – 75**: `HIGH` Risk Level
- **76 – 100**: `CRITICAL` Risk Level

**Emergency Alerts**: Automatically detects Heatwaves, Torrential Rain/Floods, Cyclones, Thunderstorms, Dense Fog, and Freezing conditions with actionable safety advice.

### 4. Personalized Recommendations
- **Clothing Advice**: Cotton/linen, jackets, umbrellas, waterproof footwear, UV gear, thermal layers.
- **Travel Safety**: Road conditions, fog headlight recommendations, braking distance warnings, traffic delay forecasts.
- **Health Guidance**: Hydration alerts, peak sun exposure warnings, dry air skin care.
- **9 Outdoor Activities Evaluation**: Suitability ratings (EXCELLENT, GOOD, CAUTION, UNSUITABLE) and scores for **Walking**, **Cycling**, **Running**, **Cricket**, **Football**, **Hiking**, **Trekking**, **Camping**, and **Picnics**.

### 5. Environmental Intelligence
- **Solar PV Potential**: Evaluates cloud cover & solar irradiance.
- **Wind Energy Potential**: Evaluates wind turbine velocity thresholds.
- **Agricultural Irrigation Needs**: Detects rainfall to suspend unnecessary municipal/farm irrigation.
- **Power Grid Cooling Load**: Predicts electricity demand surges during heatwaves.
- **Wildfire Risk Assessment**: Multi-factor humidity, temperature, and wind speed evaluation.

### 6. Conversational AI & Smart Decision Engine
Understands natural language questions such as:
- *"Will it rain today?"*
- *"Should I carry an umbrella?"*
- *"Can I go for a bike ride?"*
- *"I'm planning a picnic tomorrow."*
- *"Can I wash clothes today?"*
- *"Is today suitable for farming?"*
- *"What should I wear today?"*
- *"Is tomorrow better than today?"*

### 7. Multi-Agent System Protocol Export
Generates structured JSON payloads with standard headers (`sender_agent`, `target_agents`, `actionable_triggers`) ready to communicate with Air Quality, Carbon Footprint, Water Conservation, and Coordinator Agents.

---

## 🛠️ Project Structure

```
Eco_agent/
├── config.py                     # System settings & Open-Meteo endpoints
├── main.py                       # CLI & Web Server entry point
├── agentverse_entry.py           # Standalone AgentVerse IDE script (single file)
├── requirements.txt              # Project dependencies
├── models/
│   ├── __init__.py
│   └── schema.py                 # Pydantic & uAgents message models
├── services/
│   ├── __init__.py
│   ├── geocoding.py             # Open-Meteo Geocoding API service & cache
│   └── open_meteo.py             # Open-Meteo Weather API & 7-day forecast parser
├── engine/
│   ├── __init__.py
│   ├── risk_analyzer.py          # 0-100 Weather Risk Engine & Emergency Alerts
│   ├── recommendation_engine.py  # Clothing, Travel, Health & 9 Activity Evaluator
│   ├── environmental_engine.py   # Renewable energy, Agriculture & Wildfire analysis
│   └── decision_engine.py        # Conversational AI & Decision Synthesizer
├── agents/
│   ├── __init__.py
│   └── weather_agent.py          # Fetch.ai uAgents Protocol & Agent node
├── web/
│   ├── __init__.py
│   ├── server.py                 # FastAPI web server
│   ├── static/
│   │   ├── style.css             # Glassmorphism dark mode CSS
│   │   └── app.js                # Frontend interactivity & real-time REST client
│   └── templates/
│       └── index.html            # Interactive Web Dashboard UI
└── tests/
    └── test_weather_agent.py     # System test suite
```

---

## 🚀 Quick Start Guide

### 1. Installation & Environment Setup

```bash
# Clone repository or navigate to workspace
cd Eco_agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Launch Interactive Web Dashboard

Run the FastAPI web server to launch the visual dashboard on `http://127.0.0.1:8080`:

```bash
python main.py --mode web
```

Open your web browser and navigate to **`http://127.0.0.1:8080`**.

---

### 3. Run Standalone Fetch.ai uAgent Node

Run the agent node to start listening on native P2P uAgents message protocols:

```bash
python main.py --mode agent
```

---

### 4. Run Automated Test Suite

Verify all components (geocoding, risk scoring, recommendations, smart decision engine, multi-agent protocol):

```bash
python main.py --mode test
```

---

## 🌐 Deploying to Fetch.ai AgentVerse

1. Go to **[AgentVerse.ai](https://agentverse.ai)** and log into your account.
2. Create a new Agent.
3. Open **`agentverse_entry.py`** from this repository.
4. Copy the entire contents of `agentverse_entry.py` and paste it into the AgentVerse Code Editor.
5. Click **Submit & Run Agent**.

---

## 📄 Example Multi-Agent JSON Response Structure

```json
{
  "success": true,
  "timestamp": "2026-07-27T19:30:00Z",
  "location": "Coimbatore",
  "latitude": 11.0168,
  "longitude": 76.9558,
  "metrics": {
    "temperature_c": 31.0,
    "feels_like_c": 33.5,
    "relative_humidity": 68,
    "wind_speed_kmh": 12.0,
    "weather_condition": "Partly Cloudy",
    "rain_probability": 20,
    "uv_index": 7.2
  },
  "risk_analysis": {
    "risk_score": 18,
    "risk_level": "LOW",
    "primary_reason": "Comfortable temperature, calm winds, low rain probability.",
    "detected_conditions": ["Pleasant Weather"],
    "emergency_alerts": []
  },
  "recommendations": {
    "clothing": ["Wear light-colored cotton clothes", "Carry sunglasses"],
    "travel_advice": "Safe for travel",
    "health_advice": ["Stay hydrated throughout the day."],
    "outdoor_activities": [
      {
        "activity_name": "Cycling",
        "suitable": true,
        "status": "EXCELLENT",
        "suitability_score": 90,
        "reason": "Ideal environmental conditions for cycling."
      }
    ]
  },
  "environmental_intelligence": {
    "solar_power_potential": "HIGH",
    "wind_energy_potential": "MODERATE",
    "irrigation_need": "MODERATE",
    "wildfire_risk": "LOW"
  },
  "multi_agent_payload": {
    "header": {
      "sender_agent": "WeatherWise_AI_Agent",
      "target_agents": [
        "AirQualityAgent",
        "WasteManagementAgent",
        "CarbonFootprintAgent",
        "WaterConservationAgent",
        "EnvironmentalEducationAgent",
        "CoordinatorAgent"
      ],
      "protocol_version": "1.0.0"
    },
    "actionable_triggers": ["MAXIMIZE_SOLAR_GRID_DISPATCH"]
  }
}
```

---

## 📜 License & Credits

Built for the Fetch.ai AgentVerse Hackathon. Powered by **Fetch.ai uAgents** and **Open-Meteo**.
