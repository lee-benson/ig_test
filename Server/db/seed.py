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
            print(f"User '{user.username}' just sent this.")

def seed_comments():
    with db.atomic():
        first_user = User.get(User.username == 'user1')
        sec_user = User.get(User.username == 'user2')

        first_post = Post.get(Post.user == first_user)
        sec_post = Post.get(Post.user == sec_user)

        first_comment = Comment.create(
            user=first_user,
            post=sec_post,
            text='You stole my post bruh. The lack of originality is appalling.',
            timestamp=datetime.utcnow(),
        )
        sec_comment = Comment.create(
            user=first_user,
            post=sec_post,
            text='Actually, I\'m not even that mad because it\'s a nice post.',
            timestamp=datetime.utcnow(),
        )
        third_comment = Comment.create(
            user=sec_user,
            post=sec_post,
            text='You stole my post @first_user. The lack of originality is appalling.',
            timestamp=datetime.utcnow(),
        )
        fourth_comment = Comment.create(
            user=sec_user,
            post=first_post,
            text='You stole my post bruh. The lack of originality is appalling.',
            timestamp=datetime.utcnow(),
        )
        print(f"If this worked you'll see this : '{fourth_comment.text}'")


        



        