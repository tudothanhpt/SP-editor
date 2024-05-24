from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker,declarative_base
from sqlalchemy.sql import text
import pandas as pd

from general_infor_tb import GeneralInfor, Base as GeneralInforBase,update_general_infor,get_general_infor
engine = create_engine('sqlite:///total_database.db', echo=True)
Base = declarative_base()


# Create tables in the database
GeneralInforBase.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    pass