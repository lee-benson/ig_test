import os
from peewee import *
from dotenv import load_dotenv
from models.users import User
from models.posts import Post
from models.comments import Comment
from models.chatrooms import Chatroom
from models.messages import Message
from models.usersChatrooms import UsersChatroom
from models.followers import Follower

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)

# Create Tables

db.connect()
db.create_tables([User, Post, Follower, Comment, Chatroom, Message, UsersChatroom])
db.close()

# Next step would be to seed data/ create dummy data

# Remember to save data and close connection: .save() & db.close()
