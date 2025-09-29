from json import JSONDecodeError

import json
import logging
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

from identman.helper.api import api
from identman.helper.helpers import Query
from identman.helper.decryption import decrypt
import threading
from fastapi import APIRouter, Depends, Request
import requests
from ..helper.settings import settings

logger = logging.getLogger("identman")
api_router = APIRouter(prefix="/api", tags=["items"])


sem = threading.Semaphore(5)

@api_router.get('')
def index(csrf_protect: CsrfProtect = Depends(), query: str | None = None):

    if not query:
        logger.debug("Hallo!!!!")
        return JSONResponse(status_code=404, content={})
    else:
        logger.debug("Hallo2")
        csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
        response = {"query": query, "nHash": settings.leading_zeros, "csrfToken": csrf_token, "signedToken": signed_token}
        csrf_protect.set_csrf_cookie(signed_token, JSONResponse(status_code=200, content=response))
        return response


@api_router.post('/challenge')
async def challenge(request: Request, csrf_protect: CsrfProtect = Depends()):
    request_data = await request.json()
    query = Query(**request_data)
    print(request.cookies)
    print(request_data)

    try:
        await csrf_protect.validate_csrf(request, cookie_key="csrfToken")
    except CsrfProtectError as e:
        return JSONResponse(status_code=416, content={"error": "CSRF Error Try again!"})
    if not query.validate():
        return JSONResponse(status_code=416, content={"error": "Nice try!"})
    try:
        plain = decrypt(settings.secret, query.get_query())
        data = json.loads(plain)
    except JSONDecodeError:
        return JSONResponse(status_code=416, content={"error": "Invalider QR Code"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"error": "Invalider QR Code"})
    
    if api.call(data):
        return data, 200
    return JSONResponse(status_code=400, content={"error": "Ist kein Aktives Mitglied der AG DSN!"})
