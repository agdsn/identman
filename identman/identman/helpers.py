import numbers

from argon2 import low_level
from cryptography.hazmat.primitives import hashes

class Query:
    def __init__(self, query=None, n=None, salt=None, **kwargs):
        self._query = query
        self._n = n
        self._salt = salt

    def validate(self) -> bool:
        if not (self._query and self._n and self._salt):
            return False

        if not isinstance(self._n, numbers.Number):
            return False

        try:
            bytes.fromhex(self._salt)
        except ValueError:
            return False

        digest = hashes.Hash(hashes.SHA512())
        digest.update(self._query.encode())
        digest.update(self.get_salt())
        digest = digest.finalize()
        hash = digest.hex()
        print(hash)
        cash = hash[:self._n].replace('0'*self._n, "")
        if len(cash) > 0:
            return False
        return True

    def get_salt(self) -> bytes:
        return bytes.fromhex(self._salt)

    def get_query(self) -> str:
        return self._query