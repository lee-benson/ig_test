from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from ..models.users import User
from ..models.chatrooms import Chatroom
from ..models.messages import Message
from ..models.usersChatrooms import UsersChatroom
import os
import jwt
from dotenv import load_dotenv

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

messages_bp = Blueprint('messages', __name__)

# GET uses chatroom id
@messages_bp.route('/<int:id>', methods=['GET'])
def get_messages(id):
    try:
        chatroom = Chatroom.select().where(Chatroom.id == id).get()
        if not chatroom:
            return jsonify({'error' : 'Chatroom not found'}), 404
        messages = [message.serialize() for message in chatroom.messages]
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# CREATE uses chatroom id
@messages_bp.route('/<int:id>', methods=['POST'])
def create_message(id):
    try:
        user = token_user()
        chatroom = Chatroom.select().where(Chatroom.id == id).get()
        if not chatroom:
            return jsonify({'error' : 'Chatroom not found'}), 404
        
        data = request.json
        
        receivers = [users.user for users in chatroom.users]

        message = Message.create(
            chatroom=chatroom,
            sender=user,
            receiver=receivers,
            text=data['text'],
            timestamp=datetime.utcnow(),
        )
        return jsonify(message.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500