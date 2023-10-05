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
    print(f"Tracking token_key: {TOKEN_KEY}")

    token = jwt.encode(payload, TOKEN_KEY, algorithm='HS256')
    print(f"Tracking token: {token}")
    return token

# Define signup and login functions

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        print(f"Received username: {username}")
        print(f"Received password: {password}")

        # Hash password

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create user
        user = User.create(username=username, password=hashed_password)
        print(f"Created user: {user.username}")

        token = generate_token(user)
        print(f"Generated token: {token}")

        return jsonify({'token' : token})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500 

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        # Debug prints
        print(f"Received username: {username}")
        print(f"Received password: {password}")

        # Find user

        user = User.select().where(User.username == username).get()
        print(f"Received user: {user.username}")
        
        # Verify password

        print(f"Show user's password: {user.password}") # This was returned as string needs to be encoded in checkpw

        verify_status = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        print(f"Show verify_status: {verify_status}")
        if user and verify_status:
            token = generate_token(user)
            print(f"Show token: {token}")
            return jsonify({'token' : token})
        else:
            return jsonify({'error' : 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error' : str(e)}), 500




    



