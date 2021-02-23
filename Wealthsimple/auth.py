from wsimple.api import Wsimple, InvalidAccessTokenError, InvalidRefreshTokenError
import os
from dotenv import set_key
import requests

def refresh_token(tokens):
    r = requests.post(
        url=f"{os.environ.get('WEALTHSIMPLE_API_SERVER')}auth/refresh",
        data=tokens[1],
    )
    if r.status_code == 401:
        raise InvalidRefreshTokenError
    else:
        access_token = r.headers['X-Access-Token']
        new_refresh_token = r.headers['X-Refresh-Token']
        tokens = [{'Authorization': access_token}, {"refresh_token": new_refresh_token}]

        return tokens

def get_session(dotenv_path):
    email = os.environ["WEALTHSIMPLE_GMAIL_ADDRESS"]
    password = os.environ["WEALTHSIMPLE_PASSWORD"]
    
    new_tokens = refresh_token(tokens=[
        {"Authorization": os.environ["WEALTHSIMPLE_ACCESS_TOKEN"]},
        {"refresh_token": os.environ["WEALTHSIMPLE_REFRESH_TOKEN"]}
    ])
    
    try:
        # login to Wealthsimple
        ws = Wsimple(
            email,
            password,
            oauth_mode=True,
            tokens=new_tokens,
            )
    except InvalidAccessTokenError:
        print("invalid access token")
        otpnumber = int(input("Enter otpnumber: \n>>>"))
        ws = Wsimple.otp_login(email, password, otpnumber)
    except InvalidRefreshTokenError:
        print("invalid refresh token")
        otpnumber = int(input("Enter otpnumber: \n>>>"))
        ws = Wsimple.otp_login(email, password, otpnumber)
        
     # update refresh token
    os.environ['WEALTHSIMPLE_REFRESH_TOKEN'] = ws.tokens[1]["refresh_token"]
    set_key(dotenv_path, "WEALTHSIMPLE_REFRESH_TOKEN", os.environ["WEALTHSIMPLE_REFRESH_TOKEN"])
    
    # update access token
    os.environ['WEALTHSIMPLE_ACCESS_TOKEN'] = ws.tokens[0]["Authorization"]
    set_key(dotenv_path, "WEALTHSIMPLE_ACCESS_TOKEN", os.environ["WEALTHSIMPLE_ACCESS_TOKEN"])
        
    return ws, ws.tokens