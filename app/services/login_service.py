# Imports
import requests
import os

# Logging
import logging
logger = logging.getLogger(__name__)

# Returns booleon true/false if authed successfully or not
def authenticate(username, password):
    # Snag the auth token from the environment
    NH_AUTH_TOKEN = os.environ.get("NH_AUTH_TOKEN")

    # API url
    url = "https://www.noahhumbert.com/api/check-role"

    # Headers
    headers = {
        "X-API-TOKEN": f"{NH_AUTH_TOKEN}",
        "Content-type": "application/json"
    }

    logger.debug(headers)
    
    # Body 
    body = {
        "email": username,
        "password": password,
        "role": "ROLE_TUNEDGPT"
    }

    logger.debug(body)

    # POST request and grab response
    response = requests.post(url, headers=headers, json=body)

    logger.debug(response)

    # Parse it with JSON
    data = response.json()

    # Check of the user has the role
    has_role = bool(data['has_role'])

    # Return bool true or false if user has role
    logger.debug(has_role)
    return has_role
