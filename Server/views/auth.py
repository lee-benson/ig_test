# CREATE user (Created through the signup process)

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv
from models.users import User
import os
import bcrypt
import jwt

load_dotenv()

auth_bp = Blueprint('auth', __name__)

TOKEN_KEY = os.environ.get('TOKEN_KEY')

# Function to generate JWT Token

def generate_token(user):
    payload = {
       'user_id': user.id,
       'exp': datetime.utcnow() + timedelta(minutes=30) 
    }
    token = jwt.encode(payload, TOKEN_KEY, algorithm='HS256')
    return token

# Define signup and login functions

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        # Hash password

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create user
        user = User.create(username=username, password=hashed_password)
        token = generate_token(user.id)
        return jsonify({'token' : token})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500 

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        # Find user

        user = User.select().where(User.username == username).get()

        # Verify password

        verify_status = bcrypt.checkpw(password.encode('utf-8'), user.password)
        if user and verify_status:
            token = generate_token(user.id)
            return jsonify({'token' : token})
        else:
            return jsonify({'error' : 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error' : str(e)}), 500




    



