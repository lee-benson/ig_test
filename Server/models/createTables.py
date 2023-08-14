import os
from peewee import *
from dotenv import load_dotenv
from users import User
from posts import Post
from comments import Comment
from chatrooms import Chatroom
from messages import Message
from usersChatrooms import UsersChatroom

load_dotenv()

db = PostgresqlDatabase(
    'trusting_wu',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)

# Create Tables

db.connect()
db.create_tables([User, Post, Comment, Chatroom, Message, UsersChatroom])

# Next step would to seed data/ create dummy data
# Remember to save data and close connection: .save() & db.close()
