
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
    email = payload.get('email').lower()
    dob = payload.get('dob')
    
    # check if the email already exists
    if userModel.get_user_by_username(email):
        return make_error_response(False, "User email already exists, please login."), 400
    # check if the user already exists
    if userModel.get_user_by_username(username):
        return make_error_response(False, "Username exists, pick another one."), 400
    
    
    # hash the password
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    success, data = userModel.create_user({'username': username, 'password': str(password), 'first_name': first_name, 'last_name': last_name,'email': email, 'dob': dob})
    # create a new user
    if not success:
        return make_error_response(False, data), 400
    user_id = data
    print(user_id, type(user_id))

    # save the user details to the database
    return make_success_response(True, "User created successfully", data={"user_id":str(user_id)}), 201

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