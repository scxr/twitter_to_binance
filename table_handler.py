from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
base = declarative_base()
engine = create_engine('sqlite:///main.db')

class Transactions(base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    coin = Column(String)
    amount = Column(Float)
    buy_price = Column(Float)
    sell_price = Column(Float)
    still_open = Column(Boolean, default=True)
    order_id = Column(String)


    def __repr__(self):
        return f"""<Coin bought : {self.coin}, Amount Bought : {self.amount},\\n
            Still open : {self.still_open}>"""
