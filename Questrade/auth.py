import requests
import os
from dotenv import set_key
import json

def valid_access_token():
    url = f"{os.environ.get('QUESTRADE_API_SERVER')}v1/accounts"
    
    res = requests.get(url, headers={"Authorization":f"Bearer {os.environ.get('QUESTRADE_ACCESS_TOKEN')}"})
    if res.status_code == 200 or res.status_code == 201:
        return True
    elif res.status_code == 401:
        return False
    else:
        print("Error has occured during access token validity check.")
        return False

def update_dotenv(dotenv_path, new_refresh_token, access_token, api_server):
    # update refresh token
    os.environ['QUESTRADE_REFRESH_TOKEN'] = new_refresh_token
    set_key(dotenv_path, "QUESTRADE_REFRESH_TOKEN", os.environ["QUESTRADE_REFRESH_TOKEN"])
    
    # update access token
    os.environ['QUESTRADE_ACCESS_TOKEN'] = access_token
    set_key(dotenv_path, "QUESTRADE_ACCESS_TOKEN", os.environ["QUESTRADE_ACCESS_TOKEN"])
    
    # update api server if changed
    if os.environ.get('QUESTRADE_API_SERVER') != api_server:
        os.environ['QUESTRADE_API_SERVER'] = api_server
        set_key(dotenv_path, "QUESTRADE_API_SERVER", os.environ["QUESTRADE_API_SERVER"])

def get_access_token(dotenv_path):
    QUESTRADE_AUTH_BASEURL = os.environ.get('QUESTRADE_AUTH_BASEURL')
    QUESTRADE_REFRESH_TOKEN = os.environ.get('QUESTRADE_REFRESH_TOKEN')
       
    auth_url = f"{QUESTRADE_AUTH_BASEURL}?grant_type=refresh_token&refresh_token={QUESTRADE_REFRESH_TOKEN}"
    
    try:
        res = requests.post(auth_url)
    except requests.exceptions.RequestException as e:
        print("request error:", e)
        
    if res.status_code != 200 and res.status_code != 201:
        print("request not ok:", res.status_code)
    
    auth_json = json.loads(res.text)
    access_token = auth_json["access_token"]
    new_refresh_token = auth_json["refresh_token"]
    api_server = auth_json["api_server"]
    
    update_dotenv(dotenv_path, new_refresh_token, access_token, api_server)

    return access_token
