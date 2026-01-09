import os
from flask import Flask

def create_app():
    # Initialize Flask app with explicit template and static folders
    app = Flask(
        __name__,
        template_folder="templates",  # ensures Flask finds chat.html
        static_folder="static"        # ensures CSS/JS load properly
    )
    
    # Load configuration from environment variables
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "devsecret"),
        DEBUG=os.environ.get("DEBUG", "False").lower() in ("true", "1", "t"),
        PREFERRED_URL_SCHEME=os.environ.get("PREFERRED_URL_SCHEME", "https")
    )

    # Register routes / Blueprints
    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)  # serves '/'

    from app.routes.login import login_bp
    app.register_blueprint(login_bp) # serves '/login'

    return app
