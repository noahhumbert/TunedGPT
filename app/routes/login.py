# Import libraries
from flask import Blueprint, render_template, request, session, redirect, url_for

# Pull in service
from app.services.login_service import authenticate

login_bp = Blueprint("login", __name__)
@login_bp.route("/login", methods=["GET", "POST"])
def login_screen():
    # If the user is logged in, redirect them to chat
    if 'logged_in' in session:
        return redirect(url_for('chat.html'))
    
    # On form submit
    if request.method == 'post':
        # Grab username and password form form
        username = request.form.get("_username")
        password = request.form.get("_password")

        # Check if the credentials are valid
        valid = authenticate(username, password)

        if valid:
            session['logged_in'] = True
            session['user_email'] = username
            session["role"] = "user"

            return redirect(url_for("chat.html"))

    # Render the login page
    render_template('login.html')