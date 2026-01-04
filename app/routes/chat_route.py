from flask import Blueprint, render_template, request, jsonify
from app.services.chat_service import get_chat_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["GET", "POST"])
def chat_screen():
    if request.method == "POST":
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        ai_response = get_chat_response(user_message)
        return jsonify({"response": ai_response})

    # GET request just renders the page
    return render_template("chat.html")
