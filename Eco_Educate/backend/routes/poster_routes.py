import random
from flask import Blueprint, request, jsonify

poster_bp = Blueprint('poster', __name__)

POSTER_SLOGANS = {
    "climate": [
        "Act Before the Ice Melts – Save Our Common Home!",
        "Small Steps Today, A Greener Tomorrow",
        "Stop Climate Change Before It Changes Everything",
        "Turn Down the Heat: Choose Clean Renewable Energy",
        "The Earth Doesn't Belong to Us, We Belong to Earth"
    ],
    "pollution": [
        "Refuse Plastic, Save Our Ocean Fantastic!",
        "Clean Air is Not a Luxury – It is Life",
        "Be Part of the Solution, Not the Pollution",
        "Recycle Today for a Breathable Tomorrow",
        "Say NO to Single-Use Plastic, YES to Future Life"
    ],
    "farming": [
        "Heal the Soil, Nourish the Soul – Go Natural!",
        "Zero Chemical Farming, 100% Pure Harvest",
        "Feed the Soil Microbes, Soil Will Feed You",
        "Protect Earthworms: Nature’s Master Farmers",
        "Jeevamrutham Soil Power – Biological Farming Revolution"
    ],
    "biodiversity": [
        "Every Species Matters – Protect Wildlife Diversity",
        "Plant Native Trees, Welcome Wild Bees",
        "When Forest Thrives, Humanity Survives",
        "Save Habitats, Protect Life on Earth",
        "Biodiversity is the Key to Planetary Balance"
    ]
}

POSTER_THEMES = [
    {"id": "emerald-forest", "name": "Emerald Forest", "primaryColor": "#1b4332", "accentColor": "#52b788", "bgGradient": "from-emerald-950 via-forest-900 to-green-950", "textColor": "#ffffff"},
    {"id": "ocean-blue", "name": "Ocean Cleanse", "primaryColor": "#03045e", "accentColor": "#00b4d8", "bgGradient": "from-slate-950 via-sky-950 to-cyan-950", "textColor": "#ffffff"},
    {"id": "earth-harvest", "name": "Warm Earth", "primaryColor": "#582f0e", "accentColor": "#ddbea9", "bgGradient": "from-amber-950 via-stone-900 to-yellow-950", "textColor": "#ffffff"},
    {"id": "solar-glow", "name": "Solar Dawn", "primaryColor": "#78290f", "accentColor": "#ffb703", "bgGradient": "from-orange-950 via-amber-900 to-yellow-900", "textColor": "#ffffff"},
    {"id": "botanical-bloom", "name": "Botanical Garden", "primaryColor": "#2d6a4f", "accentColor": "#b7e4c7", "bgGradient": "from-teal-950 via-emerald-900 to-green-900", "textColor": "#ffffff"},
    {"id": "neon-eco", "name": "Cyber Green", "primaryColor": "#0d1b2a", "accentColor": "#00ff87", "bgGradient": "from-black via-slate-950 to-emerald-950", "textColor": "#00ff87"},
    {"id": "midnight-canopy", "name": "Midnight Forest", "primaryColor": "#10002b", "accentColor": "#e0aaff", "bgGradient": "from-violet-950 via-indigo-950 to-slate-950", "textColor": "#ffffff"},
    {"id": "sunset-radiance", "name": "Sunset Eco", "primaryColor": "#6b705c", "accentColor": "#ffe8d6", "bgGradient": "from-rose-950 via-amber-950 to-stone-950", "textColor": "#ffffff"}
]

@poster_bp.route('/api/poster/generate', methods=['POST'])
def generate_poster():
    data = request.get_json() or {}
    category = data.get('category', 'climate')
    custom_title = data.get('customTitle', '').strip()
    theme_id = data.get('theme', 'emerald-forest')
    layout_style = data.get('layoutStyle', 'centered')

    slogans = POSTER_SLOGANS.get(category, POSTER_SLOGANS["climate"])
    chosen_slogan = random.choice(slogans)

    theme = next((t for t in POSTER_THEMES if t['id'] == theme_id), POSTER_THEMES[0])

    title = custom_title if custom_title else f"Protect Earth: {category.title()}"

    poster_data = {
        "title": title,
        "slogan": chosen_slogan,
        "category": category,
        "theme": theme,
        "layoutStyle": layout_style,
        "tip": "Share this awareness poster to inspire eco-friendly habits in your community!",
        "callToAction": "Join the EcoGuide AI Green Movement Today"
    }

    return jsonify({
        "status": "success",
        "poster": poster_data
    })
