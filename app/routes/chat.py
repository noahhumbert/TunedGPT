from flask import Blueprint, render_template, request, jsonify
from app.services.chat_service import get_chat_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["GET", "POST"])
def chat_screen():
    if request.method == "POST":
        # Get data from the form
        user_message = request.form.get("message")
        dropdown_value = request.form.get("mode-select") 

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # ai_response = get_chat_response(user_message, dropdown_value)

        print(user_message, dropdown_value)

    return render_template("chat.html")
