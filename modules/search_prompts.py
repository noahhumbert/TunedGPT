# Searches the prompts database for requests that match the criteria
# Takes email, organization, start date, end date, start time, and end time as input
# Outputs a list containing the lists of all the rows that meet the criteria in the database

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