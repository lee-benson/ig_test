import os
from peewee import *
from playhouse.migrate import *
from dotenv import load_dotenv


load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)

# Defining migrator
migrator = PostgresqlMigrator(db)

if __name__ == '__main__':
    migrator.run()