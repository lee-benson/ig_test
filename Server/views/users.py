# CRUD for users (Primarily the GET)

from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from models.users import User
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

users_bp = Blueprint('users', __name__ )

# Deletes User
@users_bp.route('/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        user = token_user()
        if user.username != username:
            return jsonify({'error' : 'You do not have permission to delete this account'}), 403
        user.delete()
        return jsonify({'message' : 'Account deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
