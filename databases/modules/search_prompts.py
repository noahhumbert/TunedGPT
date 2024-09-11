# Searches the prompts database for requests that match the criteria
# Takes email, organization, start date, end date, start time, and end time as input
# Outputs a list containing the lists of all the rows that meet the criteria in the database

'''

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
            time = datetime.strptime(str(org[2]), '%Y-%m-%d')
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
    
'''

# Imports
from supabase import create_client, Client
from datetime import datetime

# Initialize Database
url: str = "https://cwopkvreemqzoorgalsq.supabase.co/"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3b3BrdnJlZW1xem9vcmdhbHNxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTkzNjk4MCwiZXhwIjoyMDQxNTEyOTgwfQ.zeQP7mgnuo4AWgbDJ4mV6yGGtNrczqtlXaV1q7QG3EE"
supabase: Client = create_client(url, key)

def search_prompts(email, organization, start_date, end_date, start_time, end_time):
    # Start building the quiery
    query = supabase.table('prompts').select('*')

    # Filter out organization
    query = query.eq('organization', organization)

    # Filter by date range if provided
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        query = query.gte('date', start_date).lte('date', end_date)

    # Filter by time range if provided
    if start_time and end_time:
        start_time = datetime.strptime(start_time + ":00", '%H:%M:%S').time()
        end_time = datetime.strptime(end_time + ":00", '%H:%M:%S').time()
        query = query.gte('time', start_time).lte('time', end_time)

    # Filter by email if provided
    if email:
        query = query.eq('email', email)

    # Execute the query
    response = query.execute()
    
    return response.data