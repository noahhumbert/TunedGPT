from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Load config from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')  # fallback for dev

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
