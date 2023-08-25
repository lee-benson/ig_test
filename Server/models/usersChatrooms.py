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


class UsersChatroom(Model):
    user = ForeignKeyField(User, backref='chatrooms')
    chatroom = ForeignKeyField(Chatroom, backref='users')

    class Meta:
        database = db
