import os
from peewee import *
from dotenv import load_dotenv
import users

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)

# Creates a relationship between followers and followees
# To help establish homepage posts
# Assume user1 is an instance of User
# user1.following queries users that user1 is following (user1 is a follower)
# user1.followers queries users that follow user1 (user1 is a followee)

class Follower(Model):
    follower = ForeignKeyField(users.User, backref='following') 
    followee = ForeignKeyField(users.User, backref='followers')

    class Meta:
        database = db