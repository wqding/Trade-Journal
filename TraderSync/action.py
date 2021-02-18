import requests
import os

def add_questrade_execution(executions, token):
    url = f"{os.environ.get('TRADERSYNC_API_SERVER')}manuals"
    
    add_execution_headers = {
            "Content-Type": "application/json",
            "Host": os.environ.get('TRADERSYNC_HOST'),
            "token": token,
        }
    
    # tradersync_data = [{"market":"STOCK","portfolio":72942,"symbol":"THCB","action":"sell","date":"2021-02-15","time":"16:28:42","price":"20","shares":"200","commission":"5"},{"market": "STOCK", "portfolio": "72942", "symbol": "HQGE", "action": "Buy", "date": "2021-02-16", "time": "14:58:10", "price": 0.023, "shares": 14908, "commission": 0}]

    tradersync_data=[{}]*len(executions)
    
    for i, ex in enumerate(executions):
        tradersync_data[i] = {
            "market": "STOCK",
            "portfolio": os.environ.get("TRADERSYNC_PORTFOLIO_NUMBER"),
            "symbol": ex["symbol"],
            "action": ex["side"],
            "date": ex["timestamp"][:10],
            "time": ex["timestamp"][11:19],
            "price": ex["price"],
            "shares": ex["quantity"],
            "commission": ex["commission"]
        }
    
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