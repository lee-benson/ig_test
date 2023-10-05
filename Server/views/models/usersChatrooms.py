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
 
# Creates association between users and their chatrooms
class UsersChatroom(Model):
    user = ForeignKeyField(User, backref='chatrooms')
    chatroom = ForeignKeyField(Chatroom, backref='users')

    class Meta:
        database = db

print("models/usersChatroom executed")