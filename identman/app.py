from flask import Flask
from flask_cors import CORS
import logging



def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from identman import bp
    app.register_blueprint(bp)
    app.config.update()
    app.crftoken = []
    return app

def create_logger(level) -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)