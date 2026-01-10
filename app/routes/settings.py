# Import libraries
from flask import Blueprint, render_template, session, redirect, url_for, request

# Pull in service
# from app.services.settings_service import push_settings, pull_settings, apply_settings

settings_bp = Blueprint("settings", __name__)
@settings_bp.route("/settings", methods=["GET", "POST"])
def settings_screen():
    # If the user isn't logged in, redirect them to login
    if not 'logged_in' in session or ('logged_in' in session and not session['logged_in']):
        return redirect(url_for('login.login_screen'))
    
    if request.method == "POST":
        # Pull ALL form values at once
        settings_data = request.form.to_dict()

        # Push the settings to the DB
        # push_settings(session['user_email'], settings_data)

        # Pull the settings from the DB
        # apply_settings(session['user_email'])

        # Redirect back to the chat with the new settings pulled
        return redirect(url_for('chat.chat_screen'))

    # Pull the settings to show on the template
    # settings_data = pull_settings(session['user_email'])

    # Return the template
    return render_template('settings.html', settings_data=settings_data)