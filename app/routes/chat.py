# Import libraries
from flask import Blueprint, Response, render_template, redirect, url_for, stream_with_context, request, session

# Pull in service
from app.services.chat_service import get_chat_response_stream, parse_chat_response, inject_chat_interaction, get_chat_history, manipulate_user_memory, poke_user_memory, initialize_user_memory
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
            # Pull the chat history for the template
            chat_history = get_chat_history(session["user_email"])

            return render_template("chat.html", chat_history=chat_history, styles=styles)

        # Create our generator
        def generate():
            # Flushes headers
            yield b"data: \n\n"

            # start the stream
            for token, chat_response in get_chat_response_stream(user_message, dropdown_value, session["user_email"]):
                # If its a delta
                if token:
                    yield f"data: {token}\n\n".encode("utf-8")
                # If its the full text
                if chat_response:
                    # Parse the result json
                    id, timestamp, response, tokens_used = parse_chat_response(response)

                    # Inject reply into the DB
                    inject_chat_interaction(session["user_email"], id, timestamp, user_message, dropdown_value, response, tokens_used)

                    # If user doesn't have memory, initialize it
                    if not poke_user_memory(session["user_email"]):
                        initialize_user_memory(session["user_email"])

                    # Pull the message and reply into the sender data db
                    manipulate_user_memory(user_message, response, session["user_email"])

                    yield b"data: [DONE]\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"  # VERY IMPORTANT for nginx
            },
            direct_passthrough=True
        )

    if not poke_styles(session["user_email"]):
        initialize_user_styles(session["user_email"])

    # Pull Styles in
    styles = pull_styles(session["user_email"])

    # Pull the chat history for the template
    chat_history = get_chat_history(session["user_email"])

    return render_template("chat.html", chat_history=chat_history, styles=styles)
