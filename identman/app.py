import sys
from configparser import ConfigParser

from flask import Flask
from flask_cors import CORS
import os



def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from identman import bp
    app.register_blueprint(bp)
    get_config(app)
    app.crftoken = []
    return app

def get_config(app):
    config = ConfigParser()
    if key := os.environ.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = key
    else:
        sys.exit("there was no SECRET_KEY provided in env")

    if pyc_key := os.environ.get("PYCROFT_BACKEND_KEY"):
        app.config["PYCROFT_BACKEND_KEY"] = pyc_key
    else:
        sys.exit("there was no PYCROFT_BACKEND_KEY in env")

    if pycb := os.environ.get("PYCROFT_BACKEND"):
        app.config["PYCROFT_BACKEND"] = pycb
    else:
        sys.exit("there was no PYCROFT_BACKEND in env")

    return config
