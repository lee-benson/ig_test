import os
from peewee import *
from dotenv import load_dotenv
from users import User
from chatrooms import Chatroom

load_dotenv()

db = PostgresqlDatabase(
    'trusting_wu',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)


class Message(Model):
    chatroom = ForeignKeyField(Chatroom, backref='messages')
    sender = ForeignKeyField(User, backref='messages_sent')
    receiver = ForeignKeyField(User, backref='messages_received')
    text = TextField()
    timestamp = DateTimeField()

    class Meta:
        database = db
