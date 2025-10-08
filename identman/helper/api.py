from typing import List, Union
import requests
from abc import ABC, abstractmethod
import csv
from .settings import settings, FileAPISettings, DummyAPISettings, PycroftAPISettings

class API(ABC):
    def __init__(self, url: str = "", api_key: str = ""):
        self.url = url
        self.key = api_key

    def call(self, data: dict) -> bool:
        if self.validate(data):
            return self.check_user(data)
        raise ValueError

    def validate(self, data: dict) -> bool:
        return True

    @abstractmethod
    def check_user(self, data: dict) -> bool:
        """check if user is authenticated"""
        pass

class DummyAPI(API):
    def __init__(self, data: List[List[str]]):
        super().__init__("dummy API", "dummy key")
        self._data = data

    def check_user(self, data: dict) -> bool:
        subset = [value for key, value in data.items()]
        for row in self._data:
            if subset in row:
                return True
        return False

class FileAPI(API):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def check_user(self, data):
        data_list = [value for key, value in data.items()]
        with open(self.path) as file:
            reader = csv.reader(file)
            for subset in reader:
                if set(subset).issubset(data_list):
                    return True
            return False



class PycroftAuthorization:
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def __call__(self, r: requests.Request) -> requests.Request:
        r.headers["Authorization"] = f"ApiKey {self.api_key}"
        return r


class PycroftAPI(API):
    def __init__(self):
        super().__init__(settings.pycroft_url, settings.pycroft_key)
        self.session = requests.Session()
        self.session.auth = PycroftAuthorization(settings.pycroft_key)
        

    def check_user(self, user_data: dict):

        try:
            res = self.session.get(self.url, data=user_data)
        except ConnectionError as e:
            raise e

        if res.status_code != 200:
            return False
        return True

def get_api(api: Union[DummyAPISettings, FileAPISettings, PycroftAPISettings]) -> API:
    match api:
        case PycroftAPISettings():
            return PycroftAPI(api.url, api.key)
        case DummyAPISettings():
            return DummyAPI(api.records)
        case FileAPISettings():
            return FileAPI(api.path)
        
api = get_api(settings.api)
