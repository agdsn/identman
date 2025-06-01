import random
import datetime
from math import radians

from flask import current_app
import logging
import threading
import base64

CSRF_EXIRATION = 30
MIN_CASH = 2
MAX_CASH = 4
s = threading.Semaphore(MAX_CASH)
logger = logging.getLogger(__name__)


class CRSFToken:
    def __init__(self):
        rand = random.randbytes(64)
        self._csrf_token = base64.b64encode(rand).decode('utf-8')

        self._exspiry = datetime.datetime.now() + datetime.timedelta(seconds=CSRF_EXIRATION)
        self._n = random.randint(MIN_CASH, MAX_CASH)

    def expired(self) -> bool:
        print(f"{self._exspiry} {datetime.datetime.now()}")
        if self._exspiry < datetime.datetime.now():
            return True
        return False

    def serialize(self) -> dict:
        return {"nhash": self._n, "csrf_token": self._csrf_token}

    def __repr__(self):
        return f"<CRSF Token: {self._csrf_token}, expires: {self._exspiry}>"

    def check_token(self, token) -> bool:
        return token == self._csrf_token

    def get_n(self) -> int:
        return self._n


def _check_token_list():
    for t in current_app.crftoken:
        if t.expired():
            logger.info(f"{t}")
            current_app.crftoken.remove(t)
            s.release()


def get_token() -> CRSFToken:
    _check_token_list()
    s.acquire()
    token = CRSFToken()
    current_app.crftoken.append(token)
    return token

def get_token_csrf(csrf: str) -> CRSFToken | None:
    for t in current_app.crftoken:
        print(f"running {t._csrf_token} or {csrf}")
        if t.check_token(csrf):
            current_app.crftoken.remove(t)
            s.release()
            return t

    return None
