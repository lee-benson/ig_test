import psycopg2
import os


# Load the environment variables
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_pw = os.environ.get('DB_PW')

# Connect to postgres
connection = psycopg2.connect(
    dbname='postgres', user=db_user, password=db_pw, host='172.17.0.2',
)

# Create Cursor

cursor = connection.cursor()

# Create db

cursor.execute(f"CREATE DATABASE {db_name}")

# Commit the changes

connection.commit()

# Close cursor and disconnect

cursor.close()
connection.close()
