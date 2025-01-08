from flask import Blueprint
from userRoutes import auth

def register_rotues(app):
    app.register_blueprint(auth, url_prefix='/auth')
    