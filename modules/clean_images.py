# This file runs through every image in imgcache and sees if it is older than 7 days old then deletes it if it is
# No input
# No output

# Imports
import os
from datetime import datetime, timedelta

# Deletes the files
def clean_images():
    for filename in os.listdir('./static/imgcache'):
        current_date = datetime.now()
        file_date_str = filename.split('_')[0]  # Get the 'YYYY-MM-DD' part
        file_date = datetime.strptime(file_date_str, '%Y-%m-%d')  # Parse it into a date object

        if current_date - file_date >= timedelta(days=8):
                print(f"Deleting file: {filename}")
                os.remove('./imgcache/' + filename)  # Delete the file
            