# Takes the data that is returned from the prompt_handler and injects it into a database
# Input is the user logged in and data from prompt_handler
# Output is a just a return to show it completed

# Imports
import boto3

# Initialize Database
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('prompts')

# Inject the prompt
def inject_prompt(user, organization, data):
    # Create a New Data list to combine the user with Data
    new_data = []
    new_data.append(user)
    new_data.append(organization)
    for piece in data:
        new_data.append(piece)

    # Remote the commas from the response to keep the whole thing inside one column
    new_data[4] = new_data[4].replace(",", "").replace("\n", "").replace("#", "").replace('#', '')
    new_data[5] = new_data[5].replace(",", "").replace("\n", "").replace("#", "").replace('#', '')
    
    injected_data = {
        "Email": new_data[0],
        "Date-time": str(new_data[2]) + "T" + str(new_data[3]),
        "Organization": new_data[1],
        "Question": new_data[4],
        "Response": new_data[5],
        "Stop-reason": new_data[6],
        "Tokens": new_data[7]
    }

    table.put_item(Item=injected_data)

    return injected_data