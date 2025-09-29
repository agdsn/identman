import os

#from flask import Flask
#from flask_cors import CORS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect

from identman.helper.settings import settings, Settings
from identman.blueprints import api_router




def create_app():
    #app = Flask(__name__)
    #CORS(app, resources={r"/api/*": {"origins": "*"}})
    print("ENV seen by OS:", os.environ.get("api__kind"))

    app = FastAPI()
    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @CsrfProtect.load_config
    def get_csrf_config():
        return settings.csrf_settings
    print(type(settings.api))
    #app.register_blueprint(bp)
    return app
