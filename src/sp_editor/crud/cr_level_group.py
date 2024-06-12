import sys
import pandas as pd
from pandas import DataFrame

from sqlmodel import Session, select
from sp_editor.database.models import Grouplevel, Pierlabel, Level

from sqlalchemy.engine.base import Engine


def get_level_db(engine: Engine, df: DataFrame):
    df.to_sql("level", con=engine, if_exists='replace')


def get_level(engine: Engine):
    with Session(engine) as session:
        statement = select(Level)
        results = session.exec(statement)
        level_detail = results.all()
        return level_detail

# def update_tier(engine: Engine, list[Level]):
#     with Session(engine) as session:
#         statement = select(Grouplevel).where(Grouplevel.story==)
