from flask import Blueprint, request, jsonify, json
from datetime import datetime
from ..models.users import User
from ..models.posts import Post
from ..models.comments import Comment
from ..cache.redis_cache import *
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

# Uses post id
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

# Uses post id
@comments_bp.route('/<int:id>', methods=['GET'])
def get_comments(id):
    try:
        user = token_user()
        post = Post.select().where(Post.id == id).get()
        if not post:
            return jsonify({'error' : 'Post not found'}), 404
        
        # redis cache
        comment_cache_key = f'cache_key_comment_user_{user.id}'
        cached_comments = get_data_from_cache(comment_cache_key)
        if cached_comments is not None:
            comments = json.loads(cached_comments)
        else:
            comments = [comment.serialize() for comment in post.comments]
            set_data_in_cache(comment_cache_key, comments_ttl, json.dumps(comments))
          
        return jsonify(comments), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    
# Uses comment id
@comments_bp.route('/<int:id>', methods=['PUT'])
def edit_comment(id):
    try:
        user = token_user()
        comment = Comment.select().where(Comment.id == id, Comment.user == user).get()

        if comment.user != user:
            return jsonify({'error' : 'You do not have permission to change this'}), 403
        
        data = request.json

        if 'text' in data:
            comment.text = data['text']
        comment.timestamp = datetime.utcnow()
        comment.save()
        return jsonify(comment.serialize()), 200
    except Comment.DoesNotExist:
        return jsonify({'error' : 'Comment not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# Uses comment id
@comments_bp.route('/<int:id>', methods=['DELETE'])
def delete_comment(id):
    try:
        user = token_user()
        comment = Comment.select().where(Comment.id == id, Comment.user == user).get()
        if comment.user != user:
            return jsonify({'error' : 'You do not have permission to delete this'}), 403
    
        comment.delete()
        return jsonify({'message' : 'Comment deleted successfully'}), 200
    except Comment.DoesNotExist:
        return jsonify({'error' : 'Comment not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
        