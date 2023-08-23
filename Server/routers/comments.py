from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models.users import User
from ..models.posts import Post
from ..models.comments import Comment
import jwt
import os
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

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/<int:id>', methods=['POST'])
def create_comment(id):
    try:
        user = token_user()
        post = Post.select().where(Post.id == id).get()

        if not post:
            return jsonify({'error' : 'Post not found'}), 404

        data = request.json
        text = data['text']

        comment = Comment.create(
            user=user,
            post=post,
            text=text,
            timestamp=datetime.utcnow()
        )
        return jsonify(comment.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    
@comments_bp.route('/<int:id>', methods=['GET'])
def get_comments(id):
    try:
        post = Post.select().where(Post.id == id).get()
        if not post:
            return jsonify({'error' : 'Post not found'}), 404
        comment = post.comments
        return jsonify(comment.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500