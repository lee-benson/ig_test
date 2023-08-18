# CREATE user

from flask import Blueprint, request, jsonify
import bcrypt
import jwt



auth_bp = Blueprint('auth', __name__)
