import json
import os
import sys
from typing import Type, Literal, Sequence

import pandas as pd

from sqlmodel import Session, select, SQLModel
from sp_editor.database.models import BarSet

from sp_editor.core.global_variables import BarGroupType
from sp_editor import GLOBALPATH
from sqlalchemy.engine.base import Engine


def create_barset(engine: Engine, barset: str):
    barset_file = barset_list(barset)
    json_to_sql(barset_file, engine, mode='append')


def update_barset(engine: Engine, barset: str):
    barset_file = barset_list(barset)
    json_to_sql(barset_file, engine, mode='replace')


def get_barset(engine: Engine, barset: str) -> Sequence[BarSet]:
    with Session(engine) as session:
        statement = select(BarSet)
        results = session.exec(statement)
        bar_detail = results.all()
        return bar_detail


def barset_list(barset: str):

    if barset == str(BarGroupType.ASTM615):

        return os.path.join(GLOBALPATH, "database", "barset_table","tb_ASTM_A615.json")

    elif barset == str(BarGroupType.ASTM615M):
        return os.path.join(GLOBALPATH, "database", "barset_table","tb_ASTM_A615M.json")
    elif barset == str(BarGroupType.PR_EN_10080):
        return os.path.join(GLOBALPATH, "database", "barset_table","tb_PrEN_10080.json")
    elif barset == str(BarGroupType.CSA_G30_18):
        return os.path.join(GLOBALPATH, "database", "barset_table","tb_CSA_G30_18.json")
    else:
        return None


def json_to_sql(file_name: str, engine: Engine,
                mode: Literal['fail', 'append', 'replace']):
    with open(file_name) as json_file:
        data = json.load(json_file)
    df = pd.DataFrame(data)
    df.to_sql("barset", con=engine, if_exists=mode, index=False)
