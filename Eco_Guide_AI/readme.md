# 🌿 Eco Guide AI (WildGuard Agent)

**Eco Guide AI** is an intelligent, multi-agent AI assistant designed for wildlife conservation, biodiversity tracking, species identification, habitat protection, and ecological education. Powered by Google Gemini 2.0 Flash, RAG (Retrieval-Augmented Generation), and real-time species datasets (IUCN Red List & GBIF).

---

## ✨ Features

- 🔍 **Species Identification & Vision Analysis**: Upload or analyze images to identify flora and fauna, determine conservation status, and view threat details.
- 💬 **Eco-Guide Chat Assistant**: Conversational AI agent answering biodiversity, conservation, and ecosystem management queries.
- 📚 **Interactive Education Module**: Learn about ecosystems, endangered species, threats, and conservation tips with interactive quizzes and structured modules.
- 📍 **Wildlife Sightings & Habitat Tracking**: Report and view wildlife sightings with geographical location integration.
- 🧠 **RAG (Retrieval-Augmented Generation)**: Enhanced knowledge retrieval for accurate ecological facts and species data.

---

## 🏗️ Architecture & Tech Stack

- **Backend**: Python, FastAPI, Google Gemini 2.0 API, RAG Service, IUCN Red List API, GBIF API.
- **Frontend**: HTML5, Vanilla CSS3 (modern glassmorphism UI), JavaScript (ES6+ modular components).
- **Database / Data Storage**: Local JSON storage for species database and community sightings.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Gemini API Key

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd Eco_Guide_AI/backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   Copy `.env.example` to `.env` and insert your API keys:
   ```bash
   cp .env.example .env
   ```
   Set `GEMINI_API_KEY=your_actual_gemini_api_key` in `.env`.

5. Run the FastAPI server:
   ```bash
   python main.py
   ```
   The backend API will run at `http://localhost:8000`.

### Frontend Setup

1. Open `Eco_Guide_AI/frontend/index.html` in your web browser, or serve it using a local HTTP server (e.g., VS Code Live Server or `python -m http.server 3000` inside `frontend/`).

---

## 📁 Repository Structure

```
Eco_Guide_AI/
├── backend/
│   ├── core/           # Config, Gemini client, memory management
│   ├── data/           # Species database & sightings JSON files
│   ├── routers/        # FastAPI endpoint routes
│   ├── services/       # RAG, vision, location, education, sighting services
│   ├── main.py         # App entry point
│   ├── requirements.txt# Python dependencies
│   └── .env.example    # Example configuration environment template
├── frontend/
│   ├── css/            # Stylesheets
│   ├── js/             # Modular JS components (chat, identify, education, etc.)
│   └── index.html      # Main application interface
├── .gitignore          # Git ignore file
└── README.md           # Project documentation
```

---

## 📜 License

Distributed under the MIT License.
