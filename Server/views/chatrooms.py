# CRUD
# Create is for group chat (For DM see routers/messages)

from peewee import *
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models.chatrooms import Chatroom
from ..models.users import User
from ..models.chatrooms import UsersChatroom
from ..models.createTables import db
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

TOKEN_KEY = os.environ.get('TOKEN_KEY')

# Get user from header
def token_user():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error' : 'Missing authorization header'}), 401
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, TOKEN_KEY, algorithms=['HS256'])
        user = User.get(User.id == decoded_token['user_id'])
        return user
    except User.DoesNotExist:
        return jsonify({'error' : 'User not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

chatrooms_bp = Blueprint('chatrooms', __name__)

# GET all chatrooms (DM & GC)
@chatrooms_bp.route('/', methods=['GET'])
def get_all_chatrooms():
    try:
        user = token_user()
        dm_initiate_chatrooms = Chatroom.select().where(Chatroom.initiator == user).get()
        dm_receive_chatrooms = Chatroom.select().where(Chatroom.direct_receiver == user).get()
        gc_chatrooms = Chatroom.select().join(UsersChatroom).where(
            UsersChatroom.user == user,
            UsersChatroom.chatroom == Chatroom.id
        )

        # Combine the chatrooms
        all_chatrooms = dm_initiate_chatrooms | dm_receive_chatrooms | gc_chatrooms
        
        chatroom_data = [chatroom.serialize() for chatroom in all_chatrooms]
        return jsonify(chatroom_data), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# CREATE a chatroom (GC)
@chatrooms_bp.route('/', methods=['POST'])
def create_group_chatroom():
    try:
        user = token_user()
        data = request.json
        
        # Need to get participants from request data
        chatroom = Chatroom.create(
            name=data['name'],
            participants=data['participants'],
        )
        return jsonify(chatroom.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
  
# UPDATE a chatroom (GC)
@chatrooms_bp.route('/<int:id>', methods=['PUT'])
def update_group_chatroom(id):
    try:
        user = token_user()
        chatroom = Chatroom.select().where(Chatroom.id == id).get()
        if user not in chatroom.participants:
            return jsonify({'error' : 'You do not have permission to edit this chatroom'}), 403
        
        data = request.json
        if 'name' in data:
            chatroom.name = data['name']
        chatroom.updated_at = datetime.utcnow()
        chatroom.save()
        return jsonify(chatroom.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# DELETE? removes yourself from participants
@chatrooms_bp.route('/<int:id>', methods=['DELETE'])
def leave_group_chatroom(id):
    try:
        user = token_user()
        chatroom = Chatroom.select().where(Chatroom.id == id).get()
        if user not in chatroom.participants:
            return jsonify({'error' : 'You are not in this chatroom'}), 403

        with db.atomic():
            chatroom.participants.remove(user)
            chatroom.save()
        return jsonify(chatroom.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500