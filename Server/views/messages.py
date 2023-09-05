from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from ..models.users import User
from ..models.chatrooms import Chatroom
from ..models.messages import Message
from ..models.usersChatrooms import UsersChatroom
from flask_socketio import emit
from . import socketio 
import os
import jwt
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

messages_bp = Blueprint('messages', __name__)

# GET uses chatroom id
@messages_bp.route('/<int:id>', methods=['GET'])
def get_messages(id):
    try:
        chatroom = Chatroom.select().where(Chatroom.id == id).get()
        if not chatroom:
            return jsonify({'error' : 'Chatroom not found'}), 404
        messages = [message.serialize() for message in chatroom.messages]
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# CREATE direct message chat uses username
@messages_bp.route('/<username>', methods=['POST'])
def create_direct_message(username):
    try:
        # Check if DM already exists
        # If true no DM: create DM, send message
        # If false: just send message

        user = token_user()
        receiver = User.select().where(User.username == username).get()
        
        chatroom = Chatroom.select().where(Chatroom.initiator == user, Chatroom.direct_receiver == receiver).get()
        
        # if user B sends message to user A, so username is user A
        # Check if the direct_receiver is himself
        initiator = User.select().where(User.username == username).get()
        chatroomReverse = Chatroom.select().where(Chatroom.initiator == initiator, Chatroom.direct_receiver == user).get()
        if not chatroom or not chatroomReverse:
            chatroom = Chatroom.create()
            UsersChatroom.create(user=user, chatroom=chatroom)
            UsersChatroom.create(user=receiver, chatroom=chatroom)

        data = request.json

        message = Message.create(
            chatroom=chatroom if chatroom else chatroomReverse,
            sender=user,
            receiver=receiver,
            text=data['text'],
            timestamp=datetime.utcnow(),
        )
        message_data = {
            'chatroom': chatroom.id if chatroom else chatroomReverse.id,
            'sender': user.id,
            'receiver': receiver.id,
            'text': data['text'],
            'timestamp': datetime.utcnow().isoformat(),
        }
        socketio.emit('new_message', message_data, room=f'chatroom_{chatroom.id}')
        return jsonify(message.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500



# CREATE group chat uses chatroom id
@messages_bp.route('/<int:id>', methods=['POST'])
def create_group_message(id):
    try:
        user = token_user()
        chatroom = Chatroom.select().where(Chatroom.id == id).get()
        if not chatroom:
            return jsonify({'error' : 'Chatroom not found'}), 404
        
        data = request.json

        # Determine list of receivers (including the sender)
        receivers = [users.user for users in chatroom.users]
        receivers.append(user)

        message = Message.create(
            chatroom=chatroom,
            sender=user,
            text=data['text'],
            timestamp=datetime.utcnow(),
        )
        message.receiver.add(receivers)
        return jsonify(message.serialize()), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# EDIT uses message id
@messages_bp.route('/<int:id>', methods=['PUT'])
def edit_message(id):
    try:
        user = token_user()
        message = Message.select().where(Message.id == id, Message.sender == user).get()
        if message.user != user:
            return jsonify({'error' : 'You do not have permission to delete this'}), 403
        
        data = request.json
        if 'text' in data:
            message.text = data['text']
        message.timestamp = datetime.utcnow()
        message.save()
        return jsonify(message.serialize()), 200
    except Message.DoesNotExist:
        return jsonify({'error' : 'Message not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    
# DELETE uses message id
@messages_bp.route('/<int:id>', methods=['DELETE'])
def delete_message(id):
    try:
        user = token_user()
        message = Message.select().where(Message.id == id, Message.user == user).get()
        if message.user != user:
            return jsonify({'error' : 'You do not have permission to delete this'}), 403
        message.delete()
        return jsonify({'message' : 'Message deleted successfully'}), 200
    except Message.DoesNotExist:
        return jsonify({'error' : 'Message not found'}), 404
    except Exception as e:
        return jsonify({'error' : str(e)}), 500