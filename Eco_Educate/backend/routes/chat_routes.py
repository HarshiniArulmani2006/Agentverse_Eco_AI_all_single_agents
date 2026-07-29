from flask import Blueprint, request, jsonify
from ai_agent import eco_agent
from database import db_manager

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    language = data.get('language', 'en')

    if not message:
        return jsonify({"error": "Message parameter is required"}), 400

    # Process AI Agent response
    response_data = eco_agent.generate_response(message, language=language)

    # Save to MongoDB chat_history collection
    chat_record = {
        "user_message": message,
        "language": language,
        "agent_response": response_data
    }
    db_manager.insert_record("chat_history", chat_record)

    return jsonify({
        "status": "success",
        "query": message,
        "language": language,
        "response": response_data
    })

@chat_bp.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    history = db_manager.get_records("chat_history", limit=20)
    return jsonify({
        "status": "success",
        "history": history
    })
