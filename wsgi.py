import sys
import os

project_dir = "/var/www/TunedGPT"
sys.path.insert(0, project_dir)

from app import app as application
