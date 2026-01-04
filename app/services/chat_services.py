import os
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # Inject via Docker Compose

def get_chat_response(message: str) -> str:
    """
    Sends the user's message to OpenAI's ChatGPT API and returns the AI response.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]
