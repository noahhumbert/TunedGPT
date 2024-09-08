# Grab functions from modules that are needed
from modules.add_users import add_users_file, add_users_individual
from modules.email_login import email_login
from modules.format_text import format_text
from modules.inject_prompt import inject_prompt
from modules.prompt_handler import process_prompt
from modules.search_prompts import search_prompts
from modules.style_edits import style_edits
from modules.style_grab import style_grab

# Imports
from flask import Flask, request, render_template, redirect, url_for, session
import os
from datetime import datetime, timedelta

# Grab a Session Token
session_key = os.urandom(24)

# Initialize Flask
app = Flask(__name__)
app.secret_key = session_key

# Data Variables
userdata = ['', '', '', '']

# Home Screen
@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('login'))  
    else:
        return redirect(url_for('login'))   

# Login Screen
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Grab the global userdata variable
    global userdata

    # Check if Logged in already in the session
    if 'logged_in' in session:
        return redirect(url_for('ai'))

    org_logo, primary_color, secondary_color, text_color = style_grab(userdata[2])

    # Open the request form
    if request.method == 'POST':
        # Grab the info submitted
        email = request.form['email']
        password = request.form['password']

        # Attempt a Login
        valid, user_data = email_login(email, password)

        # Check if the Login was successful, if so set needed variables and send to ai, if not have them retry
        if valid == True:
            session['logged_in'] = True
            session['username'] = email
            userdata = user_data

            # See if admin panel should show up.
            if userdata[3] == "Admin":
                session['is_admin'] = True

            if userdata[3] == "Zone":
                session['is_zone'] = True

            org_logo, primary_color, secondary_color, text_color = style_grab(userdata[2])

            return redirect(url_for('ai'))

    # If it fails, restart the login
    return render_template('login.html', primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo)

# AI Prompt screen
@app.route('/ai', methods=['GET', 'POST'])
def ai():
    # Check if the user is logged in, if so go to the screen and await form submittion, if not get sent to login
    if 'logged_in' in session:
        org_logo, primary_color, secondary_color, text_color = style_grab(userdata[2])

        # Format date and time
        now = datetime.now()
        current_date = now.date()
        seven_days_ago = now - timedelta(days=7)
        seven_days_ago_date = seven_days_ago.date()

        # Search for searches
        searches = []
        searches = search_prompts(userdata[0], userdata[2], str(seven_days_ago_date), str(current_date), '', '')

        for search in searches:
            search[4] = format_text(search[4])
            search[5] = format_text(search[5])

        if request.method == 'POST':
            # Grab the prompt from the form
            user_prompt = request.form.get('user_prompt')

            # Send the prompt to AI and grab the data
            data = process_prompt(user_prompt)
            answer = data[3]

            # Send the data and user to inject into the database
            injected = inject_prompt(userdata[0], userdata[2], data)

            # Search for searches
            searches = []
            searches = search_prompts(userdata[0], userdata[2], str(seven_days_ago_date), str(current_date), '', '')

            for search in searches:
                search[4] = format_text(search[4])
                search[5] = format_text(search[5])

        if 'is_admin' in session:
            return render_template('ai.html', searches=searches, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, org_name=userdata[2])
        elif 'is_zone' in session:
            return render_template('ai.html', searches=searches, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_zone=True, is_admin=True, org_name=userdata[2])
    else:
        return redirect(url_for('login'))

# Search Panel Screen
@app.route('/search', methods=['GET', 'POST'])
def search():
    global search_data
    
    org_logo, primary_color, secondary_color, text_color = style_grab(userdata[2])

    if 'logged_in' in session:
        if not 'is_admin' in session and not 'is_zone' in session:
            return redirect(url_for('ai'))
    else:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Grab all data
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        search_email = request.form['email']    
        organization = userdata[2]

        # Search
        print(search_email, organization, start_date, end_date, start_time, end_time)
        search_data = search_prompts(search_email, organization, start_date, end_date, start_time, end_time)

        return redirect(url_for('search_results'))

    # Render Template
    if 'is_admin' in session:
        return render_template('search.html', primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, org_name=userdata[2])
    elif 'is_zone' in session:
        return render_template('search.html', primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata[2])

# Displays search results
@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    global search_data

    org_logo, primary_color, secondary_color, text_color = style_grab(userdata[2])

    if 'logged_in' in session:
        if 'is_admin' in session or 'is_zone' in session:
            return render_template('search_results.html', search=search_data, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata[2])
        else:
            return redirect(url_for('ai'))
    else:
        return redirect(url_for('login'))
    
# Opens the organization customizer
@app.route('/styling', methods=['GET', 'POST'])
def styling():
    if 'logged_in' in session:
        if not 'is_zone' in session:
            return redirect(url_for('ai'))
    else:
        return redirect(url_for('login'))

    # Pre-populate the fields
    og_image_link,og_primary_color,og_secondary_color,og_text_color = style_grab(userdata[2])

    # Grab data from the form
    if request.method == 'POST':
        image_link = request.form.get('image_link')
        primary_color = request.form.get('primary_color')
        secondary_color = request.form.get('secondary_color')
        text_color = request.form.get('text_color')

        edits = style_edits(userdata[2], image_link, primary_color, secondary_color, text_color)

        # Pre-populate the fields
        og_image_link,og_primary_color,og_secondary_color,og_text_color = style_grab(userdata[2])
    # Run the template
    return render_template('styling.html', organization_name=userdata[2], image_link=og_image_link, primary_color=og_primary_color, secondary_color=og_secondary_color, text_color=og_text_color, is_admin=True, is_zone=True, org_name=userdata[2])

# Add Users to Organization
@app.route('/add_users', methods=['GET', 'POST'])
def add_users():
    message = None

    org_logo, primary_color, secondary_color, text_color = style_grab(userdata[2])

    if 'logged_in' in session:
        if not 'is_zone' in session:
            return redirect(url_for('ai'))
    else:
        return redirect(url_for('login'))
    
    # Grab data from the form
    if request.method == 'POST':
        message = ''

        # Get form responses
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        file = request.files.get('file')

        # Upload the file to the directory
        if file.filename == '':
            pass
        else:
            if file and file.filename.endswith('.csv'):
                # Secure the filename and save the file to the upload folder
                filename = os.path.join('./uploads', file.filename)
                file.save(filename)

        # Make sure enough data was given and go down the correct path
        success = None
        if (email == '' or password == '' or role == '') and file.filename == '':
            message = 'Make sure you give either a file directory, or email, password, and role'
        elif not file.filename == '':
            success = add_users_file(filename, userdata[2])
        elif email == '' or password == '' or role == '':
            message = 'If you are not using a file, make sure you input a email, password, and a role'
        else:
            success = add_users_individual(email, password, userdata[2], role)

        # Give a success message if successful
        if success == True:
            message = 'User(s) have been added!'
        else:
            pass
        
        # Delete cached file
        if not file.filename == '':
            os.remove(filename)

        return render_template('add_users.html', message=message, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata[2])
    
    if message == None:
        return render_template('add_users.html', message='', primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata[2])
    else:
        return render_template('add_users.html', message=message, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata[2])

# Run Webapp
with app.app_context():
        print("Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(rule)
app.run(debug=True)