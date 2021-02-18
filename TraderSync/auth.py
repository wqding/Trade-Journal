import requests
import json
import os

def get_token():
    auth_url = f"{os.environ.get('TRADERSYNC_API_SERVER')}auth"
    auth_data = {
            "email": os.environ.get('TRADERSYNC_USERNAME'),
            "password": os.environ.get('TRADERSYNC_PASSWORD')
        }
    auth_headers = {
            "Content-Type": "application/json",
            "Host": os.environ.get('TRADERSYNC_HOST'),
            "Client": "web",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        }
    
    # s = requests.Session()
    
    try:
        res = requests.post(
            auth_url, 
            headers=auth_headers,
            # cannot put data=auth_data, thats what was the issue before
            json=auth_data,
        )
        # res = s.post(
        #     auth_url, 
        #     headers=auth_headers,
        #     # cannot put data=auth_data, thats what was the issue before
        #     json=auth_data,
        #     # cookies=auth_cookies
        # )
        
    except requests.exceptions.RequestException as e:
        print("request error:", e)
        
    if res.status_code != 200 and res.status_code != 201:
        print("request not ok:", res.status_code)
        
    auth_json = json.loads(res.text)
    token = auth_json["token"]
    
    # may also have to return the session
    return token