import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

def create_app():
    # Load environment variables from .env
    load_dotenv()  # looks for .env in current working dir

    app = Flask(__name__)

    # Config from environment
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "devsecret"),
        DEBUG=os.environ.get("DEBUG", "False") == "True",
        DATABASE_URL=os.environ.get("DATABASE_URL", "sqlite:///dev.db"),
        PREFERRED_URL_SCHEME=os.environ.get("PREFERRED_URL_SCHEME", "https")
    )

    # Fix proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # Register blueprints/routes
    from .routes import main
    app.register_blueprint(main)

    return app
