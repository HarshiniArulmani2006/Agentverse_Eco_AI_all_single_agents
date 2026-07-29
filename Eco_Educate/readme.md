# EcoGuide AI: Intelligent Environmental Education & Natural Farming Assistant Platform

![EcoGuide AI Banner](https://img.shields.io/badge/EcoGuide%20AI-v1.0.0-emerald?style=for-the-badge&logo=leaf)
![Groq RAG](https://img.shields.io/badge/AI%20Engine-Groq%20Llama%203.3-blue?style=for-the-badge)
![Stack](https://img.shields.io/badge/Stack-React%20%7C%20Flask%20%7C%20MongoDB-green?style=for-the-badge)

**EcoGuide AI** is an intelligent full-stack environmental education and zero-chemical natural farming advisor platform. It educates citizens about global environmental challenges, climate mitigation, pollution control, biodiversity conservation, sustainable water practices, and organic agricultural techniques through conversational RAG AI.

---

## 🌟 Core Features & Modules

1. **AI Environmental Mentor (`/chat`)**:
   - ChatGPT-style interface with structured responses: **Answer**, **Environmental Tip**, and **Action Step**.
   - Powered by Retrieval-Augmented Generation (RAG) over detailed environmental domain text files.
   - **Multilingual Support**: Seamless toggle between English and Tamil (தமிழ்).
   - **Hands-Free Voice Support**: Speech-to-Text query dictation and Text-to-Speech audio response reading.

2. **Interactive Learning Hub (`/learn`)**:
   - Deep-dive educational modules covering: *Climate Change*, *Global Warming*, *Pollution*, *Biodiversity*, *Renewable Energy*, *Water Conservation*, and *Sustainable Living*.
   - Each module contains Definitions, Primary Causes, Ecological Impacts, Prevention Strategies, and Case Studies.

3. **Zero-Chemical Natural Farming Advisor (`/farming`)**:
   - Dedicated agricultural advisor for chemical-free farming.
   - Complete guides for growing tomatoes naturally, making aerobic compost, and preparing organic formulations like **Jeevamrutham** and **Neem Bio-sprays**.

4. **Dynamic Eco Quiz (`/quiz`)**:
   - Interactive multiple-choice quizzes with instant evaluation and progress tracking.
   - Awards tier badges: *Eco Beginner*, *Eco Learner*, *Green Warrior*, and *Earth Protector*.

5. **Carbon Footprint Calculator (`/carbon`)**:
   - Evaluates daily travel distance, transport mode, monthly electricity kWh, and weekly single-use plastics.
   - Generates annual CO₂e score, impact rating, and personalized carbon reduction plans.

6. **Awareness Poster Generator (`/poster`)**:
   - Generates environmental awareness slogans and visual theme templates for school/workplace eco campaigns.

7. **System Analytics Dashboard (`/dashboard`)**:
   - Live metrics display: total users, questions asked, top searched topics, quiz badge distribution, and carbon analytics.

---

## 📁 Project Folder Structure

```
EcoGuide-AI/
├── backend/
│   ├── app.py                      # Flask Server Entry Point
│   ├── config.py                   # Environment Configuration
│   ├── database.py                 # MongoDB Manager with Resilient Fallback
│   ├── ai_agent.py                 # Groq Llama 3 AI Agent & RAG Synthesizer
│   ├── rag_engine.py               # TF-IDF Knowledge Retrieval Engine
│   ├── requirements.txt            # Python Dependencies
│   └── routes/
│       ├── chat_routes.py          # /api/chat & /api/chat/history
│       ├── quiz_routes.py          # /api/quiz/questions & /api/quiz/submit
│       ├── carbon_routes.py        # /api/carbon-calculator
│       ├── learn_routes.py         # /api/learn/topics
│       ├── farming_routes.py       # /api/farming/query & presets
│       ├── dashboard_routes.py     # /api/dashboard/stats
│       └── poster_routes.py        # /api/poster/generate
├── frontend/
│   ├── index.html                  # HTML5 Entry Point with SEO Meta Tags
│   ├── package.json                # Frontend Node Dependencies
│   ├── vite.config.js              # Vite & API Proxy Config
│   ├── tailwind.config.js          # Forest Green Eco Design Tokens
│   ├── postcss.config.js           # PostCSS Config
│   └── src/
│       ├── main.jsx
│       ├── App.jsx                 # React Router Shell
│       ├── index.css               # Global Tailwind Styles
│       ├── components/
│       │   ├── Navbar.jsx          # Glassmorphic Header & Language Toggle
│       │   ├── Footer.jsx          # Footer & Random Eco Fact Banner
│       │   └── DailyTipModal.jsx   # Top Notification Daily Eco Tip
│       ├── pages/
│       │   ├── Home.jsx            # Hero, Mission, Topic Cards
│       │   ├── Chat.jsx            # AI Chat UI with Speech & Tamil Support
│       │   ├── Learn.jsx           # Interactive Learning Drawer
│       │   ├── NaturalFarming.jsx  # Crop Care & Organic Bio-sprays
│       │   ├── Quiz.jsx            # Dynamic Quiz & Badge Awards
│       │   ├── CarbonCalculator.jsx# Slider Footprint Calculator
│       │   ├── PosterGenerator.jsx # Awareness Poster Designer
│       │   └── Dashboard.jsx       # Analytics Charts
│       └── utils/
│           ├── api.js              # Axios API Client with Client Fallbacks
│           └── translations.js     # English & Tamil UI Strings
├── knowledge_base/
│   ├── climate.txt                 # Climate Change Knowledge Base
│   ├── pollution.txt               # Air, Water, Soil, Noise Pollution KB
│   ├── biodiversity.txt            # Ecosystems & Species Conservation KB
│   ├── natural_farming.txt         # Chemical-free Agriculture & Formulations
│   ├── renewable_energy.txt        # Solar, Wind, Grid Clean Tech KB
│   └── water_conservation.txt      # Rainwater Harvesting & Drip Irrigation KB
├── .env.example                    # Template Environment Variables
├── requirements.txt                # Root Requirements File
├── vercel.json                     # Vercel Deployment File
├── render.yaml                     # Render Backend Service Configuration
└── README.md                       # Complete Project Documentation
```

---

## ⚡ Quick Start & Installation

### 1. Prerequisites
- Python 3.10+ installed
- Node.js 18+ and npm installed
- MongoDB installed locally OR a free MongoDB Atlas cluster connection string.
- *(Optional)* Free Groq API Key from [console.groq.com](https://console.groq.com).

### 2. Backend Setup
```bash
# Navigate to backend folder
cd backend

# Create virtual environment (optional)
python -m venv venv
# Activate on Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy ..\.env.example .env

# Run Flask backend server
python app.py
```
Backend will start at `http://localhost:5000`.

### 3. Frontend Setup
```bash
# Navigate to frontend folder
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```
Frontend will start at `http://localhost:3000`.

---

## 🔒 Environment Variables Configuration

Create a `.env` file in the `backend/` directory:
```env
PORT=5000
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/ecoguide_db
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

## 🗄️ MongoDB Collections Schema

The system manages the following collections:
- `users`: User profiles and registration metadata.
- `chat_history`: Message query strings, selected language, and structured AI response.
- `quiz_results`: User name, raw score, percentage score, and badge unlocked.
- `environment_topics`: Educational domain records and search hits.
- `carbon_calculations`: Daily travel, kWh usage, plastic count, CO₂ score, and impact rating.
- `farming_queries`: Agricultural questions and custom organic advisory output.

---

## 🌐 Deployment Instructions

### Frontend (Vercel)
1. Push repository to GitHub.
2. Import project into Vercel dashboard.
3. Set root directory to `frontend`.
4. Build Command: `npm run build` | Output Directory: `dist`.
5. Deploy!

### Backend (Render)
1. Connect repository to Render.
2. Select **Web Service** with runtime `Python 3`.
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn --chdir backend app:app`
5. Add Environment Variables: `MONGO_URI` and `GROQ_API_KEY`.
6. Deploy!
