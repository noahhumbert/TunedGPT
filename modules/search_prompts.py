# Searches the prompts database for requests that match the criteria
# Takes email, organization, start date, end date, start time, and end time as input
# Outputs a list containing the lists of all the rows that meet the criteria in the database

# Imports
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Initialize Database
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('prompts')

def search_prompts(email=None, organization=None, start_date=None, end_date=None, start_time=None, end_time=None):
    # Prepare date-time range in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
    if start_date and start_time:
        start_dt_iso = f"{start_date}T{start_time}"
    else:
        start_dt_iso = None
    
    if end_date and end_time:
        end_dt_iso = f"{end_date}T{end_time}"
    else:
        end_dt_iso = None
    
    # Start with query on the Partition Key (Email)
    query = {
        'KeyConditionExpression': Key('Email').eq(email)
    }

    # Add the Date-time range filter if provided
    if start_dt_iso and end_dt_iso:
        query['KeyConditionExpression'] &= Key('Date-time').between(start_dt_iso, end_dt_iso)
    elif start_dt_iso:
        query['KeyConditionExpression'] &= Key('Date-time').gte(start_dt_iso)
    elif end_dt_iso:
        query['KeyConditionExpression'] &= Key('Date-time').lte(end_dt_iso)

    # Add FilterExpression for non-key attributes (like Organization)
    if organization:
        query['FilterExpression'] = Attr('Organization').eq(organization)

    # Execute the query
    response = table.query(**query)

    # Return the matched items
    return response['Items']