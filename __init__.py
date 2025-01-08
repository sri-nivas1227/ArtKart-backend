from flask import Flask
from views import register_rotues
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    CORS(app, origins=['http://localhost:3000'])
    register_rotues(app)
    @app.route('/')
    def hello():
        return 'Hello, World!'
    return app

