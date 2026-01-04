from flask import Blueprint, render_template, request, jsonify
from app.services.chat_service import get_chat_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["GET"])
def chat_screen():
    # Just render the chat template
    return render_template("chat.html")

@chat_bp.route("/chat/message", methods=["POST"])
def chat_message():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call your AI service
    ai_response = get_chat_response(user_message)
    
    return jsonify({"response": ai_response})
