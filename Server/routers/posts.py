# CRUD for posts

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from posts import Post
from ..models.users import User
from ..models.followers import Follower
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_KEY = os.environ.get('TOKEN_KEY')

posts_bp = Blueprint('posts', __name__)

# Consider that you may be requesting:
# Homepage (Your) posts
# Someone else's posts
# Specific post

# Homepage posts
@posts_bp.route('/', methods=['GET'])
def get_posts():
    try:
        data = request.json
        username = data['username']

        user = User.select().where(User.username == username).get()

        # Create list of users the current user is following

        followees = [follower.followee for follower in user.following]

        # Query followee's posts ('<<' means included)

        posts = Post.select().where(Post.user << followees).order_by(Post.timestamp.desc())

        #  Return serialized data back to client

        return jsonify([post.serialize() for post in posts]), 200
    except User.DoesNotExist:
        return jsonify({'error' : 'User not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    

# Someone else' posts
@posts_bp.route('/<username>', methods=['GET'])
def get_user_post():
    try:
        username = request.args.get("username")

        user = User.select().where(User.username == username).get()

        posts = Post.select().where(Post.user << user).order_by(Post.timestamp.desc())

        return jsonify({[post.serialize() for post in posts]}), 200
    except User.DoesNotExist:
        return jsonify({'error' : 'User not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# Create post
@posts_bp.route('/', methods=['POST'])
def create_post():
    try:
        
        # Verify first (Will have a separate middleware verification as well)

        data = request.json
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error' : 'Missing authorization header'}), 401
        
        token = auth_header.split()[1] 
        decoded_token = jwt.verify(token, TOKEN_KEY)
        user = User.get(User.username == decoded_token.username)

        return jsonify(), 200
    except Exception as e: 
        return jsonify({'error' : str(e)}), 500


