import os
from typing import List, Union, Literal

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

    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    backend: str = "sample"
    leading_zeros: int = 4
    csrf_settings: CsrfSettings = CsrfSettings()
    secret: str = "Hallo"
    api: Union[DummyAPISettings, FileAPISettings, PycroftAPISettings] = DummyAPISettings()

    @classmethod
    def from_yaml(cls, path: str = "config.yaml"):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)


if not os.getenv("CONFIG"):
    settings = Settings()
else:
    settings = Settings.from_yaml(os.getenv("CONFIG"))