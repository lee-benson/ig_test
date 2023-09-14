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
 
# Creates association between users and their chatrooms
class UsersChatroom(Model):
    user = ForeignKeyField(users.User, backref='chatrooms')
    chatroom = ForeignKeyField(chatrooms.Chatroom, backref='users')

    class Meta:
        database = db
