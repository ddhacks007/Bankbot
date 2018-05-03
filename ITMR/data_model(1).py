
from sqlalchemy import BigInteger, Column, DateTime, Integer,SmallInteger, String,Float
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from flask import Flask
from config import params

app = Flask(__name__)
Base = declarative_base()
metadata = Base.metadata
engine = create_engine('mysql://'+params['username']+':'+params['password']+'@'+params['hostname']+':'+params['port']+'/'+params['db'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

class CustomerInfo(Base):
	__tablename__ = 'customer_info'
	id = Column(BigInteger, primary_key=True)
	account_number = Column(BigInteger, unique=True)
	customer_id = Column(BigInteger, unique=True)
	first_name = Column(String(255))
	last_name = Column(String(255))
	age = Column(Integer)
	sex = Column(String(1))
	email = Column(String(100))
	account_balance = Column(BigInteger)
	date_of_joinee = Column(DateTime)
	phone_number = Column(BigInteger)
	account_branch = Column(String(100))
	address = Column(String(255))


class CustomerPii(Base):
	__tablename__ = 'customer_pii'
	id = Column(BigInteger, primary_key=True)
	account_number = Column(BigInteger)
	user_name = Column(String(100))
	password = Column(String(255))
	customer_id = Column(BigInteger)
	card_type = Column(SmallInteger)
	card_number = Column(BigInteger)
	cvv = Column(Integer)
	card_expiry = Column(DateTime)
	name_on_card = Column(String(100))


class Net_banking(Base):
	__tablename__ = 'Net_banking'
	id = Column(BigInteger, primary_key=True)
	account_number1 = Column(BigInteger)
	account_number2 = Column(BigInteger)
	address = Column(String(255))
	transfer_amount = Column(BigInteger)
	date_time = Column(DateTime)
    

class agent_details(Base):
	__tablename__ = 'agent_details'
	id = Column(BigInteger, primary_key=True)
	phone_number = Column(BigInteger)
	age = Column(BigInteger)
	address = Column(String(255))
	name = Column(String(255))
    	email = Column(String(255))



Base.metadata.create_all(bind=engine)












