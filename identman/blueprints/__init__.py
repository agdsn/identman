from json import JSONDecodeError

#from flask import render_template, Blueprint, request, redirect, jsonify, current_app
import json

from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from identman.helper.api import api
from identman.helper.helpers import Query
from identman.helper.csrf import get_token, get_token_csrf
from identman.helper.decryption import decrypt
import threading
from fastapi import APIRouter, Depends
import requests
from ..helper.settings import settings


#bp = Blueprint('api', __name__, url_prefix='/api')

api_router = APIRouter(prefix="/api", tags=["items"])


sem = threading.Semaphore(5)

@api_router.get('')
def index(csrf_protect: CsrfProtect = Depends()):
    if not requests.args.get('query'):
        return JSONResponse(status_code=404, content={})
    else:
        csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
        response = {"query": requests.args.get('query'), "nHash": settings.leading_zeros, "csrfToken": csrf_token}
        csrf_protect.set_csrf_cookie(signed_token, response)
        return JSONResponse(status_code=200, content=response)


@api_router.post('/challenge')
def challenge():
    request_data = requests.get_json()
    query = Query(**request_data)

    if not query.validate():
        return JSONResponse(status_code=416, content={"error": "Nice try!"})
    try:
        plain = decrypt(settings.secret, query.get_query())
        data = json.loads(plain)
    except JSONDecodeError:
        return {"error": "Invalider QR Code"}, 416
    except:
        return {"error": "Invalider QR Code"}, 400
    
    if api.call(data):
        return data, 200
    return {"error": "Ist kein Aktives Mitglied der AG DSN!"}, 400
