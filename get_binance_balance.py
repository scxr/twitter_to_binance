from binance.client import Client
import json

with open('credentials.json') as f:
    credentials = json.load(f)
    

client = Client(credentials['BINANCE_API'], credentials['BINANCE_SECRET'])

def get_balance():
    bal = client.get_account()
    resp = [i for i in bal['balances'] if i['asset']=='USDT']
    if float(resp[0]['free']) == 0:
        return 'Please deposit some USDT to use this program, you have no Free USDT', 0,False
    else:
        return f'Your balance is : {resp[0]["free"]}', resp[0]["free"],True
    
