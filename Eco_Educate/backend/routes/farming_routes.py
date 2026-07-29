from flask import Blueprint, request, jsonify
from database import db_manager
from ai_agent import eco_agent

farming_bp = Blueprint('farming', __name__)

FARMING_PRESET_GUIDES = {
    "tomatoes": {
        "crop": "Tomatoes",
        "soilRequirements": "Well-drained loamy soil rich in organic matter (pH 6.0 - 6.8). Add bio-char or aged compost.",
        "organicFertilizer": "Apply Jeevamrutham liquid tonic every 14 days near root zone. Top dress with vermicompost during flowering.",
        "naturalPesticides": "Neem Oil Spray (5ml neem oil + 2ml liquid soap/liter). Spray Agniastra for severe caterpillars or stem borers.",
        "waterRequirements": "Deep watering twice a week at root level (avoid soaking foliage to prevent leaf blight). Maintain 2-inch organic dry straw mulch.",
        "seasonalGuidance": "Sow in early spring/warm months. Provide wooden stakes or bamboo trellises for upright vine support."
    },
    "compost": {
        "topic": "Home Composting Guide",
        "method": "Aerobic Layering Method (3 Browns : 1 Green)",
        "browns": "Dry leaves, cardboard scraps, sawdust, dry twigs (Carbon sources)",
        "greens": "Vegetable peels, fruit scraps, coffee grounds, fresh grass trimmings (Nitrogen sources)",
        "process": [
            "Start with a 4-inch bottom layer of coarse twigs for ventilation.",
            "Alternate layers of brown dry leaves and green kitchen scraps.",
            "Keep moist like a wrung-out sponge; stir/turn every 7-10 days to aerate.",
            "Rich black humus is ready in 45-60 days with zero foul odor!"
        ]
    },
    "pest_control": {
        "topic": "Natural Pest Control Recipes",
        "recipes": [
            {
                "name": "Neem Oil Bio-Spray",
                "ingredients": "5ml Cold-pressed Neem oil + 2ml organic soap + 1L warm water",
                "target": "Aphids, whiteflies, thrips, spider mites, mealybugs"
            },
            {
                "name": "Jeevamrutham Soil Microbe Booster",
                "ingredients": "Cow dung, cow urine, jaggery, pulse flour, soil & water fermented 48 hours",
                "target": "Restores soil microbial flora, prevents root rot and wilt fungal diseases"
            },
            {
                "name": "Sour Buttermilk Spray",
                "ingredients": "100ml fermented sour buttermilk diluted in 1L water",
                "target": "Effective natural fungicide against powdery mildew and leaf curl virus"
            }
        ]
    }
}

@farming_bp.route('/api/farming/preset/<topic_key>', methods=['GET'])
def get_farming_preset(topic_key):
    preset = FARMING_PRESET_GUIDES.get(topic_key)
    if not preset:
        return jsonify({"error": "Preset guide not found"}), 404
    return jsonify({
        "status": "success",
        "guide": preset
    })

@farming_bp.route('/api/farming/query', methods=['POST'])
def farming_query():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    language = data.get('language', 'en')

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Custom farming response generation using EcoGuide AI Agent
    agent_res = eco_agent.generate_response(query, language=language)

    record = {
        "query": query,
        "language": language,
        "recommendation": agent_res
    }
    db_manager.insert_record("farming_queries", record)

    return jsonify({
        "status": "success",
        "query": query,
        "language": language,
        "advice": agent_res
    })
