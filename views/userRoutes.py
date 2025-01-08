
from flask import Blueprint, request
import bcrypt
from models.userModel import UserModel
from utils.helpers import create_token, make_error_response, make_success_response



auth = Blueprint('auth', __name__, url_prefix='/auth')
userModel = UserModel()


@auth.route('/register', methods=['POST'])
def user_register():
    # get the user details from the request body
    payload = request.get_json()
    username = payload.get('username').lower()
    first_name = payload.get('firstName').lower()
    last_name = payload.get('lastName').lower()
    password = payload.get('password')
    email = payload.get('email')
    dob = payload.get('dob')
    
    # check if the user already exists
    if userModel.get_user_by_username(username):
        return 'User already exists', 409
    
    
    # hash the password
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # create a new user
    user_id = userModel.create_user({'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name,'email': email, 'dob': dob})



    # save the user details to the database
    return make_success_response(True, "User created successfully", data={"user_id":user_id}), 201

@auth.route('/login', methods=['POST'])
def user_login():
    # get the user details from the request body
    payload = request.get_json()
    identifier = payload.get('username')
    if not identifier:
        identifier = payload.get('email')
        if not identifier:
            return 'Username or email is required', 400
    
    password = payload.get('password')
    # get the user details from the database
    user = userModel.get_user_by_username( identifier.lower())
    # check if the user exists
    if not user:
        return 'User not found', 404
    # check if the password is correct
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return 'Invalid credentials', 401
    # create a tokenp
    token = create_token(user)
    # return the token
    
    return make_success_response(True, "Login Successful", data={"token":token}), 200