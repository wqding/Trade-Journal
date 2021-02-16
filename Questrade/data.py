import requests
import os
import json

def get_accounts():
    url = f"{os.environ.get('QUESTRADE_API_SERVER')}v1/accounts"
    try:
        res = requests.get(url, headers={"Authorization":f"Bearer {os.environ.get('QUESTRADE_ACCESS_TOKEN')}"})
    except requests.exceptions.RequestException as e:
        print("accounts request error:", e)
    
    accounts_json = json.loads(res.text)
    return accounts_json["accounts"]

def get_executions(accountID, start="", end=""):
    url = f"{os.environ.get('QUESTRADE_API_SERVER')}v1/accounts/{accountID}/executions"
    if start != "" or end != "":
        url += "?"
    if start != "":
        url += f"&startTime={start}"
    if end != "":
        url += f"&endTime={end}"
    
    try:
        res = requests.get(url, headers={"Authorization":f"Bearer {os.environ.get('QUESTRADE_ACCESS_TOKEN')}"})
    except requests.exceptions.RequestException as e:
        print("executions request error:", e)
    
    executions_json = json.loads(res.text)
    return executions_json["executions"]
        