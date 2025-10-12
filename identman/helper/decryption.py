import base64
from typing import Optional

from argon2 import PasswordHasher, low_level
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel, ConfigDict, field_validator

IV_LENGTH = 12
SALT_LENGTH = 12

class Message(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: str
    fname: str
    byear: Optional[int] = None
    uid: int

    @field_validator('byear', mode='before')
    def empty_str_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v

def get_secret_key(password: str, salt: bytes):
    hasher = PasswordHasher(time_cost=10, memory_cost=80, parallelism=10, hash_len=32, type=low_level.Type.ID)
    a = hasher.hash(password, salt=salt)
    a = a.split("$")
    return base64.b64decode(a[-1] + "=")


def decrypt(password: str, salt: str, cipher_message: str) -> str:
    decoded_cipher_byte = base64_urlsafe_no_pad_decode(cipher_message)
    salt = decoded_cipher_byte[:SALT_LENGTH] + salt.encode()
    iv = decoded_cipher_byte[SALT_LENGTH : (SALT_LENGTH + IV_LENGTH)]
    encrypted_message_byte = decoded_cipher_byte[(IV_LENGTH + SALT_LENGTH) :]
    secret = get_secret_key(password, salt)
    aesgcm = AESGCM(secret)
    plaintext = aesgcm.decrypt(iv, encrypted_message_byte, None)
    return plaintext.decode("utf-8")

def base64_urlsafe_no_pad_decode(data: str) -> bytes:
    # Padding ggf. auffüllen (Base64 muss durch 4 teilbar sein)
    padding_needed = 4 - (len(data) % 4)
    if padding_needed and padding_needed != 4:
        data += '=' * padding_needed
    return base64.urlsafe_b64decode(data)