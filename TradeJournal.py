import os
from os.path import join, dirname
from dotenv import load_dotenv
from Questrade import auth as q_auth, data
from TraderSync import auth as t_auth, action as t_action

if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    tradersync_token = t_auth.get_token()
    print("tradersync token:", tradersync_token)
    
    if q_auth.valid_access_token():
        questrade_token = os.environ.get('QUESTRADE_ACCESS_TOKEN')
    else:
        questrade_token = q_auth.get_access_token(dotenv_path)
        
    print("questrade token:", questrade_token)
    accounts = data.get_accounts()
        
    for acc in accounts:
        executions = data.get_executions(acc["number"], "2020-08-01T00:00:00-0")

        res = t_action.add_questrade_execution(executions, tradersync_token)
        if res.status_code != 200:
            print("failed to add executions:", res.request.body)
