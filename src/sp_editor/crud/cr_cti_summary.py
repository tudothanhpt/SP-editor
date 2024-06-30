import pandas as pd
from pandas import DataFrame
from sqlalchemy import func

from sqlmodel import Session, select
from sp_editor.database.models import CTISummary

from sp_editor.core.find_pier import restructure_sdshapeDF, spColumn_CTI_PierPoint, shape_area
from sqlalchemy.engine.base import Engine
from sqlmodel import create_engine

TB_CTISUMMARY = str(CTISummary.__name__).lower()


def read_summaryCTI_DB(engine:Engine):
    """
    """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name= TB_CTISUMMARY,  # The table to read
        con=engine  # The SQLAlchemy engine
    )
    return df  # The DataFrame containing the table data