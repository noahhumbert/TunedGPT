import requests

# Snag the auth token from the environment
NH_AUTH_TOKEN = "9zCtsynul4ItNwpyGXDupZ0EMWM7768L2Eo"

# API url
url = "https://noahhumbert.com/api/check-role"

# Headers
headers = {
    "X-API-TOKEN": f"{NH_AUTH_TOKEN}",
    "Content-type": "application/json"
}

# Body 
body = {
    "email": "nhumbert26@gmail.com",
    "password": "159013113Noah#",
    "role": "ROLE_TUNEDGPT"
}

# POST request and grab response
response = requests.post(url, headers=headers, json=body)

# Check of the user has the role
has_role = bool(response.json().get("has_role", False))

print(has_role)