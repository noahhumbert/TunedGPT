# Import libraries
from flask import Blueprint, render_template, request, session, redirect, url_for

# Pull in service
from app.services.login_service import authenticate

login_bp = Blueprint("login", __name__)
@login_bp.route("/login", methods=["GET", "POST"])
def login_screen():
    # Error debugging
    error = None
    debug = {}

    # If the user is logged in, redirect them to chat
    if 'logged_in' in session:
        return redirect(url_for('chat.chat_screen'))
    
    # On form submit
    if request.method == 'POST':
        # Grab username and password form form
        username = request.form.get("_email")
        password = request.form.get("_password")

        debug["username"] = username
        debug["password_present"] = bool(password)

        if not username or not password:
            error = "Email and password are required"
        else:
            # Check if the credentials are valid
            valid = authenticate(username, password)
            debug["authentication_return"] = valid

            if valid:
                session['logged_in'] = True
                session['user_email'] = username
                session["role"] = "user"

                return redirect(url_for("chat.chat_screen"))
            
            # Render the login page
            error = "Authentication Failed"

    # Render the login page
    return render_template('login.html', error=error, debug=debug)