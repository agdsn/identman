import requests
from flask import current_app

def check_user(json: dict):
    url = current_app.config.get("PYCROFT_BACKEND")
    res = requests.post(url, json=json)
    if res.status_code != 200:
        return {}
    return res.json()
