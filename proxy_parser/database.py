from sqlalchemy import Table, Column, Text, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///proxy.sqlite')
Base = declarative_base()

proxy_table = Table(
    'proxy_table', Base.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('ip_address', Text),
    Column('port', Text),
)

Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()
