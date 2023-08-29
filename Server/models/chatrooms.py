import os
from peewee import *
from dotenv import load_dotenv
from datetime import datetime
from users import User
from usersChatrooms import UsersChatroom

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
    name = CharField(default='Chat')
    participants = ManyToManyField(User, backref='chatrooms', through_model=UsersChatroom)
    initiator = ForeignKeyField(User, backref='dm_initiated', null=True)
    direct_receiver = ForeignKeyField(User, backref='dm_received', null=True)

    class Meta:
        database = db
