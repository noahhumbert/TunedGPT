# Import libraries
from flask import Blueprint, Response, render_template, redirect, url_for, stream_with_context, request, session

# Pull in service
from app.services.chat_service import get_chat_response_stream, parse_chat_response, inject_chat_interaction, get_chat_history, manipulate_user_memory, poke_user_memory, initialize_user_memory, get_image_generation
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

        # If we aren't dealing with image gen
        if (not dropdown_value=="imagegen"):
            # Create our generator
            def generate():
                for token, chat_response in get_chat_response_stream(user_message, dropdown_value, session["user_email"]):
                    if token:
                        yield token.encode("utf-8")

                    if chat_response:
                        # Parse and store the final response
                        id, timestamp, response_text, tokens_used = parse_chat_response(chat_response)
                        inject_chat_interaction(session["user_email"], id, timestamp, user_message, dropdown_value, response_text, tokens_used)

                        if not poke_user_memory(session["user_email"]):
                            initialize_user_memory(session["user_email"])

                        manipulate_user_memory(user_message, response_text, session["user_email"])

            return Response(
                stream_with_context(generate()),
                mimetype="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no"  # VERY IMPORTANT for nginx
                },
                direct_passthrough=True
            )
        # Else we are generating an image
        else:  
            # Call the api and get needed info
            image_bytes, mimetype = get_image_generation(user_message, dropdown_value, session["user_email"])

            # Return response to the front end
            return Response(
                image_bytes,
                mimetype=mimetype,
                headers={
                    "Cache-Control": "no-store",
                    "Content-Disposition": "inline; filename=generated.png"
                }
            )
        


    if not poke_styles(session["user_email"]):
        initialize_user_styles(session["user_email"])

    # Pull Styles in
    styles = pull_styles(session["user_email"])

    # Pull the chat history for the template
    chat_history = get_chat_history(session["user_email"])

    return render_template("chat.html", chat_history=chat_history, styles=styles)
