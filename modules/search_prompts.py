# Searches the prompts database for requests that match the criteria
# Takes email, organization, start date, end date, start time, and end time as input
# Outputs a list containing the lists of all the rows that meet the criteria in the database

# Imports
import csv
from datetime import datetime

# Search
def search_prompts(email, organization, start_date, end_date, start_time, end_time):
    # Grab the database
    database = []
    with open(".\\databases\\prompts.csv", mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            database.append(row)
        
        file.close()

    # Filter out the Organization
    organization_list = []
    for prompt in database:
        if prompt[1] == organization:
            organization_list.append(prompt)

    # Filter out dates
    date_list = []
    if start_date == '' or end_date == '':
        date_list = organization_list
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        for org in organization_list:
            time = datetime.strptime(org[2], '%Y-%m-%d')
            if start_date <= time <= end_date or end_date <= time <= start_date:
                date_list.append(org)

    # Filter out times
    time_list = []
    if start_time == '' or end_time == '':
        time_list = date_list
    else:
        start_time = start_time + ":00"
        end_time = end_time + ":00"
        start_time = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time, '%H:%M:%S').time()

        for date in date_list:
            trytime = datetime.strptime(date[3], '%H:%M:%S').time()
            if start_time <= trytime <= end_time or end_time <= trytime <= start_time:
                time_list.append(date)

    # Filter out emails
    search = []
    if email == '':
        search = time_list
    else:
        for address in time_list:
            if address[0] == email:
                search.append(address)

    return search