# CRUD
# Create is for group chat (For DM see routers/messages)

from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models.chatrooms import Chatroom
from ..models.users import User
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
@chatrooms_bp.rotue('/<username>', methods=['GET'])
def get_all_chatrooms(username):
    try:
        user = token_user()
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
