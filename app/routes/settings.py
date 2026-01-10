# Import libraries
from flask import Blueprint, render_template, session, redirect, url_for

# Pull in service
# from app.services.settings_service import

settings_bp = Blueprint("settings", __name__)
@settings_bp.route("/", methods=["GET", "POST"])
def settings_screen():
    # If the user isn't logged in, redirect them to login
    if not 'logged_in' in session or ('logged_in' in session and not session['logged_in']):
        return redirect(url_for('login.login_screen'))
    
    return render_template('settings.html')