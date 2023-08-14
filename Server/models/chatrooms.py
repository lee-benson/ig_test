import os
from peewee import *
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

db = PostgresqlDatabase(
    'trusting_wu',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)


class Chatroom(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()

    class Meta:
        database = db
