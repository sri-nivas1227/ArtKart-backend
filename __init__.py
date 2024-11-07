from flask import Flask
from .authentication import auth
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.register_blueprint(auth)
    @app.route('/')
    def hello():
        return 'Hello, World!'
    return app

