# Grab functions from modules that are needed
from modules.add_users import add_users_file, add_users_individual
from modules.clean_images import clean_images
from modules.email_login import email_login
from modules.format_text import format_text
from modules.inject_prompt import inject_prompt
from modules.org_stats import update_stats
from modules.prompt_handler import process_prompt
from modules.search_prompts import search_prompts
from modules.style_edits import style_edits, style_grab

# Imports
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
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
        return redirect(url_for('ai')) 
    else:
        return redirect(url_for('login'))   

# Login Screen
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Grab the global userdata variable
    global userdata

    # Check if already logged in via the session
    if 'logged_in' in session:
        return redirect(url_for('ai'))

    # Set default style for the login page
    # Access organization from the list if userdata is not None, otherwise use 'default_org'
    org_logo, primary_color, secondary_color, text_color = style_grab('default_org')

    # Open the request form
    if request.method == 'POST':
        # Grab the info submitted
        email = request.form['email']
        password = request.form['password']

        # Attempt a login
        valid, user_data = email_login(email, password)

        # Check if the login was successful
        if valid:
            session['logged_in'] = True
            session['username'] = email
            userdata = user_data  # This will still be a list from Supabase

            # See if admin panel should show up based on user role
            if userdata['role'] == "Admin":  # userdata[3] refers to the Role
                session['is_admin'] = True
            if userdata['role'] == "Zone":
                session['is_zone'] = True

            # Grab the organization-specific styles again after login
            org_logo, primary_color, secondary_color, text_color = style_grab(userdata['organization'])

            return redirect(url_for('ai'))

    # If login fails or is not yet attempted, render the login page again
    return render_template('login.html', primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo)

# AI Prompt screen
@app.route('/ai', methods=['GET', 'POST'])
def ai():
    # Check if the user is logged in, if so go to the screen and await form submittion, if not get sent to login
    if 'logged_in' in session:
        org_logo, primary_color, secondary_color, text_color = style_grab(userdata['organization'])

        # Format date and time
        now = datetime.now()
        current_date = now.date()
        seven_days_ago = now - timedelta(days=7)
        seven_days_ago_date = seven_days_ago.date()

        # Search for searches
        searches = search_prompts(userdata['email'], userdata['organization'], str(seven_days_ago_date), str(current_date), '', '')

        for row in searches:
            question = row['question']
            response = row['response']

            question = format_text(question)
            response = format_text(response)

        if request.method == 'POST':
            # Grab the prompt from the form
            user_prompt = request.form.get('user_prompt')
            model_option = request.form.get('model_option')

            # Send the prompt to AI and grab the data
            data = process_prompt(user_prompt, searches, model_option)

            # Send the data and user to inject into the database
            injected_data = inject_prompt(userdata['email'], userdata['organization'], data)

            # Update the orgstats db
            update_stats(injected_data)

            # Clean up the image cache
            clean_images()

            # Search for searches
            searches = search_prompts(userdata['email'], userdata['organization'], str(seven_days_ago_date), str(current_date), '', '')

            for row in searches:
                question = row['question']
                response = row['response']

                question = format_text(question)
                response = format_text(response)

        if 'is_admin' in session:
            return render_template('ai.html', searches=searches, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, org_name=userdata['organization'])
        elif 'is_zone' in session:
            return render_template('ai.html', searches=searches, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_zone=True, is_admin=True, org_name=userdata['organization'])
    else:
        return redirect(url_for('login'))

# Search Panel Screen
@app.route('/search', methods=['GET', 'POST'])
def search():
    global search_data
    
    org_logo, primary_color, secondary_color, text_color = style_grab(userdata['organization'])

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
        search_data = search_prompts(search_email, organization, start_date, end_date, start_time, end_time)

        return redirect(url_for('search_results'))

    # Render Template
    if 'is_admin' in session:
        return render_template('search.html', primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, org_name=userdata['organization'])
    elif 'is_zone' in session:
        return render_template('search.html', primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata['organization'])

# Displays search results
@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    global search_data

    org_logo, primary_color, secondary_color, text_color = style_grab(userdata['organization'])

    if 'logged_in' in session:
        if 'is_admin' in session or 'is_zone' in session:
            return render_template('search_results.html', search=search_data, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata['organization'])
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
    og_image_link,og_primary_color,og_secondary_color,og_text_color = style_grab(userdata['organization'])

    # Grab data from the form
    if request.method == 'POST':
        image_link = request.form.get('image_link')
        primary_color = request.form.get('primary_color')
        secondary_color = request.form.get('secondary_color')
        text_color = request.form.get('text_color')

        style_edits(userdata['organization'], image_link, primary_color, secondary_color, text_color)

        # Pre-populate the fields
        og_image_link,og_primary_color,og_secondary_color,og_text_color = style_grab(userdata['organization'])
    # Run the template
    return render_template('styling.html', organization_name=userdata['organization'], image_link=og_image_link, primary_color=og_primary_color, secondary_color=og_secondary_color, text_color=og_text_color, is_admin=True, is_zone=True, org_name=userdata['organization'])

# Add Users to Organization
@app.route('/add_users', methods=['GET', 'POST'])
def add_users():
    message = None

    org_logo, primary_color, secondary_color, text_color = style_grab(userdata['organization'])

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
            success = add_users_file(filename, userdata['organization'])
        elif email == '' or password == '' or role == '':
            message = 'If you are not using a file, make sure you input a email, password, and a role'
        else:
            success = add_users_individual(email, password, userdata['organization'], role)

        # Give a success message if successful
        if success == True:
            message = 'User(s) have been added!'
        else:
            pass
        
        # Delete cached file
        if not file.filename == '':
            os.remove(filename)

        return render_template('add_users.html', message=message, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata['organization'])
    
    if message == None:
        return render_template('add_users.html', message='', primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata['organization'])
    else:
        return render_template('add_users.html', message=message, primary_color=primary_color, secondary_color=secondary_color, text_color=text_color, org_logo=org_logo, is_admin=True, is_zone=True, org_name=userdata['organization'])

@app.route('/health', methods=['GET'])
def health_check():
    # You can add more comprehensive checks here if needed
    return jsonify(status='healthy'), 200
