import requests
import os
import datetime
import constants

def parse_questrade_executions(executions):
    tradersync_data=[{}]*len(executions)
    
    for i, ex in enumerate(executions):
        execution_time = datetime.datetime.strptime(ex["timestamp"][:-6], '%Y-%m-%dT%H:%M:%S.%f')
        
        tradersync_data[i] = {
            "market": "STOCK",
            "portfolio": os.environ.get("TRADERSYNC_PORTFOLIO_NUMBER"),
            "symbol": ex["symbol"],
            "action": ex["side"],
            "date": execution_time.strftime("%Y-%m-%d"),
            "time": execution_time.strftime("%H:%M:%S"),
            "price": ex["price"],
            "shares": ex["quantity"],
            "commission": ex["commission"]
        }
        
    return tradersync_data

def parse_wealthsimple_equities_executions(executions):
    tradersync_data=[{}]*len(executions)
    
    curr = 0
    for ex in executions:
        if "filled_at" not in ex or "settled" not in ex:
            continue
        
        if ex["settled"] == False or ex["filled_at"] == None:
            continue
        
        # compare starttime to last run time
        execution_time = datetime.datetime.strptime(ex["filled_at"][:-5], '%Y-%m-%dT%H:%M:%S')
        last_run_time = datetime.datetime.strptime(os.environ.get('START_DATE_TIMESTAMP'), '%Y-%m-%dT%H:%M:%S')
        if execution_time > last_run_time:
            continue

        tradersync_data[curr] = {
            "market": "STOCK",
            "portfolio": os.environ.get("TRADERSYNC_PORTFOLIO_NUMBER"),
            "symbol": ex["symbol"],
            "action": ex["order_type"][:-9],
            "date": execution_time.strftime("%Y-%m-%d"),
            "time": execution_time.strftime("%H:%M:%S"),
            "price":  ex["market_value"]["amount"]/ex["quantity"] if ex["limit_price"] == None else ex["limit_price"]["amount"],
            "shares": ex["quantity"],
            "commission": 0 if ex["market_value"]["currency"] == "CAD" else ex["market_value"]["amount"]*0.015
        }
        curr += 1
        
    return tradersync_data[:curr]

def parse_wealthsimple_crypto_executions(executions):
    tradersync_data=[{}]*len(executions)
    
    curr = 0
    for ex in executions:
        if "filled_at" not in ex:
            continue
        
        if ex["filled_at"] == None:
            continue
        
        # compare starttime to last run time
        execution_time = datetime.datetime.strptime(ex["filled_at"][:-5], '%Y-%m-%dT%H:%M:%S')
        last_run_time = datetime.datetime.strptime(os.environ.get('START_DATE_TIMESTAMP'), '%Y-%m-%dT%H:%M:%S')
        if execution_time > last_run_time:
            continue

        tradersync_data[curr] = {
            "market": "STOCK",
            "portfolio": os.environ.get("TRADERSYNC_PORTFOLIO_NUMBER"),
            "symbol": ex["symbol"],
            "action": ex["order_type"][:-9],
            "date": execution_time.strftime("%Y-%m-%d"),
            "time": execution_time.strftime("%H:%M:%S"),
            "price": ex["price"]["amount"],
            "shares": ex["quantity"],
            "commission": abs(ex["fee"]["amount"])
        }
        curr += 1
        
    return tradersync_data[:curr]

def add_executions_to_tradersync(executions, tradersync_token, platform, isCrypto=False):
    url = f"{os.environ.get('TRADERSYNC_API_SERVER')}manuals"
    
    add_execution_headers = {
            "Content-Type": "application/json",
            "Host": os.environ.get('TRADERSYNC_HOST'),
            "Client": "web",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "token": tradersync_token,
        }
    
    if platform == constants.PLATFORM_QUESTRADE:
        tradersync_data = parse_questrade_executions(executions)
    elif platform == constants.PLATFORM_WEALTHSIMPLE:
        if isCrypto:
            tradersync_data = parse_wealthsimple_crypto_executions(executions)
        else:
            tradersync_data = parse_wealthsimple_equities_executions(executions)
    else:
        print("incorrect platform")
        tradersync_data = []

    # print(tradersync_data)
    
    try:
        res = requests.post(
            url,
            headers=add_execution_headers,
            json=tradersync_data
        )
    except requests.exceptions.RequestException as e:
        print("request error:", e)
        
    return res