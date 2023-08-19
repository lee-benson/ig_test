# CRUD for posts

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from posts import Post

posts_bp = Blueprint('posts', __name__)

# Consider that you may be requesting:
# Homepage (Your) posts
# Someone else's posts
# Specific post

# Homepage posts
@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    try:
        
    except Exception as e:
        return jsonify({'error' : str(e)}), 500