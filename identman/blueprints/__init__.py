from json import JSONDecodeError
import json
import logging

from cryptography.exceptions import InvalidTag
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

from identman.helper.api import api
from identman.helper.helpers import Query
from identman.helper.decryption import decrypt
from fastapi import APIRouter, Depends, Request
from ..helper.settings import settings, secrets

logger = logging.getLogger("identman")
api_router = APIRouter(prefix="/api", tags=["items"])


@api_router.get('')
def index(csrf_protect: CsrfProtect = Depends(), query: str | None = None):

    if not query:
        return JSONResponse(status_code=404, content={})
    else:
        csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
        response = {"query": query, "nHash": settings.leading_zeros, "csrfToken": csrf_token, "signedToken": signed_token}
        csrf_protect.set_csrf_cookie(signed_token, JSONResponse(status_code=200, content=response))
        return response


@api_router.post('/challenge')
async def challenge(request: Request, csrf_protect: CsrfProtect = Depends()):
    request_data = await request.json()
    query = Query(**request_data)
    logger.debug(f"Send Cookie data: {request.cookies}")
    logger.debug(f"Request data: {request_data}")

    try:
        await csrf_protect.validate_csrf(request, cookie_key="csrfToken")
    except CsrfProtectError:
        response = JSONResponse(
            status_code=416, content={"error": "CSRF Error Try again!"}
        )
        csrf_protect.unset_csrf_cookie(response)
        return response
    if not query.validate():

        response = JSONResponse(status_code=416, content={"error": "Nice try!"})
        csrf_protect.unset_csrf_cookie(response)
        return response
    try:
        plain = decrypt(secrets.secret, secrets.salt, query.get_query())
        data = json.loads(plain)
    except JSONDecodeError:
        response = JSONResponse(status_code=416, content={"error": "Invalider QR Code"})
        csrf_protect.unset_csrf_cookie(response)
        return response
    except InvalidTag:
        response = JSONResponse(status_code=400, content={"error": "Invalider QR Code"})
        csrf_protect.unset_csrf_cookie(response)
        return response
    logger.debug(f"Decoded data: {data}")
    if api.call(data):
        response = JSONResponse(status_code=200, content=data)
        csrf_protect.unset_csrf_cookie(response)
        return response
    response = JSONResponse(
        status_code=400, content={"error": "Ist kein Aktives Mitglied der AG DSN!"}
    )
    csrf_protect.unset_csrf_cookie(response)
    return response
