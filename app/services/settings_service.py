# Imports
import os
import mysql.connector
from mysql.connector import Error

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

def poke_styles(email: str):
    # Initialize Connection
    conn = initialize_message_database()

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

def intitialize_user_styles():
    print("initializing...")

def pull_styles():
    print("pulling...")