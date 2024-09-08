# Logs the user into the computer
# Takes a username and password as input
# Returns a True or False, and if True also the username.

# Imports
import pandas
import hashlib
from flask import session

# Setup Database
usersdb = "G:\\My Drive\\Projects\\ProjectX1\\databases\\users.csv"
df = pandas.read_csv(usersdb)

# login check function
def email_login(email, password):

    # Check for the email in the database
    result_df = df[df['Email'] == email]

    # Clean up the output
    for index, row in result_df.iterrows():
        # Convert the row to a list excluding the index
        row_list = row.tolist()

    # Try to see if row_list has anything in it, except if it doesn't and pass a failed login as the return
    try:
       if row_list:
           pass
    except:
        return False, 'None'

    # Check if the password brought back from the db is the same as the password given, if not pass a failed login. If so, pass a successful login
    hash_object = hashlib.sha256()
    hash_object.update(password.encode('utf-8'))
    hashed_password = hash_object.hexdigest()

    if row_list[1] == hashed_password:
        return True, row_list
    else:
        return False, 'None'