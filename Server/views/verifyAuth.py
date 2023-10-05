from flask import request, jsonify
import models
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

TOKEN_KEY = os.environ.get('TOKEN_KEY')

def verify_auth():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401 
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, TOKEN_KEY, algorithms=['HS256'])
        user = models.users.User.get(models.users.User.id == decoded_token['user_id'])
        if not user:
            return jsonify({'message' : 'You need to be signed in to make this request'}), 401
    except Exception as e:
        return jsonify({'error : str(e)'}), 500

print("views/verify_Auth executed")
        