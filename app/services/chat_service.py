# Imports
import os
import requests
import mysql.connector
import time
from pathlib import Path

# Get SQL initializer
from app.services.database_init import initialize_database_connection

# Snag the API key from the enviornment veriable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Pull the user memory from the DB
def pull_user_memory(email):
# Initialize Database Connection
    conn = initialize_database_connection()

    # Initialize Cursor
    cursor = conn.cursor(dictionary=True)
    
    # Query
    sql = """
        SELECT memory_summary
        FROM user_memory
        WHERE email = %s
    """

    # Initialize the query
    try:
        cursor.execute(sql, (email,))
        old_memory = cursor.fetchone()
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

    return old_memory

# Pull the user's chat history
def pull_chat_history(email: str):
    # Initialize conneciton
    conn = initialize_database_connection()

    # Initialize Cursor
    cursor = conn.cursor(dictionary=True)

    # SQL query
    sql = """
        SELECT user_message, response
        FROM message_history
        WHERE email = %s
        ORDER BY timestamp ASC
    """

    # Initialze rows
    rows = []

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

    # Get old user memory
    old_memory = pull_user_memory(email)

    # Initialize conversation history list with system at index 0
    conversation = [{"role": "system", "content": f"Long Term User Information: {old_memory}"}]

    # Iterate through the messages and append the questions and responses from the DB
    for row in rows:
        # Append to conversation
        conversation.append({"role": "user", "content": row['user_message']})
        conversation.append({"role": "assistant", "content": row['response']})

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
    elif (model=="chatgpt-5"):
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

# Inject the chat interaction into the chat history db
def inject_chat_interaction(email, id, timestamp, user_message, dropdown_value, response, tokens_used):
    # Initialize the DB connection
    conn = initialize_database_connection()

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
    conn = initialize_database_connection()

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

# Get the chat history
def get_chat_history(email: str):
    # Initialize the connection
    conn = initialize_database_connection()

    # Initialize the Cursor
    cursor = conn.cursor(dictionary=True)

    # SQL Query
    sql = """
            SELECT user_message, response
            FROM message_history
            WHERE email = %s
            ORDER BY timestamp ASC
        """

    # Create chat history list
    chat_history = []

    # Initialize the query
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

# Poke user memory for a row
def poke_user_memory(email):
    # Initialize DB connection
    conn = initialize_database_connection()

    # Intitialize Cursor
    cursor = conn.cursor()

    # SQL query
    sql = "SELECT 1 FROM user_memory WHERE email = %s LIMIT 1"

    # Execute
    try:
        cursor.execute(sql, (email, ))
        row = cursor.fetchone()
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

    return bool(row)

# Initialize a user's long term memory
def initialize_user_memory(email):
    # Initialize DB connection
    conn = initialize_database_connection()

    # Initialize Cursor
    cursor = conn.cursor()

    # Query
    sql = """
        INSERT INTO user_memory (email, memory_summary)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            memory_summary = memory_summary
    """

    # Execute
    try:
        cursor.execute(sql, (email, "NO MEMORY"))
        conn.commit()
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
    

# Manipulate the user long term memory
def manipulate_user_memory(message, response, email):
    # Get old memory
    old_memory = pull_user_memory(email)

    # Pull the system prompt from my .txt file
    memory_prompt_file = Path("app/prompts/memory_prompt.txt")
    if not memory_prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {memory_prompt_file}")
    system_prompt = memory_prompt_file.read_text("utf-8")
    
    # Combine the question and response to create new_memory
    new_entry = f"Question: {message} Response: {response} Old Memory: {old_memory}"

    # Build the API query
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Data
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{new_entry}"}
        ]
    }

    # Run the post request
    api_response = requests.post(url, headers=headers, json=data)
    api_response.raise_for_status()
    result = api_response.json()

    # Check if 'choices' exists
    if "choices" not in result or len(result["choices"]) == 0:
        raise ValueError(f"Unexpected API response: {result}")

    # Extract new memory
    new_memory = result["choices"][0]["message"]["content"].strip()

    # Did the memory get changed?
    if new_memory.strip() == old_memory.strip():
        return
    
    # Is the new memory too long?
    if len(new_memory) > 2000:
        return
    
    # Initialize connection
    conn = initialize_database_connection()

    # Initialize cursor
    cursor = conn.cursor()

    # Query
    sql = """
        INSERT INTO user_memory (email, memory_summary)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            memory_summary = VALUES(memory_summary),
            updated_at = CURRENT_TIMESTAMP
    """

    # Execute
    try:
        cursor.execute(sql, (email, new_memory))
        conn.commit()
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