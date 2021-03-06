import requests
import time
import json
from queue import Queue
from threading import Thread
from thread_pool_manager import ThreadPool
from make_binance_transaction import create_order
from handle_transactions import *
import random
base_url = "https://api.binance.com/api/v3/ticker/price?symbol="

with open('rules.json') as f:
    rules = json.load(f)

def get_price(crypto:str,  inital_price:int=0, fiat:str="USDT", base_price:int=0) -> float:
    url = f"{base_url}{crypto.upper()}{fiat}"
    r = requests.get(url)
    price = float(r.json()["price"])
    percent_change = ((price - inital_price) / ((price+inital_price)/2)) * 100 
    return percent_change, price

def main_loop(crypto, amount):
    print('test')
    int(amount)
    _, base_price = get_price(crypto)
    order_id = random.randint(000000, 111111) 
    add_new_transaction(crypto, amount,base_price,order_id)
    try:
        create_order('BUY',crypto.upper(), amount)
    except Exception as e:
        print(e)
        return 'Failed'
    percent = 0.00
    print('here')
    
    while 1:
        percent, curr = get_price(crypto, inital_price=base_price)
        if percent >= rules['TAKE_PROFIT'] or percent <= rules['TAKE_LOSS']:
            create_order('SELL',crypto.upper(), amount)
            mark_closed(order_id, curr)
            print(f'bought in at {base_price} and sold at {curr}')
        time.sleep(10)
    return




