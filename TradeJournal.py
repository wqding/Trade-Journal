import os
from os.path import join, dirname
from dotenv import load_dotenv
from Questrade import auth as q_auth, data
    
if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    if q_auth.valid_access_token():
        access_token = os.environ.get('QUESTRADE_ACCESS_TOKEN')
    else:
        access_token = q_auth.get_access_token(dotenv_path)
        
    print("access_token:", access_token)
    
    accounts = data.get_accounts()
    
    for acc in accounts:
        executions = data.get_executions(acc["number"])
                