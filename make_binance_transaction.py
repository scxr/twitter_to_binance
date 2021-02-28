from binance.client import Client
import json

with open('credentials.json') as f:
    credentials = json.load(f)
    

client = Client(credentials['BINANCE_API'], credentials['BINANCE_SECRET'])

def create_order(order_type:str, crypto_symbol:str, amount:float, fiat:str='USDT') -> dict:
    try:
        buy_order = client.create_test_order(
            symbol = f'{crypto_symbol}{fiat}',
            side = order_type,
            type='MARKET',
            quantity = 1000
        )
        return buy_order
    except Exception as e:
        print(e)
        return "ERROR: %s" % e