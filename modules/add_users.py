# This file adds users to the user database
# The users by file takes a file input and outputs a true or false depending on success
# The individual file takes an email, password, organization, and role and adds it to a database

# Imports
import boto3
import csv

# Setup Database
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')  # Change to your region
table = dynamodb.Table('users')

# Function to add users from a file to DynamoDB
def add_users_file(filename, organization):
    rows = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)

    # Remove header row if present
    topleft = str(rows[0][0])
    if '@' not in topleft:
        rows.pop(0)

    for row in rows:
        add_users_individual(row[0], row[1], organization, row[2])

    return True

# Function to add an individual user to DynamoDB
def add_users_individual(email, password, organization, role):
    # Prepare new user data
    new_user = {
        'Email': email,
        'Password': password,
        'Organization': organization,
        'Role': role
    }

    response = table.put_item(Item=new_user)

    return response