import os
from peewee import *
from dotenv import load_dotenv
from users import User
from chatrooms import Chatroom


load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)


class Message(Model):
    chatroom = ForeignKeyField(Chatroom, backref='messages')
    sender = ForeignKeyField(User, backref='messages_sent')
    text = TextField()
    timestamp = DateTimeField()

    class Meta:
        database = db

    def serialize(self):
        return {
            'id': self.id,
            'chatroom': self.chatroom,
            'sender': self.sender,
            'text': self.text,
            'timestamp': self.timestamp,
        }

print("models/messages executed")