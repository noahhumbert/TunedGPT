# This file adds users to the user database
# The users by file takes a file input and outputs a true or false depending on success
# The individual file takes an email, password, organization, and role and adds it to a database

# Imports
import csv
import hashlib
import pandas

# Setup Database
usersdb = "G:\\My Drive\\Projects\\ProjectX1\\databases\\users.csv"
df = pandas.read_csv(usersdb)

def add_users_file(filename, organization):
    rows = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)

    topleft = str(rows[0][0])
    if not '@' in topleft:
        rows.pop(0)

    for index in rows:
        success = add_users_individual(index[0], index[1], organization, index[2])

    return True

# Adds and individual
def add_users_individual(email, password, organization, role):
    # Check for the email in the database
    result_df = df[df['Email'] == email]

    # Clean up the output
    for index, row in result_df.iterrows():
        # Convert the row to a list excluding the index
        row_list = row.tolist()

    # Try to see if row_list has anything in it, except if it doesn't and pass a failed login as the return
    try:
       if row_list:
           return False
    except:
        pass

    # Encrypt password
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    encrypted_password = sha256.hexdigest()

    inject_user = [email, encrypted_password, organization, role]

    # Writes User
    with open('.\\databases\\users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(inject_user)
        file.close()
    
    return True
    