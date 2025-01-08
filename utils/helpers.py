from flask import jsonify
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def create_token(user):
    # creating a token valid for 7 days
    print(user)
    payload = {
        'id': str(user["_id"]),
        'email': user["email"],
        'username': user["username"],
    }
    print(payload)
    print(os.getenv('JWT_SECRET'))
    return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def make_success_response(success, message="Success", data=None):
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    })

def make_error_response(message="Error", data=None):
    return jsonify({
        'success': False,
        'message': message,
        'data': data
    })