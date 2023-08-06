import psycopg2
import os
import hashlib

# Load environment variables
db_user = os.environ.get('DB_USER')
db_pw = os.environ.get('DB_PW')


# Defining function for connection
def connect_to_postgres():
    connection = psycopg2.connect(
        dbname='postgres', user=db_user, password=db_pw, host='localhost', port='5432',
    )
    try:
        yield connection
    finally:
        connection.close()


def check_superuser_exists(username):
    # Establish connection to postgres db
    with connect_to_postgres() as connection:
        # Create cursor
        cursor = connection.cursor()

        # Execute sql query to check if superuser already exists
        cursor.execute(
            "SELECT rolname FROM pg_roles WHERE rolname = %s", (username,))
        superuser_exists = cursor.fetchone() is not None

        cursor.close()
    return superuser_exists


def create_superuser(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Establish connection to postgres db
    with connect_to_postgres() as connection:
        # Create cursor
        cursor = connection.cursor()

        try:
            # Execute parameterized sql queries to create superuser
            cursor.execute("CREATE USER %s WITH PASSWORD %s",
                           (username, hashed_password,))
            cursor.execute("ALTER USER %s WITH SUPERUSER", (username,))

            # Commit the changes
            connection.commit()
            print(f"Superuser '{username}' created successfully.")
        except Exception as e:
            print(f"Error occurred: {e}")
            connection.rollback()
        cursor.close()


superuser_username = os.environ.get('SUP_USER')
superuser_password = os.environ.get('SUP_USERPW')

if not check_superuser_exists(superuser_username):
    create_superuser(superuser_username, superuser_password)
else:
    print(f"The superuser '{superuser_username}' already exists.")
