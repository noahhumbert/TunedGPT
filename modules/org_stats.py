# This will make updates to the orgstats database to keep track of tokens, messages, and $$$ owed.
# It will take the inputted data is input
# It will output nothing

# Imports
import boto3
from decimal import Decimal

# Setup Database
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
table = dynamodb.Table('orgstats')

def calculate_cost(tokens, images):
    cost_per_token = float(0.000002)
    cost_per_image = float(0.5)

    return (cost_per_token * float(tokens)) + (cost_per_image * float(images))

def update_stats(injected_data):
    key = {"Organization": injected_data['Organization']}
    response = table.get_item(Key=key)

    # Check for organization in database
    data = response['Item']

    if not isinstance(injected_data["Tokens"], int):
        data['Images-total'] += 1
        data['Images-this-period'] += 1
    else:
        data['Messages-total'] += 1
        data['Messages-this-period'] += 1
        data['Tokens-this-period'] = data['Tokens-this-period'] + injected_data['Tokens']
        data['Tokens-total'] = data['Tokens-total'] + injected_data['Tokens']

    data['Payment-this-period'] = calculate_cost(data['Tokens-this-period'], data['Images-this-period'])

    # Create data object
    new_data = {
        "Organization": data['Organization'],
        "Tokens-this-period": data['Tokens-this-period'],
        "Tokens-total": data['Tokens-total'],
        "Messages-this-period": data['Messages-this-period'],
        "Messages-total": data['Messages-total'],
        "Payment-this-period": Decimal(str(data['Payment-this-period'])),
        "Total-payed": data['Total-payed'],
        "Images-total": data['Images-total'],
        "Images-this-period": data['Images-this-period']
    }

    # Inject into DynamoDB
    response = table.put_item(Item=new_data)