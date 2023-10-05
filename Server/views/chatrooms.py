# CRUD
# Create is for group chat (For DM see routers/messages)

from peewee import *
from flask import Blueprint, request, jsonify, json
from datetime import datetime
from models.users import User
from models.chatrooms import Chatroom
from cache.redis_cache import *
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)

TOKEN_KEY = os.environ.get('TOKEN_KEY')

# Function for importing userschatroom
def import_userschatroom():
    from models.usersChatrooms import UsersChatroom
    return UsersChatroom

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
        UsersChatroom = import_userschatroom()
        dm_initiate_chatrooms = Chatroom.select().where(Chatroom.initiator == user).get()
        dm_receive_chatrooms = Chatroom.select().where(Chatroom.direct_receiver == user).get()
        gc_chatrooms = Chatroom.select().join(UsersChatroom).where(
            UsersChatroom.user == user,
            UsersChatroom.chatroom == Chatroom.id
        )

        # Combine the chatrooms
        all_chatrooms = dm_initiate_chatrooms | dm_receive_chatrooms | gc_chatrooms
        
        # redis cache
        chat_cache_key = f'cache_key_chat_user_{user.id}'
        cached_chats = get_data_from_cache(chat_cache_key)
        if cached_chats is not None:
            chatrooms = json.loads(cached_chats)
        else:
            chatrooms = [chatroom.serialize() for chatroom in all_chatrooms]
            set_data_in_cache(chat_cache_key, chats_ttl, json.dumps(chatrooms))
            
        return jsonify(chatrooms), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# CREATE a chatroom (GC)
@chatrooms_bp.route('/', methods=['POST'])
def create_group_chatroom():
    try:
        user = token_user()
        UsersChatroom = import_userschatroom()
        data = request.json
        # Need to get participants from request data
        participants = data.get('participants', [])
        
        chatroom = Chatroom.create(
            name=data['name'],
            initiator=user,
        )

        # Add participants to the chatroom using the association table
        with db.atomic():
            for participant_id in participants:
                user_chatroom = UsersChatroom.create(user=participant_id, chatroom=chatroom)
                user_chatroom.save()
                
        return jsonify(chatroom.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
  
# UPDATE a chatroom (GC)
@chatrooms_bp.route('/<int:id>', methods=['PUT'])
def update_group_chatroom(id):
    try:
        user = token_user()
        chatroom = Chatroom.select().where(Chatroom.id == id).get()
        if user not in chatroom.users:
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
        if user not in chatroom.users:
            return jsonify({'error' : 'You are not in this chatroom'}), 403

        chatroom.users.remove(user)
        chatroom.save()
        return jsonify(chatroom.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

print("views/chatrooms executed")