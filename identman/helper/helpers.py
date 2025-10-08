import numbers
from cryptography.hazmat.primitives import hashes
import logging

from .settings import settings

logger = logging.getLogger(__name__)

class Query:
    def __init__(self, query=None, n=None, salt="", csrfToken=None, **kwargs):
        self._query = query
        self._n = n
        self._salt = salt
        self._csrfToken = csrfToken

    def validate(self) -> bool:
        if not (self._query and self._n and self._salt and self._csrfToken):
            return False

        if not (isinstance(self._n, numbers.Number)):
            return False
        print(f"Validating query: {self._query} salt {self._salt}")
        digest = hashes.Hash(hashes.SHA512())
        digest.update(self._query.encode())
        digest.update(self.get_token().encode())
        digest.update(self.get_salt())
        digest = digest.finalize()
        hash = digest.hex()

        cash = hash[:self._n].replace('0' *  settings.leading_zeros, "")
        print(cash)
        if len(cash) > 0:
            print("Chache")
            return False
        return True

    def get_salt(self) -> bytes:
        return bytes.fromhex(self._salt)

    def get_query(self) -> str:
        return self._query

    def get_token(self) -> str:
        return self._csrfToken

