# Import libraries
from flask import Blueprint, session, redirect, url_for

logout_bp = Blueprint("logout", __name__)
@logout_bp.route("/logout", methods=["GET"])
def logout():
    session['logged_in'] = None
    session['user_email'] = ''
    session['role'] = ''

    return redirect(url_for("login.login_screen"))