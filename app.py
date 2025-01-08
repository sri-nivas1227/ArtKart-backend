from flask import Flask
from views import register_rotues
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()
def create_app():

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    CORS(app, origins=os.getenv('ORIGINS'))
    register_rotues(app)
    @app.route('/')
    def hello():
        return 'Hello, World!'
    return app

