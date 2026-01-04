# Imports
from flask import Flask, session, render_template
import os

# Grab a Session Token
session_key = os.urandom(24)

# Initialize Flask
app = Flask(__name__)
app.secret_key = session_key

# Home Screen
def home():
    if not('logged_in' in session):
        return render_template('home.html')