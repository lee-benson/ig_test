import os
from peewee import *
from dotenv import load_dotenv
from datetime import datetime
import users

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)


class Chatroom(Model):
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    name = CharField(default='Chat')
    initiator = ForeignKeyField(users.User, backref='dm_initiated', null=True)
    direct_receiver = ForeignKeyField(users.User, backref='dm_received', null=True)

    class Meta:
        database = db
