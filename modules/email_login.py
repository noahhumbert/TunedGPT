# Logs the user into the computer
# Takes a username and password as input
# Returns a True or False, and if True also the username.

# Imports
import hashlib
from supabase import Client, create_client

# Initialize Supabase client
url: str = "https://cwopkvreemqzoorgalsq.supabase.co/"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3b3BrdnJlZW1xem9vcmdhbHNxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTkzNjk4MCwiZXhwIjoyMDQxNTEyOTgwfQ.zeQP7mgnuo4AWgbDJ4mV6yGGtNrczqtlXaV1q7QG3EE"
supabase: Client = create_client(url, key)

# login check function
def email_login(email, password):

    # Check for the email in the Supabase 'users' table
    response = supabase.from_("users").select("*").eq("email", email).execute()
    data = response.data

    # If no user is found, return a failed login
    if not data:
        return False, 'None'

    # Get the user data (there should only be one result since emails are unique)
    user = data[0]

    # Encrypt the input password to compare with the stored password
    hash_object = hashlib.sha256()
    hash_object.update(password.encode('utf-8'))
    hashed_password = hash_object.hexdigest()

    # Check if the provided password matches the stored one
    if user['password'] == hashed_password:
        return True, user
    else:
        return False, 'None'