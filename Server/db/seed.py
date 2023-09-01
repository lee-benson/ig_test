from peewee import *
from flask import request, jsonify
from ..models.createTables import db
from ..models.users import User
from ..models.posts import Post
from ..models.messages import Message
from ..models.comments import Comment
from ..models.chatrooms import Chatroom
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import bcrypt
import jwt


load_dotenv()
TOKEN_KEY = os.environ.get('TOKEN_KEY')

def generate_token(user):
    payload = {
       'user_id': user.id,
       'exp': datetime.utcnow() + timedelta(minutes=30) 
    }
    token = jwt.encode(payload, TOKEN_KEY, algorithm='HS256')
    return token

# Seeding user data

def seed_users():
    with db.atomic():
        user_data = [
            {'username' : 'user1', 'password' : 'password1'},
            {'username' : 'user2', 'password' : 'password2'},
        ]

        for data in user_data:
            username = data['username']
            password = data['password']

            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            user = User.create(username=username, password=hashed_password)
            token = generate_token(user)
            print(f"User '{username}' with token : '{token}' has been created.")

def seed_posts():
    with db.atomic():
        
        first_user = User.get(User.username == 'user1')
        sec_user = User.get(User.username == 'user2')

        users = [
            first_user,
            sec_user,
        ]

        for user in users:
            post = Post.create(
                user=user,
                caption='Wow are these two posts exactly the same.',
                image_url='https://gogocdn.net/cover/86.png',
                timestamp=datetime.utcnow(),
            )
            print(f"User '{User.username}' just sent this.")


        



        