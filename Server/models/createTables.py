import os
from peewee import *
from dotenv import load_dotenv
import users
import posts
import comments
import chatrooms
import messages
import usersChatrooms
import followers

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
db.create_tables([users.User, posts.Post, followers.Follower, comments.Comment, chatrooms.Chatroom, messages.Message, usersChatrooms.UsersChatroom])
db.close()

# Next step would be to seed data/ create dummy data

# Remember to save data and close connection: .save() & db.close()
