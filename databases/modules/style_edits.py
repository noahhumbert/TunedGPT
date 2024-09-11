# Edits the styles of the organization
# Takes the organization, image_link, primary_color, secondary_color, and text_color as inputs
# Outputs a True if it completed successfully

# Imports
from supabase import Client, create_client
from PIL import Image
from io import BytesIO
import requests
import shutil

url: str = "https://cwopkvreemqzoorgalsq.supabase.co/"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3b3BrdnJlZW1xem9vcmdhbHNxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTkzNjk4MCwiZXhwIjoyMDQxNTEyOTgwfQ.zeQP7mgnuo4AWgbDJ4mV6yGGtNrczqtlXaV1q7QG3EE"
supabase: Client = create_client(url, key)

# Function to update or insert styles
def style_edits(organization, image_link, primary_color, secondary_color, text_color):
    # Prepare new values
    new_values = {
        'org-logo': image_link,
        'primary-color': primary_color,
        'secondary-color': secondary_color,
        'text-color': text_color
    }

    # Update the existing record
    supabase.from_("orgstyles").update(new_values).eq("org", organization).execute()

    return

# Grab the styles
def style_grab(organization):
    # Query Supabase for the organization's styles
    response = supabase.from_("orgstyles").select("*").eq("org", organization).execute()
    data = response.data

    if data:
        # Extract the relevant fields
        styles = data[0]
        org_logo = styles['org-logo']
        primary_color = styles['primary-color']
        secondary_color = styles['secondary-color']
        text_color = styles['text-color']

        # Download and save the logo as org.ico
        response = requests.get(org_logo)
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGBA')
        img.save('./static/org.ico', format='ICO', sizes=[(32, 32)])

    else:
        # Default values if no styles are found
        org_logo = './static/favicon.ico'
        primary_color = '#000000'
        secondary_color = "#000000"
        text_color = '#ffffff'
        
        # Copy default favicon
        shutil.copy('./static/favicon.ico', './static/org.ico')

    return org_logo, primary_color, secondary_color, text_color