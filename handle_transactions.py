from table_handler import base, engine
from sqlalchemy.orm import sessionmaker
base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

