import sys

project_dir = "/var/www/TunedGPT"
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from app import create_app
application = create_app()
