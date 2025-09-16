import sys
from configparser import ConfigParser

#from flask import Flask
#from flask_cors import CORS
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect

from identman.helper.settings import settings
from identman.blueprints import api_router




def create_app():
    #app = Flask(__name__)
    #CORS(app, resources={r"/api/*": {"origins": "*"}})
    app = FastAPI()
    app.include_router(api_router, prefix="/api")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @CsrfProtect.load_config
    def get_csrf_config():
        return settings.csrf_settings

    #app.register_blueprint(bp)
    return app
