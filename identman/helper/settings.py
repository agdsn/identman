from typing import List, Union
from pydantic_settings import BaseSettings


class CsrfSettings(BaseSettings):
  secret_key: str = "Top secret"

class PycroftAPISettings(BaseSettings): 
   url: str 
   key: str

class FileAPISettings(BaseSettings):
   path: str

class DummyAPISettings(BaseSettings):
   records: List[List[str]] = [["Hallo", "Hallo", "Hallo"]]

class Settings(BaseSettings):
    cors_origins: List[str] = ["http://localhost:3000"]
    backend: str = "sample"
    leading_zeros: int = 4
    csrf_settings: CsrfSettings = CsrfSettings()
    secret: str = "Hallo"
    api: Union[DummyAPISettings, FileAPISettings, PycroftAPISettings] = DummyAPISettings()

    class Config:
        env_file = ".env"

settings = Settings()