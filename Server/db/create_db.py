import psycopg2
import os


# Load the environment variables
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_pw = os.environ.get('DB_PW')

# Connect to postgres
# Defining function for connection


def connect_to_postgres():
    connection = psycopg2.connect(
        dbname='postgres', user=db_user, password=db_pw, host='localhost', port='5432',
    )
    return connection

# Create db


def create_db():
    connection = connect_to_postgres()
    # Set connection to autocommit mode
    connection.autocommit = True
    try:
        # Create Cursor
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {db_name}")
    finally:
        # Close cursor and disconnect
        cursor.close()
        connection.close()


create_db()
