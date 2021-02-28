from sqlalchemy.sql.visitors import traverse
from table_handler import base, engine, Transactions
from sqlalchemy.orm import sessionmaker
base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
#new_transaction = Transactions(coin='doge',amount=9090.90, buy_price=99.0,sell_price=3232)
#session.add(new_transaction)
#session.commit()
def add_new_transaction(coin:str, amount:float, buy_price:float, order_id:str, sell_price:float=0):
    new_transaction = Transactions(coin=coin, 
            amount=amount, 
            buy_price=buy_price, 
            sell_price=sell_price, 
            order_id=order_id)
    session.add(new_transaction)
    session.commit()
    session.close()

def mark_closed(order_id, sell_price):
    transaction_to_close = session.query(Transactions).filter_by(order_id=order_id).first()
    transaction_to_close.sell_price=sell_price
    transaction_to_close.still_open = False
    session.commit()

def get_transaction(order_id):
    transaction = session.query(Transactions).filter_by(order_id=order_id).first()
    return transaction

def calculate_returns():
    total_buys = session.query(Transactions).filter(Transactions.buy_price).all()
    total_sells = session.query(Transactions).filter(Transactions.buy_price).all()
    buys_cost = sum([i.buy_price * i.amount  for i in total_buys if not i.still_open ])
    sells_cost = sum([i.sell_price * i.amount for i in total_sells])
    return f'Total spent on buying : ${buys_cost}, Total sold : ${sells_cost}, Profit : ${sells_cost - buys_cost}'
print(calculate_returns())
#add_new_transaction('d',1,1,'111')
#mark_closed('111', 10)
#get_transaction('111')