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
    try:
        yield connection
    finally:
        connection.close()

# Create db


def create_db():
    with connect_to_postgres() as connection:
        # Set connection to autocommit mode
        connection.autocommit = True
        # Create Cursor
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {db_name}")
        # Close cursor and disconnect
        cursor.close()


create_db()
