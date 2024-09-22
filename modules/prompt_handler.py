# Takes in the prompt and handles the responses. 
# Takes in a prompt for the AI
# Returns both the prompt and the response.

# Get S3 Handler
from modules.s3_handler import upload_file_to_s3

# Import Modules
from openai import OpenAI
from datetime import datetime
import os
import requests
from PIL import Image
from io import BytesIO

# AI Settings
client = OpenAI()
chatmodel = 'gpt-4o-mini'
imgmodel = 'dall-e-3'
temperature = 0.7

# Process the prompt.
def process_prompt(prompt, past_prompts, model_option): 
    # Process the past prompts
    thepast = ''
    for past_prompt in past_prompts:
        question = past_prompt['Question']
        response = past_prompt['Response']

        thepast = thepast + "\n Question: " + question + " Answer: " + response

    if model_option == 'chatgpt':
        # Try the prompt
        prompt = prompt.replace("\n", "")
        try:
            # Prompt the AI
            response = client.chat.completions.create(
                model=chatmodel,
                messages=[
                    {"role": "user", "content": "Here are the past questions and answers to reference: " + thepast + ". Here is your prompt: " + prompt + ". Do not mention being given the past just know its there"}
                ],
                temperature=temperature
            )

            # Extract the content from the response
            # data = [date, time, response, finish_reason, total_tokens]
            data = [datetime.now().date(), str(datetime.now().time()).split('.')[0], prompt, response.choices[0].message.content, response.choices[0].finish_reason, response.usage.prompt_tokens+response.usage.completion_tokens]
            return data
        # Except any errors
        except Exception as e:
            return f"Error: {e}"
        
    elif model_option == 'imagegen':
        # Handle image generation here
        prompt = prompt.replace("\n", "")
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )   

            # Fetch the image from the URL
            response = requests.get(response.data[0].url)
            response.raise_for_status()  # Check for any errors

            # Generate filename based on the current date and time
            filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.png'
            filepath = os.path.join('./static/imgcache', filename)

            # Open the image and save it to the imgcache folder
            image = Image.open(BytesIO(response.content))
            image.save(filepath)

            # Grab file from imgcache and upload it to S3
            file_path = './static/imgcache/' + filename
            object_key = 'imgcache/' + filename
            upload_file_to_s3(file_path, object_key)

            # Delete cached image
            os.remove('./static/imgcache/' + filename)

            data = [datetime.now().date(), str(datetime.now().time()).split('.')[0], prompt, filename, 'stop', 'image']

            return data

        except Exception as e:
            return f"Error: {e}"