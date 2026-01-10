# Imports
import os
import requests
import mysql.connector
import time

# Snag the API key from the enviornment veriable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Database connection initialization
def initialize_message_database():
    # Grab environment variables
    DB_HOST = os.environ.get("DB_HOST")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = os.environ.get("DB_PORT")

    # Create Connection
    conn = mysql.connector.connect(
        host=f"{DB_HOST}",
        user=f"{DB_USER}",
        password=f"{DB_PASSWORD}",
        database=f"{DB_NAME}",
        port=int(DB_PORT),
        autocommit=False
    )

    return conn

def pull_chat_history(email: str):
    # Initialize conneciton
    conn = initialize_message_database()

    # Initialize Cursor
    cursor = conn.cursor()

    # SQL query
    sql = """
        SELECT user_message, response
        FROM message_history
        WHERE email = %s
        ORDER BY timestamp ASC
    """

    # Execute Command
    try:
        cursor.execute(sql, (email,))
        rows = cursor.fetchall()
    # Except database error
    except mysql.connector.Error as e:
        print(f"Database error while fetching conversation: {e}")
    # Except generic error
    except Exception as e:
        print(f"Unexpected error: {e}")
    # Finally close the session
    finally:
        cursor.close()
        conn.close()

    # Initialize conversation history list with system at index 0
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    # Iterate through the messages and append the questions and responses from the DB
    for row in rows:
        # Append to conversation
        conversation.append({"role": "user", "content": row[0]})
        conversation.append({"role": "assistant", "content": row[1]})

    # return the conversation
    return conversation

# Get the chat response from OpenAI
def get_chat_response(message: str, model: str, email: str):
    # Creat the API request
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Snag the full chat history
    conversation = pull_chat_history(email)

    # Append the new message to the history
    conversation.append({"role": "user", "content": message})

    # Logic to choose data json input
    if (model=="chatgpt-5-mini"):
        data = {
            "model": "gpt-5-mini",
            "messages": conversation
        }
    if (model=="chatgpt-5"):
        data = {
            "model": "gpt-5",
            "messages": conversation
        }
    elif (model=="imagegen"):
        data = {
            "model": "gpt-image-1.5",
            "messages": conversation
        }
    
    # Run the post request
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    # Return the datas
    return result

# Parse the result data
def parse_chat_response(response):
    # Snag the ID from the response JSON
    id = response["id"]

    # Pull the timestamp
    timestamp = response["created"]

    # Pull the response
    chat_response = response['choices'][0]['message']['content']

    # Pull the tokens
    tokens = response['usage']['total_tokens']

    return id, timestamp, chat_response, tokens

def inject_chat_interaction(email, id, timestamp, user_message, dropdown_value, response, tokens_used):
    # Initialize the DB connection
    conn = initialize_message_database()

    # Create the cursor
    cursor = conn.cursor()

    # SQL Insertion Statement
    sql = """
    INSERT INTO message_history
    (id, email, timestamp, user_message, model, response, tokens_used)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Attempt to execute the data injection
    try:
        # Execute insert with parameters
        cursor.execute(sql, (
            id,
            email,
            timestamp,
            user_message,
            dropdown_value,  # model
            response,
            tokens_used
        ))

        # Commit changes
        conn.commit()
        print(f"Message {id} logged successfully.")
    # If there is an error, rollback changes and print error
    except mysql.connector.Error as e:
        # Rollback on error
        conn.rollback()
        print(f"Error inserting chat interaction: {e}")
    # After the fact, close the SQL session
    finally:
        # Close resources
        cursor.close()
        conn.close()

# Delete chat cache older than 7 days
def cleanup_chat_history():
    # Get the current Unix timestamp
    current_time = int(time.time())

    # Message Retention Math
    days = 7
    retention_time = int(days*86400)

    # Get the oldest time allowed
    oldest_time = current_time-retention_time

    # Initialize the DB connection
    conn = initialize_message_database()

    # Create the cursor
    cursor = conn.cursor()

    # Parameterized DELETE statement
    sql = """
    DELETE FROM message_history
    WHERE timestamp < %s
    """

    # Try the SQL query
    try:
        cursor.execute(sql, (oldest_time,))
        deleted_rows = cursor.rowcount
        conn.commit()
        print(f"Deleted {deleted_rows} old messages older than {oldest_time}.")
    # If the query fails
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Error deleting old messages: {e}")
    # Finally close the connection
    finally:
        cursor.close()
        conn.close()

def get_chat_history(email: str):
    # Initialize the connection
    conn = initialize_message_database()

    # Initialize the Cursor
    cursor = conn.cursor()

    # SQL Query
    sql = """
            SELECT user_message, response
            FROM message_history
            WHERE email = %s
            ORDER BY timestamp ASC
        """

    # Create chat history list
    chat_history = []

    # Initialize the cursor
    try:
        cursor.execute(sql, (email,))
        rows = cursor.fetchall()

        # Convert each row to a dict for Jinja
        for row in rows:
            chat_history.append({
                "user_message": row["user_message"],
                "response": row["response"]
            })
    # Except SQL connection error
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    # Except Generic Error
    except Exception as e:
        print(f"Unexpected error: {e}")
    # Finally
    finally:
        cursor.close()
        conn.close()

    return chat_history