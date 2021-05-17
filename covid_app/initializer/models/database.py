from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import environ, path

psw = environ.get('pg_psw')
SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{psw}@localhost:5433/covid'
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=False)
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()

