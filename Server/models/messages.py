import os
from peewee import *
from dotenv import load_dotenv
import users
import chatrooms

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)


class Message(Model):
    chatroom = ForeignKeyField(chatrooms.Chatroom, backref='messages')
    sender = ForeignKeyField(users.User, backref='messages_sent')
    receiver = ManyToManyField(users.User, backref='messages_received') # a receiver can receive multiple messages, a message can be for multiple receivers
    text = TextField()
    timestamp = DateTimeField()

    class Meta:
        database = db
