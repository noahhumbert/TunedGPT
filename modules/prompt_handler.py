# Takes in the prompt and handles the responses. 
# Takes in a prompt for the AI
# Returns both the prompt and the response.

# Import Modules
from openai import OpenAI
from datetime import datetime

# AI Settings
client = OpenAI()
model = 'gpt-4o-mini'
temperature = 0.7

# Process the prompt.
def process_prompt(prompt): 
    # Try the prompt
    prompt = prompt.replace("\n", "")
    try:
        # Prompt the AI
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        # Extract the content from the response
        # data = [date, time, response, finish_reason, total_tokens]
        data = [datetime.now().date(), str(datetime.now().time()).split('.')[0], prompt, response.choices[0].message.content, response.choices[0].finish_reason, response.usage.total_tokens]
        return data
                

    # Except any errors
    except Exception as e:
        return f"Error: {e}"