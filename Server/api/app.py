from flask import Flask, request
from ..models.createTables import db
from ..routers import auth_bp, users_bp, posts_bp, comments_bp, messages_bp, chatrooms_bp
from ..middleware import verify_auth


app = Flask(__name__)

# Register blueprints

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(chatrooms_bp)

@app.before_request
def before_request():
    if request.endpoint in ['CREATE', 'PUT', 'DELETE']:
        verify_auth()


if __name__ == "__main__":
    app.run()
