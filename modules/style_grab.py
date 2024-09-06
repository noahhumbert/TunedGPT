# Grabs the styles from the organizations row in the orgstyles db
# Takes the organization as an input
# Returns all info in the db

# Imports
import csv
import shutil
import requests
from io import BytesIO
from PIL import Image

# Grab the styles
def style_grab(organization):
    # Grab the database
    database = []
    with open('.\\databases\\orgstyles.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            database.append(row)

        file.close()

    # Find the styles
    styles = None
    for row in database:
        if row[0] == organization:
            styles = row
            break
    
    # Pop the first value
    if styles is not None:
        styles.pop(0)

        org_logo = styles[0]
        primary_color = styles[1]
        secondary_color = styles[2]
        text_color = styles[3]

        response = requests.get(org_logo)
        img = Image.open(BytesIO(response.content))

        img = img.convert('RGBA')
        img.save('.\\static\\org.ico', format='ICO', sizes=[(32, 32)])
    else:
        org_logo = '.\\static\\favicon.ico'
        primary_color = '#000000'
        secondary_color = "#000000"
        text_color = '#ffffff'
        
        shutil.copy('.\\static\\favicon.ico', '.\\static\\org.ico')
    return org_logo, primary_color, secondary_color, text_color