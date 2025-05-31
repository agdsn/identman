import base64
import json
from argon2 import PasswordHasher, low_level
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


IV_LENGTH = 12
SALT_LENGTH = 12

class Message:
    def __init__(self, f_name=None, l_name=None, b_year=None, uid=None, **kwargs):
        self.f_name = f_name
        self.l_name = l_name
        self.b_year = b_year
        self.uid = uid
        for key, value in kwargs.items():
            setattr(self, key, value)

    def validate(self) -> bool:
        return self.f_name and self.l_name and self.b_year and self.uid

    def to_dict(self) -> dict | None:
        if not self.validate():
            return None
        return {
            "f_name": self.f_name,
            "l_name": self.l_name,
            "b_year": self.b_year,
            "uid": self.uid
        }

def get_message(query: str) -> Message | None:
    text = decrypt("password", query)
    try:
        json_dict = json.loads(text)
        m = Message(**json_dict)
        if m.validate():
            return m
        else:
            return None
    except json.JSONDecodeError:
        return None


def get_secret_key(password: str, salt: bytes):
    hasher = PasswordHasher(time_cost=10, memory_cost=80, parallelism=10, hash_len=32, type=low_level.Type.ID)
    a = hasher.hash(password, salt=salt)
    a = a.split("$")
    return base64.b64decode(a[-1] + "=")


def decrypt(password: str, cipher_message: str) -> str:
    decoded_cipher_byte = base64_urlsafe_no_pad_decode(cipher_message)
    salt = decoded_cipher_byte[:SALT_LENGTH] + b"2025"
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