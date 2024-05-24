from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker,declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import pandas as pd

engine = create_engine('sqlite:///total_database.db', echo=True)
Base = declarative_base()


class GeneralInfor(Base):
    __tablename__ = 'generalInfor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    design_code = Column(String, default="ACI 318-19")
    unit_system = Column(String, default="English")
    bar_set = Column(String, default="ASTM A615")
    confinement = Column(String, default="Tied")
    section_capacity = Column(String, default="Critical capacity")


# Create the table
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

column_names = ["design_code", "unit_system", "bar_set", "confinement", "section_capacity"]


def get_general_infor():
    return session.query(GeneralInfor).order_by(GeneralInfor.id).all()


def update_general_infor(design_code):
    generalInfor = session.query(design_code).filter_by(id=1)
    if generalInfor:
        generalInfor.design_code = design_code
