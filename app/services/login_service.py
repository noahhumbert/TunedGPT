# Imports
import requests
import os

# Returns booleon true/false if authed successfully or not
def authenticate(username, password):
    # Snag the auth token from the environment
    NH_AUTH_TOKEN = os.environ.get("NH_AUTH_TOKEN")

    # API url
    url = "https://noahhumbert.com/api/check-role"

    # Headers
    headers = {
        "X-API-TOKEN": f"{NH_AUTH_TOKEN}",
        "Content-type": "application/json"
    }

    # Body 
    body = {
        "email": username,
        "password": password,
        "role": "ROLE_TUNEDGPT"
    }

    # POST request and grab response
    response = requests.POST(url, headers=headers, json=body)

    # Check of the user has the role
    has_role = bool(response.json().get("has_role", False))

    print(has_role)

    return has_role
