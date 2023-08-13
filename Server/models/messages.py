import os
from peewee import *
from dotenv import load_dotenv

load_dotenv()

db = PostgresqlDatabase(
    'trusting_wu',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)
