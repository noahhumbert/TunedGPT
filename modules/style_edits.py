# Edits the styles of the organization
# Takes the organization, image_link, primary_color, secondary_color, and text_color as inputs
# Outputs a True if it completed successfully

# Imports
from PIL import Image
from io import BytesIO
import requests
import shutil
import boto3

# Setup Database
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('orgstyles')

# Function to update or insert styles
def style_edits(organization, image_link, primary_color, secondary_color, text_color):
    # Prepare new values
    new_values = {
        'Organization': organization,
        'Org-logo': image_link,
        'Primary-color': primary_color,
        'Secondary-color': secondary_color,
        'Text-color': text_color
    }

    # Update the existing record
    response = table.put_item(Item=new_values)

    return

# Grab the styles
def style_grab(organization):
    # Query Supabase for the organization's styles
    key = {"Organization": organization}

    try: 
        response = table.get_item(Key=key)
    
        # Extract the relevant fields
        styles = response['Item']
        org_logo = styles['Org-logo']
        primary_color = styles['Primary-color']
        secondary_color = styles['Secondary-color']
        text_color = styles['Text-color']

        # Download and save the logo as org.ico
        try:
            response = requests.get(org_logo)
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGBA')
            img.save('./static/org.ico', format='ICO', sizes=[(32, 32)])
        except:
            # Copy default favicon
            shutil.copy('./static/favicon.ico', './static/org.ico')
    except:
        # Default values if no styles are found
        org_logo = './static/favicon.ico'
        primary_color = '#000000'
        secondary_color = "#000000"
        text_color = '#ffffff'
        
        # Copy default favicon
        shutil.copy('./static/favicon.ico', './static/org.ico')

    return org_logo, primary_color, secondary_color, text_color
