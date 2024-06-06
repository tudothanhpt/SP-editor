import json
import sys
from typing import Type, Literal

import pandas as pd

from sqlmodel import Session, select
from database.models import BarSet
from database.models import GeneralInfor
from database import barset_table

from core.global_variables import BarGroupType

from sqlalchemy.engine.base import Engine


def create_barset(engine: Engine, barset: str):
    barset_file = barset_list(barset)
    json_to_sql(barset_file, engine, mode='append')


def update_barset(engine: Engine, barset: str):
    barset_file = barset_list(barset)
    json_to_sql(barset_file, engine, mode='replace')


def get_barset(engine: Engine, barset: str):
    with Session(engine) as session:
        statement = select(BarSet)
        results = session.exec(statement)
        bar_detail = results.all()
        return bar_detail


def barset_list(barset: str):
    base_path = "database/barset_table"
    if barset == str(BarGroupType.ASTM615):
        return f"{base_path}/tb_ASTM_A615.json"
    elif barset == str(BarGroupType.ASTM615M):
        return f"{base_path}/tb_ASTM_A615M.json"
    elif barset == str(BarGroupType.PR_EN_10080):
        return f"{base_path}/tb_PrEN_10080.json"
    elif barset == str(BarGroupType.CSA_G30_18):
        return f"{base_path}/tb_CSA_G30_18.json"
    else:
        return None


def json_to_sql(file_name: str, engine: Engine,
                mode: Literal['fail', 'append', 'replace']):
    with open(file_name) as json_file:
        data = json.load(json_file)
    df = pd.DataFrame(data)
    df.to_sql("barset", con=engine, if_exists=mode, index=False)
