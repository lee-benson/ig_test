from peewee import *
from flask import request, jsonify
import models
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
    with models.createTables.db.atomic():
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

            user = models.User.create(username=username, password=hashed_password)
            token = generate_token(user)
            print(f"User '{username}' with token : '{token}' has been created.")

def seed_posts():
    with models.createTables.db.atomic():
        
        first_user = models.users.User.get(models.users.User.username == 'user1')
        sec_user = models.users.User.get(models.users.User.username == 'user2')
        third_user = models.users.User.get(models.users.User.username == 'user3')
        fourth_user = models.users.User.get(models.users.User.username == 'user4')

        users = [
            first_user,
            sec_user,
            third_user,
            fourth_user,
        ]

        for user in users:
            post = models.posts.Post.create(
                user=user,
                caption='Wow are these four posts exactly the same.',
                image_url='https://gogocdn.net/cover/86.png',
                timestamp=datetime.utcnow(),
            )
            print(f"User '{user.username}' just sent this.")

def seed_followers():
    with models.createTable.db.atomic():
        first_user = models.users.User.get(models.users.User.username == 'user1')
        sec_user = models.users.User.get(models.users.User.username == 'user2')
        third_user = models.users.User.get(models.users.User.username == 'user3')
        fourth_user = models.users.User.get(models.users.User.username == 'user4')

        first_follower_relation = models.followers.Follower.create(
            follower=first_user,
            followee=sec_user,
        )
        sec_follower_relation = models.followers.Follower.create(
            follower=sec_user,
            followee=first_user, 
        )        
        third_follower_relation = models.followers.Follower.create(
            follower=third_user,
            followee=fourth_user,
        )        
        fourth_follower_relation = models.followers.Follower.create(
            follower=fourth_user,
            followee=third_user,
        )
        fifth_follower_relation = models.followers.Follower.create(
            follower=third_user,
            followee=first_user,
        )
        sixth_follower_relation = models.followers.Follower.create(
            follower=fourth_user,
            followee=first_user,
        )
        seventh_follower_relation = models.followers.Follower.create(
            follower=sec_user,
            followee=third_user,
        )
        eighth_follower_relation = models.followers.Follower.create(
            follower=sec_user,
            followee=fourth_user,
        )
        print(f"If you see this : '{first_follower_relation.follower}' is a massive nerd.")

def seed_comments():
    with models.createTables.db.atomic():
        first_user = models.users.User.get(models.users.User.username == 'user1')
        sec_user = models.users.User.get(models.users.User.username == 'user2')
        third_user = models.users.User.get(models.users.User.username == 'user3')
        fourth_user = models.users.User.get(models.users.User.username == 'user4')

        first_post = models.posts.Post.get(models.posts.Post.user == first_user)
        sec_post = models.posts.Post.get(models.posts.Post.user == sec_user)
        third_post = models.posts.Post.get(models.posts.Post.user == third_user)
        fourth_post = models.posts.Post.get(models.posts.Post.user == fourth_user)

        first_comment = models.comments.Comment.create(
            user=first_user,
            post=sec_post,
            text='You stole my post bruh. The lack of originality is appalling.',
            timestamp=datetime.utcnow(),
        )
        sec_comment = models.comments.Comment.create(
            user=first_user,
            post=sec_post,
            text='Actually, I\'m not even that mad because it\'s a nice post.',
            timestamp=datetime.utcnow(),
        )
        third_comment = models.comments.Comment.create(
            user=sec_user,
            post=sec_post,
            text='You stole my post @first_user. The lack of originality is appalling.',
            timestamp=datetime.utcnow(),
        )
        fourth_comment = models.comments.Comment.create(
            user=sec_user,
            post=first_post,
            text='You stole my post bruh. The lack of originality is appalling.',
            timestamp=datetime.utcnow(),
        )
        fifth_comment = models.comments.Comment.create(
            user=third_user,
            post=fourth_post,
            text='Honestly, I just think you are really cool.',
            timestamp=datetime.utcnow(),
        )
        sixth_comment = models.comments.Comment.create(
            user=fourth_user,
            post=third_post,
            text='I read your comment on my post and I think you are really cool too.',
            timestamp=datetime.utcnow(),
        )
        print(f"If this worked you'll see this : '{fifth_comment.text}'")

def seed_chatrooms():
    with models.createTables.db.atomic():
        first_user = models.users.User.get(models.users.User.username == 'user1')
        sec_user = models.users.User.get(models.users.User.username == 'user2')

        dm_chatroom = models.chatrooms.Chatroom.create(
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name='XxXFrenemies4EverXxX',
            initiator=first_user,
            direct_receiver=sec_user,
        )

        # GC relations will be fleshed with UsersChatroom junction table
        group_chatroom = models.chatrooms.Chatroom.create(
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name='RevengersAssembled',
            initiator=first_user,
        )
        print(f"Chatroom seeding worked : '{dm_chatroom.name}'.")

