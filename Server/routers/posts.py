# CRUD for posts

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from posts import Post
from ..models.users import User
from ..models.followers import Follower

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

        return jsonify([post.serialize() for post in posts])
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    

@posts_bp.route('/:username', methods=['GET'])


