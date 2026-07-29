import os
import random
import logging
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config

# Import Blueprints
from routes.chat_routes import chat_bp
from routes.quiz_routes import quiz_bp
from routes.carbon_routes import carbon_bp
from routes.learn_routes import learn_bp
from routes.farming_routes import farming_bp
from routes.dashboard_routes import dashboard_bp
from routes.poster_routes import poster_bp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="../frontend/dist", static_url_path="")
CORS(app)

# Register Blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(carbon_bp)
app.register_blueprint(learn_bp)
app.register_blueprint(farming_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(poster_bp)

# Daily Eco Tips Pool
DAILY_ECO_TIPS = [
    {"id": 1, "tip": "Turning off the faucet while brushing teeth saves up to 8 gallons (30 liters) of water every single day!", "category": "Water"},
    {"id": 2, "tip": "A mature leafy tree produces enough oxygen for 2 to 10 human beings each year while trapping air toxins.", "category": "Trees"},
    {"id": 3, "tip": "Composting vegetable kitchen waste prevents methane emissions in landfills and builds fertile living soil.", "category": "Waste"},
    {"id": 4, "tip": "Replacing traditional incandescent bulbs with LED lights consumes up to 80% less energy and lasts 25x longer.", "category": "Energy"},
    {"id": 5, "tip": "Using cold water for laundry saves roughly 90% of the energy consumed by a washing machine cycle.", "category": "Lifestyle"},
    {"id": 6, "tip": "Jeevamrutham bio-tonic multiplies beneficial soil bacteria from 10 thousand to over 10 million in just 48 hours!", "category": "Farming"}
]

# Random Environmental Facts Pool
ENVIRONMENTAL_FACTS = [
    "Over 1 million species of plants and animals are currently threatened with extinction worldwide.",
    "Plastic bags take between 500 and 1,000 years to decompose in landfill environments.",
    "Swapping 1 burger per week for a plant-based meal saves the equivalent emissions of driving 350 miles.",
    "Global renewable energy capacity grew by a record 50% in 2023, driven primarily by solar PV adoption.",
    "Over 50% of modern prescription medicines originate from naturally occurring plant and fungal compounds.",
    "Drip irrigation systems cut agricultural water wastage by up to 80% compared to traditional surface flooding."
]

@app.route('/api/daily-tip', methods=['GET'])
def get_daily_tip():
    # Pick daily tip based on current day of year
    day_idx = random.randint(0, len(DAILY_ECO_TIPS) - 1)
    return jsonify({
        "status": "success",
        "tip": DAILY_ECO_TIPS[day_idx]
    })

@app.route('/api/random-fact', methods=['GET'])
def get_random_fact():
    fact = random.choice(ENVIRONMENTAL_FACTS)
    return jsonify({
        "status": "success",
        "fact": fact
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "EcoGuide AI Backend",
        "version": "1.0.0"
    })

# Serve static frontend build files in production mode
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    logger.info(f"Starting EcoGuide AI Backend Server on port {Config.PORT}...")
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
