import os
from peewee import *
from users import User
from messages import Message
from dotenv import load_dotenv

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)

class MessagesReceiver (Model):
    receiver = ForeignKeyField(User, backref='message_receiver')
    message = ForeignKeyField(Message, backref='message')

    class Meta:
        database = db
    
    def serialize(self):
        return {
            'id': self.id,
            'receiver': self.receiver,
            'message': self.message,
        }

print("models/messagesReceivers executed")
  