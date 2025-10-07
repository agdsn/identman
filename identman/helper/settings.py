import os
from typing import List, Union, Literal
import logging
import yaml

from pydantic_settings import BaseSettings, SettingsConfigDict


class CsrfSettings(BaseSettings):
  secret_key: str = "Top secret"
  cookie_samesite: str = "none"
  cookie_secure: bool = True
  token_location: str = "body"
  token_key: str = "csrfToken"

class PycroftAPISettings(BaseSettings):
    kind: Literal["pycroft"] = "pycroft"
    url: str
    key: str

class FileAPISettings(BaseSettings):
    kind: Literal["file"] = "file"
    path: str

class DummyAPISettings(BaseSettings):
    kind: Literal["dummy"] = "dummy"
    records: List[List[str]] = [["Hallo", "Hallo", "Hallo"]]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "https://ident-api.agdsn.de", "https://ident.agdsn.de"]
    backend: str = "sample"
    leading_zeros: int = 4
    csrf_settings: CsrfSettings = CsrfSettings()
    api: Union[DummyAPISettings, FileAPISettings, PycroftAPISettings] = DummyAPISettings()
    log_level: str = "INFO"

    @classmethod
    def from_yaml(cls, path: str = "config.yaml"):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def get_loglevel(self) -> int | None:
        return getattr(logging, self.log_level.upper(), None)


class Secrets(BaseSettings):
    secret: str = "Hallo"
    salt: str = "2025"
    csrf_key: str = "Top secret"


if not os.getenv("CONFIG"):
    settings = Settings()
    secrets = Secrets()
else:
    secrets = Secrets(
        secret=os.getenv("API_DECRYPT_PASSWORD"),
        salt=os.getenv("API_SALT"),
        csrf_key=os.getenv("API_CSRF_KEY"),
    )
    settings = Settings.from_yaml(os.getenv("CONFIG"))
    settings.csrf_settings.secret_key = secrets.csrf_key
