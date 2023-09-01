from peewee import *
from flask import request, jsonify
from ..models.createTables import db
from ..models.users import User
from ..models.posts import Post
from ..models.messages import Message
from ..models.comments import Comment
from ..models.chatrooms import Chatroom
from ..models.followers import Follower
from ..models.usersChatrooms import UsersChatroom
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
            {'username' : 'user3', 'password' : 'password3'},
            {'username' : 'user4', 'password' : 'password4'},
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
        third_user = User.get(User.username == 'user3')
        fourth_user = User.get(User.username == 'user4')

        users = [
            first_user,
            sec_user,
            third_user,
            fourth_user,
        ]

        for user in users:
            post = Post.create(
                user=user,
                caption='Wow are these four posts exactly the same.',
                image_url='https://gogocdn.net/cover/86.png',
                timestamp=datetime.utcnow(),
            )
            print(f"User '{user.username}' just sent this.")

def seed_followers():
    with db.atomic():
        first_user = User.get(User.username == 'user1')
        sec_user = User.get(User.username == 'user2')
        third_user = User.get(User.username == 'user3')
        fourth_user = User.get(User.username == 'user4')

        first_follower_relation = Follower.create(
            follower=first_user,
            followee=sec_user,
        )
        sec_follower_relation = Follower.create(
            follower=sec_user,
            followee=first_user, 
        )        
        third_follower_relation = Follower.create(
            follower=third_user,
            followee=fourth_user,
        )        
        fourth_follower_relation = Follower.create(
            follower=fourth_user,
            followee=third_user,
        )
        fifth_follower_relation = Follower.create(
            follower=third_user,
            followee=first_user,
        )
        sixth_follower_relation = Follower.create(
            follower=fourth_user,
            followee=first_user,
        )
        seventh_follower_relation = Follower.create(
            follower=sec_user,
            followee=third_user,
        )
        eighth_follower_relation = Follower.create(
            follower=sec_user,
            followee=fourth_user,
        )
        print(f"If you see this : '{first_follower_relation.follower}' is a massive nerd.")

def seed_comments():
    with db.atomic():
        first_user = User.get(User.username == 'user1')
        sec_user = User.get(User.username == 'user2')
        third_user = User.get(User.username == 'user3')
        fourth_user = User.get(User.username == 'user4')

        first_post = Post.get(Post.user == first_user)
        sec_post = Post.get(Post.user == sec_user)
        third_post = Post.get(Post.user == third_user)
        fourth_post = Post.get(Post.user == fourth_user)

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
        fifth_comment = Comment.create(
            user=third_user,
            post=fourth_post,
            text='Honestly, I just think you are really cool.',
            timestamp=datetime.utcnow(),
        )
        sixth_comment = Comment.create(
            user=fourth_user,
            post=third_post,
            text='I read your comment on my post and I think you are really cool too.',
            timestamp=datetime.utcnow(),
        )
        print(f"If this worked you'll see this : '{fifth_comment.text}'")

def seed_chatrooms():
    with db.atomic():
        first_user = User.get(User.username == 'user1')
        sec_user = User.get(User.username == 'user2')
        
        dm_chatroom = Chatroom.create(
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name='XxXFrenemies4EverXxX',
            initiator=first_user,
            direct_receiver=sec_user,
        )

        # GC relations will be fleshed with UsersChatroom junction table
        group_chatroom = Chatroom.create(
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name='RevengersAssembled',
            initiator=first_user,
        )

def seed_messages():
    with db.atomic():
        # Dm Messages

        sender = User.get(User.username == 'user1')
        receiver = User.get(User.username == 'user2')

        dm_chatroom = Chatroom.get(Chatroom.name == 'dm_chatroom')

        dm_message = Message.create(
            chatroom=dm_chatroom,
            sender=sender,
            receiver=receiver,
            text='Don\'t tell the others but I actually follow you',
            timestamp=datetime.utcnow(),
        )

        