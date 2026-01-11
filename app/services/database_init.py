# Imports
import os
import mysql.connector

def initialize_database_connection():
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