""" Top level module

This module:

- Contains create_app()
- Registers extensions
"""
from flask import Flask

import os
from .config import config_dict, config
from .extensions import api, db, migrate, register_error_handlers
from .files.routes import files_namespace


def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    initialize_storage(app)

    api.init_app(app)
    register_error_handlers(api)
    api.add_namespace(files_namespace)

    db.init_app(app)
    migrate.init_app(app, db)

    return app

def initialize_storage(app):
    """
    Initialize the storage folder
    """
    storage_path = os.path.join(os.getcwd(), config.STORAGE_FOLDER)
    if not os.path.exists(storage_path):
        os.makedirs(storage_path, exist_ok=True)
        app.logger.info(f"Storage folder created at {storage_path}")
    else:
        app.logger.info(f"Storage folder already exists at {storage_path}")
    app.config["UPLOAD_FOLDER"] = storage_path