from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect
import logging

from identman.helper.settings import settings
from identman.blueprints import api_router




def create_app():
    app = FastAPI(title="Identman API", version="1.0")
    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logging.basicConfig(level=settings.get_loglevel())

    @CsrfProtect.load_config
    def get_csrf_config():
        return settings.csrf_settings
    return app
