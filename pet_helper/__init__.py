import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()
jwt = JWTManager()

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object("config.Config")
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cors.init_app(app, supports_credentials=True)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from .models import User, Pet, Event

        db.create_all()

        return app
