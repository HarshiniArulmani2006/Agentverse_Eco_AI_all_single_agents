from flask import Blueprint, jsonify
from database import db_manager

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    stats = db_manager.get_stats()
    
    top_topics = [
        {"topic": "Climate Change & Global Warming", "searches": 142, "percentage": 32},
        {"topic": "Natural Farming & Composting", "searches": 118, "percentage": 27},
        {"topic": "Water Conservation & Harvesting", "searches": 89, "percentage": 20},
        {"topic": "Plastic & Waste Recycling", "searches": 56, "percentage": 13},
        {"topic": "Renewable Solar & Wind Energy", "searches": 35, "percentage": 8}
    ]

    quiz_stats = {
        "badgesAwarded": {
            "Earth Protector": 24,
            "Green Warrior": 45,
            "Eco Learner": 38,
            "Eco Beginner": 15
        },
        "averageScore": "82%"
    }

    carbon_analytics = {
        "averageCarbonScoreKg": 2840,
        "highImpactPercentage": "22%",
        "moderateImpactPercentage": "58%",
        "lowImpactPercentage": "20%"
    }

    return jsonify({
        "status": "success",
        "metrics": stats,
        "topSearchedTopics": top_topics,
        "quizStats": quiz_stats,
        "carbonAnalytics": carbon_analytics
    })
