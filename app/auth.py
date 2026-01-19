from functools import wraps
from flask import request, jsonify, session, redirect, url_for
import jwt
from datetime import datetime, timedelta
from config import Config
from models import User

def generate_token(user_id):
    """Generate JWT token for user."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """Verify JWT token and return user_id."""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid JWT token for API endpoints."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        # Check for token in session (for browser requests)
        if not token and 'token' in session:
            token = session['token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        user_id = verify_token(token)
        if not user_id:
            return jsonify({'message': 'Token is invalid or expired'}), 401

        current_user = User.find_by_id(user_id)
        if not current_user:
            return jsonify({'message': 'User not found'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def login_required(f):
    """Decorator to require login for web pages."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login'))

        user_id = verify_token(session['token'])
        if not user_id:
            session.pop('token', None)
            return redirect(url_for('login'))

        current_user = User.find_by_id(user_id)
        if not current_user:
            session.pop('token', None)
            return redirect(url_for('login'))

        return f(current_user, *args, **kwargs)

    return decorated
