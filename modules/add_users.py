# This file adds users to the user database
# The users by file takes a file input and outputs a true or false depending on success
# The individual file takes an email, password, organization, and role and adds it to a database

# Imports
from supabase import Client, create_client
import hashlib
import csv

# Setup Database
url: str = "https://cwopkvreemqzoorgalsq.supabase.co/"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3b3BrdnJlZW1xem9vcmdhbHNxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTkzNjk4MCwiZXhwIjoyMDQxNTEyOTgwfQ.zeQP7mgnuo4AWgbDJ4mV6yGGtNrczqtlXaV1q7QG3EE"
supabase: Client = create_client(url, key)

# Function to add users from a file to Supabase
def add_users_file(filename, organization):
    rows = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)

    # Remove header row if present
    topleft = str(rows[0][0])
    if '@' not in topleft:
        rows.pop(0)

    for row in rows:
        add_users_individual(row[0], row[1], organization, row[2])

    return True

# Function to add an individual user to Supabase
def add_users_individual(email, password, organization, role):
    # Check if the email already exists in the Supabase users table
    response = supabase.from_("users").select("email").eq("email", email).execute()
    data = response.data

    # If email already exists, return False
    if data:
        return False

    # Encrypt the password using SHA256
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    encrypted_password = sha256.hexdigest()

    # Prepare new user data
    new_user = {
        'email': email,
        'password': encrypted_password,
        'organization': organization,
        'role': role
    }

    # Insert new user into the users table
    supabase.from_("users").insert(new_user).execute()

    return True