from flask import Flask, request
from flask_socketio import SocketIO
import views 
import middleware

app = Flask(__name__)
socketio = SocketIO(app)

# Register blueprints

app.register_blueprint(views.auth_bp)
app.register_blueprint(views.users_bp)
app.register_blueprint(views.posts_bp)
app.register_blueprint(views.comments_bp)
app.register_blueprint(views.messages_bp)
app.register_blueprint(views.chatrooms_bp)

@app.before_request
def before_request():
    if request.endpoint in ['CREATE', 'PUT', 'DELETE']:
        # Middleware authentication
        middleware.verify_auth()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('new_message')
def handle_new_message(message_data):
    try:
        # Validating data
        if 'chatroom_id' in message_data and 'sender_id' in message_data and 'text' in message_data and 'timestamp' in message_data:
            chatroom_id = message_data['chatroom_id']
            socketio.emit('new_message', message_data, room=f'chatroom_{chatroom_id}')                
        else:
            print('Invalid message_data: Missing one or more required fields')
    except Exception as e:
        print(f'Error handling new message : {str(e)}')


if __name__ == "__main__":
    socketio.run(app, debug=True)
