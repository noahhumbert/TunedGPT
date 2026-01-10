# Import libraries
from flask import Blueprint, render_template, request, session, redirect, url_for

# Pull in service
from app.services.chat_service import get_chat_response, parse_chat_response, inject_chat_interaction, cleanup_chat_history, get_chat_history
from app.services.settings_service import poke_styles, initialize_user_styles, pull_styles

chat_bp = Blueprint("chat", __name__)
@chat_bp.route("/", methods=["GET", "POST"])
def chat_screen():
    # If the user isn't logged in, redirect them to login
    if not 'logged_in' in session or ('logged_in' in session and not session['logged_in']):
        return redirect(url_for('login.login_screen'))
        
    # Form submit handling
    if request.method == "POST":
        # Get data from the form
        user_message = request.form.get("message")
        dropdown_value = request.form.get("mode-select") 

        if not user_message:
            chat_history = get_chat_history(session["user_email"])
            return redirect(url_for("chat.chat_screen"))

        # Use the message and model to get a response json
        result = get_chat_response(user_message, dropdown_value, session["user_email"])

        # Parse the result json
        id, timestamp, response, tokens_used = parse_chat_response(result)

        # Inject reply into the DB
        inject_chat_interaction(session["user_email"], id, timestamp, user_message, dropdown_value, response, tokens_used)

        # Cleanup chat DB
        cleanup_chat_history()

        # Pull the chat history for the template
        chat_history = get_chat_history(session["user_email"])

        return redirect(url_for("chat.chat_screen"))

    # Poke Styles
    is_styles = poke_styles(session["user_email"])

    # If there are no styles tied to the email, initialize the styles
    if not is_styles:
        initialize_user_styles(session["user_email"])

    # Pull Styles in
    styles = pull_styles(session["user_email"])

    # Pull the chat history for the template
    chat_history = get_chat_history(session["user_email"])

    return render_template("chat.html", chat_history=chat_history, styles=styles)
