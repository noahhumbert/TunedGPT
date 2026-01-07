import os
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_chat_response(message: str, model: str):
    # Creat the API request
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Logic to choose data json input
    if (model=="chatgpt-5-mini"):
        data = {
            "model": "gpt-5-mini",
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7
        }
    if (model=="chatgpt-5"):
        data = {
            "model": "gpt-5",
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7
        }
    elif (model=="imagegen"):
        data = {
            "model": "gpt-image-1.5",
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7
        }
    
    # Run the post request
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    # Inject Data into SQL DB


    # Run the 7 day check

    
