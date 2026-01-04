import os
from flask import Flask

def create_app():
    """
    Flask application factory
    """

    app = Flask(__name__)

    # ------------------------
    # Load configuration from environment
    # ------------------------
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "devsecret"),
        DEBUG=os.environ.get("DEBUG", "False").lower() in ("true", "1", "t"),
        PREFERRED_URL_SCHEME=os.environ.get("PREFERRED_URL_SCHEME", "https")
    )

    # ------------------------
    # Register Blueprints
    # ------------------------
    from app.routes.chat_route import chat_bp  # <-- updated to match your new filename
    app.register_blueprint(chat_bp)

    return app
