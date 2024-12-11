import pandas as pd

from sp_editor.database.models import CTISummary

from sqlalchemy.engine.base import Engine

TB_CTISUMMARY = str(CTISummary.__name__).lower()


def read_summaryCTI_DB(engine: Engine):
    """ """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name=TB_CTISUMMARY,  # The table to read
        con=engine,  # The SQLAlchemy engine
    )
    return df  # The DataFrame containing the table data
