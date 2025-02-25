# Registers a new organization and adds it to all needed databases
# Takes the email, password, and organization as input
# Returns if an organization and user was able to be created

# Imports
import boto3

# Register Emails
def email_registration(email, password, org):
    # Initialize DB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('orgstyles')

    if org == None:
        org = email.split('@')[0]

        # Attempt to get the item by key
        key = {'Organization': org} 
        response = table.get_item(Key=key)

        # Check if it exists
        if 'Item' in response:
            return False
        
        # Append to Databases
        table = dynamodb.Table('orgstats')
        new_org_stats = {
            "Organization": org,
            "Images-this-period": 0,
            "Images-total": 0,
            "Messages-this-period": 0,
            "Messages-total": 0,
            "Payment-this-period": 0,
            "Tokens-this-period": 0,
            "Tokens-total": 0,
            "Total-payed": 0
        }
        table.put_item(Item=new_org_stats)

        table = dynamodb.Table("orgstyles")
        new_org_styles = {
            "Organization": org,
            "Org-logo": '',
            "Primary-color": "#B9B4B4",
            "Secondary-color": "#ffffff",
            "Text-color": "#000000"
        }
        table.put_item(Item=new_org_styles)

        table = dynamodb.Table("users")
        new_user = {
            "Email": email,
            "Organization": org,
            "Password": password,
            "Role": "Zone"
        }
        table.put_item(Item=new_user)

        return True
    else:
        # Attempt to get the item by key
        key = {'Organization': org} 
        response = table.get_item(Key=key)

        # Check if it exists
        if 'Item' in response:
            return False
        
        # Append to Databases
        table = dynamodb.Table('orgstats')
        new_org_stats = {
            "Organization": org,
            "Images-this-period": 0,
            "Images-total": 0,
            "Messages-this-period": 0,
            "Messages-total": 0,
            "Payment-this-period": 0,
            "Tokens-this-period": 0,
            "Tokens-total": 0,
            "Total-payed": 0
        }
        table.put_item(Item=new_org_stats)

        table = dynamodb.Table("orgstyles")
        new_org_styles = {
            "Organization": org,
            "Org-logo": '',
            "Primary-color": "#B9B4B4",
            "Secondary-color": "#ffffff",
            "Text-color": "#000000"
        }
        table.put_item(Item=new_org_styles)

        table = dynamodb.Table("users")
        new_user = {
            "Email": email,
            "Organization": org,
            "Password": password,
            "Role": "Zone"
        }
        table.put_item(Item=new_user)
        
        return True