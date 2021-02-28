import requests
import time
from queue import Queue
from threading import Thread
from thread_pool_manager import ThreadPool
base_url = "https://api.binance.com/api/v3/ticker/price?symbol="

def get_price(crypto:str,  inital_price:int=0, fiat:str="USDT", base_price:int=0) -> float:
    url = f"{base_url}{crypto.upper()}{fiat}"
    r = requests.get(url)
    price = float(r.json()["price"])
    percent_change = ((price - inital_price) / ((price+inital_price)/2)) * 100 
    return percent_change, price

def main_loop(crypto):
    _, base_price = get_price(crypto)
    percent = 0.0
    while percent >= -1:
        percent, curr = get_price(crypto, inital_price=base_price)
        print(percent, base_price, curr)
        time.sleep(10)
        if percent >= 0.1 or percent <= -0.01:
            break
    return

def test_loop():
    cnt = 0
    while cnt < 10:
        print('oof')
        time.sleep(10)
        cnt +=1 


