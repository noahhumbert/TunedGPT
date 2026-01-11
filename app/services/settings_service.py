# Imports
from mysql.connector import Error
from datetime import datetime

# Pull in database initialization
from app.services.database_init import initialize_database_connection
    

def poke_styles(email: str):
    # Initialize Connection
    conn = initialize_database_connection()

    # SQL Query
    sql = "SELECT 1 FROM user_chat_settings WHERE email = %s LIMIT 1"

    # Initialize Cursor
    cursor = conn.cursor()

    # Execute Query 
    try:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
    # Except any errors
    except Error as e:
        print(f"[poke_styles] Database error: {e}")
        return False  # assume no styles if DB fails
    # Finally close teh SQL session
    finally:
        cursor.close()
        conn.close()

    return result is not None

def initialize_user_styles(email):
    # Initialize database connection
    conn = initialize_database_connection()

    # Initialize Cursor
    cursor = conn.cursor()

    # Default CSS values
    DEFAULT_STYLES = {
        "chat_name": "TunedGPT",
        "chat_header_background": "#000000",
        "chat_header_text": "#FFFFFF",
        "settings_button_background": "#000000",
        "settings_button_text": "#FFFFFF",
        "settings_button_border": "#FFFFFF",
        "settings_button_hover_background": "#FFFFFF",
        "settings_button_hover_text": "#000000",
        "settings_button_hover_border": "#000000",
        "user_message_text": "#FFFFFF",
        "user_message_background": "#000000",
        "ai_message_text": "#000000",
        "ai_message_background": "#FFFFFF",
        "chat_background_color": "#DCE1E6",
        "chat_footer_background": "#000000",
        "chat_textbox_background": "#000000",
        "chat_textbox_text": "#FFFFFF",
        "chat_textbox_border": "#FFFFFF",
        "chat_textbox_focus_background": "#FFFFFF",
        "chat_textbox_focus_text": "#000000",
        "chat_textbox_focus_border": "#000000",
        "chat_dropdown_background": "#000000",
        "chat_dropdown_text": "#FFFFFF",
        "submit_button_background": "#000000",
        "submit_button_text": "#FFFFFF",
        "submit_button_border": "#FFFFFF",
        "submit_button_hover_background": "#FFFFFF",
        "submit_button_hover_text": "#000000",
        "submit_button_hover_border": "#000000"
    }

    # Build Query Dynamically
    columns = ["email"] + list(DEFAULT_STYLES.keys())
    values_placeholders = ["%s"] * len(columns)
    values = [email] + list(DEFAULT_STYLES.values())

    # SQL Query
    sql = f"INSERT INTO user_chat_settings ({', '.join(columns)}) VALUES ({', '.join(values_placeholders)})"

    # Execute
    try:
        cursor.execute(sql, values)
        conn.commit()
        print(f"Initialized default styles for {email}.")
    # Except any errors
    except Error as e:
        print(f"[initialize_user_styles] Database error: {e}")
    # Finally close connection
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def pull_styles(email):
    # Initialize Connection
    conn = initialize_database_connection()

    # Initialize Cursor
    cursor = conn.cursor(dictionary=True)

    # Query
    sql = "SELECT * FROM user_chat_settings WHERE email = %s"

    # Execute Query
    try:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
    # Except any errors
    except Error as e:
        print(f"[load_styles] Database error: {e}")
        return {}
    # Finally close the connection
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if result:
        # Remove email and timestamps if you don't want them in the CSS dict
        result.pop("email", None)
        result.pop("created_at", None)
        result.pop("updated_at", None)
        return result
    else:
        return {}
    
def push_settings(email: str, settings: dict):
    # Initialize Connection
    conn = initialize_database_connection()

    # Initialize Cursor
    cursor = conn.cursor()

    # Build the Query
    set_clause = ", ".join(f"{key} = %s" for key in settings.keys())
    set_clause += ", updated_at = %s"  # add updated_at
    values = list(settings.values())
    values.append(datetime.utcnow())  # updated_at timestamp
    values.append(email)  # for WHERE clause

    # Query
    sql = f"""
            UPDATE user_chat_settings
            SET {set_clause}
            WHERE email = %s
        """

    # Execute
    try:
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(f"[push_settings] Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()