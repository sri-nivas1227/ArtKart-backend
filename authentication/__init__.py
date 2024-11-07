
from flask import Blueprint, request
from ..db import ArtKartUsers

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['POST'])
def user_register():
    # get the user details from the request body
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')
    # check if the user already exists
    if ArtKartUsers.find_one({'username': username}):
        return 'User already exists', 409
    # create a new user
    ArtKartUsers.insert_one({'username': username, 'password': password})
    
    # save the user details to the database
    return 'User registered', 201

@auth.route('/login', methods=['POST'])
def user_login():
    # get the user details from the request body
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')
    # authenticate the user
    if username == 'admin' and password == 'admin':
        return 'Login successful', 200
    else:
        return 'Login failed', 401
