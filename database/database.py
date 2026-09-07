import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Return a MySQL connection, or None if the connection fails."""
    # Connection details are kept in .env so they are not hard-coded in the app.
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", 3306),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        if connection.is_connected():
            return connection
        return None
    except Error as error:
        print(f"Error connecting to MySQL database: {error}")
        return None
