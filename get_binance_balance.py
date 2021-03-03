from binance.client import Client
import json

with open('credentials.json') as f:
    credentials = json.load(f)
    

client = Client(credentials['BINANCE_API'], credentials['BINANCE_SECRET'])

def get_balance():
    bal = client.get_account()
    resp = [i for i in bal['balances'] if i['asset']=='USDT']
    if float(resp[0]['free']) == 0:
        return 'Please deposit some USDT to use this program, you have no Free USDT', 100,False
    else:
        return f'Your balance is : {resp[0]["free"]}', 100,True
    
def get_tick_size(crypto, fiat='USDT'):
    symbol_info = client.get_symbol_info(f'{crypto.upper()}{fiat}')
    from pprint import pprint
    pprint(symbol_info)
    ticker = symbol_info["filters"][0]["tickSize"]
    cnt = 0
    for i in ticker[2:]:
        if i == '0':
            cnt +=1
        elif i == '1':
            break
        else:
            print('How did we get here')
    return cnt

def get_alt_tick_size(crypto, fiat='USDT'):
    step_size = next(
        _filter['stepSize'] for _filter in client.get_symbol_info(f'{crypto.upper()}{fiat.upper()}')['filters']
        if _filter['filterType'] == 'LOT_SIZE')
    if step_size.find('1') == 0:
        return 1 - step_size.find('.')
    else:
        return step_size.find('1') - 1
get_tick_size('DOGE')