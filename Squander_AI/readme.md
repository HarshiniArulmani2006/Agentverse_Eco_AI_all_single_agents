# EcoWaste AI – Intelligent Waste Management, Recycling, Sustainability & Circular Economy Decision Agent

![EcoWaste AI Banner](https://img.shields.io/badge/Fetch.ai-uAgents-22c55e?style=for-the-badge) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-06b6d4?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.10%2B-3b82f6?style=for-the-badge) ![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)

**EcoWaste AI** is an advanced, production-quality AI Agent designed for intelligent waste classification, recycling optimization, carbon footprint estimation, smart bin monitoring, waste generation forecasting, emergency safety alerts, and multi-agent environmental intelligence. Built using the **Fetch.ai AgentVerse (uAgents)** framework and **FastAPI**.

---

## 🌟 Key Features

1. **AI Waste Classification**: Automatically categorizes waste across 12 distinct categories (Plastic, Paper, Glass, Metal, Organic, E-Waste, Hazardous, Biomedical, Construction, Industrial, Agricultural, Mixed) with confidence scoring.
2. **Explainable AI (XAI)**: Every prediction and recommendation provides clear, auditable environmental, recycling, and carbon reasoning.
3. **Recycling Intelligence**: Estimates recycling efficiency, potential upcycled products, step-by-step processing pipelines, and reusable material streams.
4. **Carbon Footprint Estimation**: Compares CO₂e emissions across incineration, landfilling, recycling, and composting, calculating net carbon savings.
5. **Smart Bin Monitoring & Route Optimization**: Monitors live simulated bin fill levels, temperatures, and odor risk; predicts overflow times; and optimizes collection truck routes to save fuel and CO₂.
6. **Waste Generation Forecasting**: Predicts daily (7-day) and monthly (12-month) waste trends with anomaly detection for festival surges and illegal dumping alerts.
7. **Multi-Agent Protocol Integration**: Standardized JSON communication layer designed for seamless inter-agent collaboration with Weather, Air Quality, Carbon Footprint, Water Conservation, Education, and Coordinator Agents.
8. **Interactive Glassmorphism Dashboard**: Modern dark-mode UI with live Chart.js charts, KPI tiles, animated score rings, waste segregation educational game, and conversational AI assistant.
9. **Offline Demo Mode**: Automatic fallback data for seamless offline AI hackathon demonstrations.

---

## 📁 Project Architecture & Folder Structure

```text
waste_management_agent/
├── app/
│   ├── constants.py           # Application metadata & thresholds
│   ├── logger.py              # Structured logging utility
│   └── utils.py               # Input sanitization & mathematical helpers
├── agents/
│   ├── __init__.py            # Agent package exports
│   ├── communication.py       # Inter-agent payload & messaging helpers
│   ├── protocol.py            # uAgents Pydantic message protocol definitions
│   └── waste_agent.py         # Fetch.ai uAgent runner setup
├── ai/
│   ├── __init__.py            # AI engines package exports
│   ├── anomaly_detection.py   # Statistical deviation & pattern anomaly detector
│   ├── confidence_engine.py   # Calibrated confidence scoring
│   ├── decision_engine.py     # Master decision orchestrator
│   ├── explainable_ai.py      # XAI narrative generator
│   └── trend_prediction.py    # Time-series seasonal & growth trend predictor
├── api/
│   ├── __init__.py            # API router package init
│   └── routes.py              # FastAPI REST endpoints
├── data/
│   ├── demo_data.json         # Hackathon demo data
│   ├── recycling_rules.json   # Material recycling rules dataset
│   └── waste_categories.json  # Category metadata & bin configurations
├── models/
│   ├── analytics.py           # Forecast & community Pydantic models
│   ├── smart_bin.py           # Smart bin & route optimization models
│   └── waste.py               # Waste classification & analysis models
├── services/
│   ├── collection_engine.py   # Smart bin network & route optimizer
│   ├── conversational_engine.py # Natural language Q&A engine
│   ├── environmental_engine.py  # Impact assessment & carbon calculator
│   ├── multi_agent_service.py # Standardized JSON payload builder
│   ├── prediction_engine.py   # Waste generation forecaster
│   ├── recycling_engine.py    # Recyclability & upcycling engine
│   ├── risk_engine.py         # Environmental hazard & emergency alert detector
│   ├── sustainability_engine.py # 6-dimensional AI sustainability scorer
│   └── waste_classification_engine.py # Rule-based waste classifier
├── static/
│   ├── css/styles.css         # Glassmorphism dark mode stylesheet
│   ├── js/dashboard.js        # Interactive dashboard & Chart.js integration
│   └── index.html             # Single-page web dashboard
├── tests/
│   ├── test_api.py            # API integration tests
│   ├── test_classification.py # Classification engine tests
│   ├── test_recycling.py      # Recycling engine tests
│   ├── test_risk.py           # Risk assessment tests
│   ├── test_smart_bins.py     # Smart bin monitoring tests
│   └── test_sustainability.py # Sustainability engine tests
├── config.py                  # Global application configuration & environmental variables
├── main.py                    # Entry point: mounts FastAPI & uAgent
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- `pip` package manager

### 2. Installation
Clone or navigate to the repository directory and install dependencies:
```bash
cd waste_management_agent
pip install -r requirements.txt
```

### 3. Running the Agent
Start the FastAPI server and uAgent runner:
```bash
python main.py
```

Output:
```text
==================================================
  EcoWaste AI Agent Initialized
  Web Dashboard & REST API: http://127.0.0.1:8002
  Fetch.ai uAgent Address : agent1q2...
==================================================
```

Open your browser and navigate to:
- **Web Dashboard**: [http://127.0.0.1:8002](http://127.0.0.1:8002)
- **Interactive API Documentation (Swagger)**: [http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs)

---

## 🧪 Running Unit & Integration Tests

Execute all tests using `pytest`:
```bash
pytest tests/ -v
```

---

## 📡 REST API Overview

| Endpoint | Method | Description |
|---|---|---|
| `/api/analyze` | `POST` | Full AI Waste Analysis pipeline (Classification, Carbon, Risk, Sustainability, Multi-Agent Payload) |
| `/api/classify` | `GET` | Quick waste classification & disposal recommendation |
| `/api/smart-bins` | `GET` | Live smart bin monitoring status & route optimization |
| `/api/forecast` | `GET` | Daily and monthly waste generation forecasting & anomaly alerts |
| `/api/sustainability-report` | `GET` | Comprehensive AI Sustainability Report & Eco Badges |
| `/api/query` | `POST` | Natural language Conversational AI Q&A endpoint |
| `/api/multi-agent-payload` | `GET` | Returns standardized multi-agent JSON payload |
| `/api/dashboard-data` | `GET` | Aggregated payload for dashboard initial load |
| `/api/health` | `GET` | Agent health check status |

---

## 🤝 Multi-Agent Protocol Specification

EcoWaste AI emits a standardized JSON payload designed to interoperate with companion environmental agents:
- **Weather Agent**: Recovers temperature/humidity context for odor acceleration and leachate risk.
- **Air Quality Agent**: Triggers AQI alerts if hazardous waste or open burning is detected.
- **Carbon Footprint Agent**: Syncs carbon offset savings into community carbon ledgers.
- **Water Conservation Agent**: Triggers groundwater warnings for toxic waste leachate.
- **Environmental Education Agent**: Dispatches community awareness requests for low recycling rates.
- **Coordinator Agent**: Escalates critical risk alerts and emergency containment requests.

---

## 📜 License

This project is licensed under the MIT License.
