from utils.readconfig import read_config
import requests
import json
from datetime import datetime, timedelta

def request_token():
    url = read_config('Server','token')
    _username = read_config('Server','username')
    _password = read_config('Server','password')
    payload = json.dumps({"username": _username, "password": _password})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        token = None
    else:
        token = response.json()['access_token']
    if token:
            dict = {}
            f=open("./credentials.key","w+")
            dict['access_token'] = token
            dict['expiration'] = str(datetime.now().date() + timedelta(days=1))
            f.write(json.dumps(dict))
            f.close

def check_token():
    pass

def get_token():
    f=open("./credentials.key")
    token = json.load(f)['access_token']
    f.close()
    return token