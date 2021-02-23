import os
from os.path import join, dirname
from dotenv import load_dotenv, set_key
from Questrade import auth as q_auth, data
from TraderSync import auth as t_auth, action as t_action
from Wealthsimple import auth as w_auth
import datetime
import constants

def add_questrade_executions(tradersync_token, dotenv_path):
    if q_auth.valid_access_token():
        questrade_token = os.environ.get('QUESTRADE_ACCESS_TOKEN')
    else:
        questrade_token = q_auth.get_access_token(dotenv_path)
        
    print("questrade token:", questrade_token)
    qtrade_accounts = data.get_accounts()
    
    for acc in qtrade_accounts:
        executions = data.get_executions(acc["number"], os.environ["START_DATE_TIMESTAMP"]+"-0")
        
        if len(executions) == 0:
            continue

        res = t_action.add_executions_to_tradersync(executions, tradersync_token, constants.PLATFORM_QUESTRADE)
        if res.status_code != 200:
            print("failed to add executions:", res.request.body)

def add_wealthsimple_executions(tradersync_token, dotenv_path):
    ws, tokens = w_auth.get_session(dotenv_path)
    print("ws tokens:", tokens)
    
    ws_account_ids = ws.get_account_ids(tokens)
    print(ws_account_ids)
    
    for id in ws_account_ids:
        # get buy and sell orders
        buy_executions = ws.get_activities(tokens, limit=20, type="buy", account_id=id)
        sell_executions = ws.get_activities(tokens, limit=20, type="sell", account_id=id)
        
        if len(buy_executions["results"]) == 0 or len(buy_executions["errors"]) != 0:
            print(f"get buy_executions for {id} failed:", buy_executions)
            continue
        
        if len(sell_executions["results"]) == 0 or len(sell_executions["errors"]) != 0:
            print(f"get sell_executions for {id} failed:", sell_executions)
            continue
        
        executions = buy_executions["results"] + sell_executions["results"]
        
        if "crypto" in id:
            res = t_action.add_executions_to_tradersync(executions, tradersync_token, constants.PLATFORM_WEALTHSIMPLE, isCrypto=True)
        else:
            res = t_action.add_executions_to_tradersync(executions, tradersync_token, constants.PLATFORM_WEALTHSIMPLE, isCrypto=False)
        if res.status_code != 200:
            print("failed:", res.text)
            print("failed to add executions:", res.request.body)

if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    tradersync_token = t_auth.get_token()
    print("tradersync token:", tradersync_token)
    
    add_questrade_executions(tradersync_token, dotenv_path)
    
    add_wealthsimple_executions(tradersync_token, dotenv_path)
        
    os.environ['START_DATE_TIMESTAMP'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    set_key(dotenv_path, "START_DATE_TIMESTAMP", os.environ["START_DATE_TIMESTAMP"])