def seed_users_chatrooms():
    with models.createTables.db.atomic():
        first_user = models.users.User.get(models.users.User.username == 'user1')
        sec_user = models.users.User.get(models.users.User.username == 'user2')
        third_user = models.users.User.get(models.users.User.username == 'user3')
        fourth_user = models.users.User.get(models.users.User.username == 'user4')

        dm_chatroom = models.chatrooms.hatroom.get(models.chatrooms.Chatroom.name == 'XxXFrenemies4EverXxX')
        group_chatroom = models.chatrooms.Chatroom.get(models.chatrooms.Chatroom.name == 'RevengersAssembled')

        dm_chatroom_first_user = models.usersChatrooms.UsersChatroom.create(
            user=first_user,
            chatroom=dm_chatroom,
        )
        dm_chatroom_sec_user = models.usersChatrooms.UsersChatroom.create(
            user=sec_user,
            chatroom=dm_chatroom,
        )

        # Group chat
        group_chatroom_first_user = models.usersChatrooms.UsersChatroom.create(
            user=first_user,
            chatroom=group_chatroom,
        )
        group_chatroom_sec_user = models.usersChatrooms.UsersChatroom.create(
            user=sec_user,
            chatroom=group_chatroom,
        )
        group_chatroom_third_user = models.usersChatrooms.UsersChatroom.create(
            user=third_user,
            chatroom=group_chatroom,
        )
        group_chatroom_fourth_user = models.usersChatrooms.UsersChatroom.create(
            user=fourth_user,
            chatroom=group_chatroom,
        )
        print(f"UsersChatroom works and : '{group_chatroom_first_user.chatroom}' sucks.")

def seed_messages():
    with models.createTables.db.atomic():
        # Dm Messages

        first_user = models.users.User.get(models.users.User.username == 'user1')
        sec_user = models.users.User.get(models.users.User.username == 'user2')
        third_user = models.users.User.get(models.users.User.username == 'user3')
        fourth_user = models.users.User.get(models.users.User.username == 'user4')

        dm_chatroom = models.chatrooms.Chatroom.get(models.chatrooms.Chatroom.name == 'XxXFrenemies4EverXxX')
        group_chatroom = models.chatrooms.Chatroom.get(models.chatrooms.Chatroom.name == 'RevengersAssembled')

        first_dm_message = models.messages.Message.create(
            chatroom=dm_chatroom,
            sender=first_user,
            receiver=sec_user,
            text='Don\'t tell the others but I actually follow you',
            timestamp=datetime.utcnow(),
        )
        sec_dm_message = models.messages.Message.create(
            chatroom=dm_chatroom,
            sender=sec_user,
            receiver=first_user,
            text='Yeah I got you. Secret best buddies.',
            timestamp=datetime.utcnow(),
        )
        third_dm_message = models.messages.Message.create(
            chatroom=dm_chatroom,
            sender=sec_user,
            receiver=first_user,
            text='The bestest of friends, our bond is one of a kind.',
            timestamp=datetime.utcnow(),
        )
        fourth_dm_message = models.messages.Message.create(
            chatroom=dm_chatroom,
            sender=first_user,
            receiver=sec_user,
            text='Please never string those words in that order ever again.',
            timestamp=datetime.utcnow(),
        )
        fifth_dm_message = models.messages.Message.create(
            chatroom=dm_chatroom,
            sender=sec_user,
            receiver=first_user,
            text='A kind bond, of our friends one is of the bestest.',
            timestamp=datetime.utcnow(),
        )
        sixth_dm_message = models.messages.Message.create(
            chatroom=dm_chatroom,
            sender=first_user,
            receiver=sec_user,
            text='I can\'t say it\'s been nice knowing you because it hasn\'t been. Unfollowed.',
            timestamp=datetime.utcnow(),
        )

        # Group chat messages 
        first_group_message = models.messages.Message.create(
            chatroom=group_chatroom,
            sender=first_user,
            receiver=[first_user, sec_user, third_user, fourth_user],
            text='Does this thing work?',
            timestamp=datetime.utcnow(),
        )
        sec_group_message = models.messages.Message.create(
            chatroom=group_chatroom,
            sender=sec_user,
            receiver=[first_user, sec_user, third_user, fourth_user],
            text='Does it?',
            timestamp=datetime.utcnow(),
        )
        third_group_message = models.messages.Message.create(
            chatroom=group_chatroom,
            sender=third_user,
            receiver=[first_user, sec_user, third_user, fourth_user],
            text='I mean yeah I can see your messages.',
            timestamp=datetime.utcnow(),
        )
        fourth_group_message = models.messages.Message.create(
            chatroom=group_chatroom,
            sender=fourth_user,
            receiver=[first_user, sec_user, third_user, fourth_user],
            text='It\'s a Christmas miracle that this works.',
            timestamp=datetime.utcnow(),
        )
        fifth_group_message = models.messages.Message.create(
            chatroom=group_chatroom,
            sender=first_user,
            receiver=[first_user, sec_user, third_user, fourth_user],
            text='Hey fourth_user, you\'re lack of faith is showing.',
            timestamp=datetime.utcnow(),
        )
        print(f"Please work for the love of baby Jesus : '{fourth_group_message.text}'")



seed_users()
seed_posts()
seed_followers()
seed_comments()
seed_chatrooms()    
seed_users_chatrooms()
seed_messages()
models.createTables.db.close()
