# Imports
from flask import Blueprint, render_template, request, jsonify
from app.services.chat_service import get_chat_response

chat_bp = Blueprint("chat", __name__)

# Render the chat page
@chat_bp.route("/", methods=["GET"])
def chat_screen():
    return render_template("chat.html")

# Handle user messages asynchronously
@chat_bp.route("/message", methods=["POST"])
def chat_message():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    ai_response = get_chat_response(user_message)
    return jsonify({"response": ai_response})
