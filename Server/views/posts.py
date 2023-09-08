# CRUD for posts

from flask import Blueprint, request, jsonify, json
from datetime import datetime, timedelta
from posts import Post
from ..models.users import User
from ..models.followers import Follower
from ..cache.redis_cache import *
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

        if 'username' in data:
            username = data['username']

        user = User.select().where(User.username == username).get()

        # Create list of users the current user is following

        followees = [follower.followee for follower in user.following]

        # Query followee's posts ('<<' means included)
        # Adding redis cache

        post_cache_key = f'cache_key_post_user_{user.id}'
        cached_posts = get_data_from_cache(post_cache_key)
        # The cached data exists 
        if cached_posts is not None:
            posts = json.loads(cached_posts)
        else:
            posts = Post.select().where(Post.user << followees).order_by(Post.timestamp.desc())
            posts = [post.serialize() for post in posts]

            # Store fetched data into redis cache
            set_data_in_cache(post_cache_key, posts_ttl, json.dumps(posts))

        #  Return serialized data back to client

        return jsonify(posts), 200
    except User.DoesNotExist:
        return jsonify({'error' : 'User not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    

# Get someone else' posts
@posts_bp.route('/<username>', methods=['GET'])
def get_user_posts():
    try:
        username = request.args.get('username')

        user = User.select().where(User.username == username).get()

        posts = Post.select().where(Post.user << user).order_by(Post.timestamp.desc())

        return jsonify({[post.serialize() for post in posts]}), 200
    except User.DoesNotExist:
        return jsonify({'error' : 'User not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# Create Posts
@posts_bp.route('/', methods=['POST'])
def create_post():
    try:
        user = token_user()
        data = request.json
        post = Post.create(
            user=user,
            caption=data.get('caption', ''),
            image_url=data['image_url'],
            timestamp=datetime.utcnow()
            )
        return jsonify(post.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# Update Post
@posts_bp.route('/<int:id>', methods=['PUT'])
def update_post(id):
    try:
        # Verify first (Will have a separate middleware verification as well)
        user = token_user()

        # Find post by id and user

        post = Post.select().where(Post.id == id, Post.user == user).get()
        
        if post.user != user:
            return jsonify({'error' : 'You do not have permission to update this post'}), 403
        # After retrieving post add the changes

        data = request.json

        if 'caption' in data: 
            post.caption = data['caption']
        if 'image_url' in data:
            post.image_url = data['image_url']
        post.timestamp = datetime.utcnow()
        post.save()
        return jsonify(post.serialize()), 200
    except Post.DoesNotExist:
        return jsonify({'error' : 'Post not found'}), 404
    except Exception as e: 
        return jsonify({'error' : str(e)}), 500

# Delete post
@posts_bp.route('/<int:id>', methods=['DELETE'])
def delete_post(id):
    try:
        user = token_user()
        post = Post.select().where(Post.id == id, Post.user == user).get()

        if post.user != user:
            return jsonify({'error' : 'You do not have permission to delete this post'}), 403
        post.delete()
        return jsonify({'message' : 'Post deleted successfully'}), 200
    except Post.DoesNotExist:
        return jsonify({'error' : 'Post not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

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



