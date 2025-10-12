import numbers
from cryptography.hazmat.primitives import hashes
import logging

from pydantic import BaseModel, ConfigDict, model_validator

from .settings import settings

logger = logging.getLogger(__name__)

class Query(BaseModel):
    model_config = ConfigDict(extra='ignore')

    query: str
    salt: str
    csrfToken: str

    @model_validator(mode="after")
    def validate_challenge(self):
        digest = hashes.Hash(hashes.SHA512())
        digest.update(self.query.encode())
        digest.update(self.csrfToken.encode())
        digest.update(bytes.fromhex(self.salt))
        digest = digest.finalize()
        hash = digest.hex()

        cash = hash[:settings.leading_zeros].replace('0' * settings.leading_zeros, "")

        if len(cash) > 0:
            raise ValueError
        return self
