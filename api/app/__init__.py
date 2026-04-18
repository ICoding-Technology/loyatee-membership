import os
from flask import Flask
from flask_cors import CORS

from config import config
from app.extensions import init_db
from app.routes import register_blueprints
from app.controllers.errors import register_error_handlers


def create_app(config_name=None):
    app = Flask(__name__)
    config_name = config_name or os.getenv("FLASK_ENV", "default")
    app.config.from_object(config[config_name])

    CORS(app)
    init_db(app)

    register_blueprints(app)
    register_error_handlers(app)

    return app
