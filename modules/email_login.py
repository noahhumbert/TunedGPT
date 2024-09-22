# Logs the user into the computer
# Takes a username and password as input
# Returns a True or False, and if True also the username.

# Imports
import boto3

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('users')

# login check function
def email_login(email, password):
    primary_key = {'Email': email}

    response = table.get_item(Key=primary_key)

    item = response.get('Item')

    if not item:
        return False, 'None'
    

    if password == item["Password"]:
        return True, item
    
    return False, 'None'