import pandas as pd
from sqlalchemy import func

from sqlmodel import Session, select
from sp_editor.database.models import PierForce

from sqlalchemy.engine.base import Engine

TB_PIERFORCE = str(PierForce.__name__).lower()

def get_pier_design_force_to_db(engine: Engine, df: pd.DataFrame):
    df.to_sql(TB_PIERFORCE, con=engine, if_exists='replace')
    
def read_pierdesign_forceDB(engine):
    """
    Reads the SQL table `TB_PIERFORCE` into a pandas DataFrame.

    Parameters:
    engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.

    Returns:
    pd.DataFrame: The DataFrame containing the table data.
    """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name=TB_PIERFORCE,  # The table to read
        con=engine                     # The SQLAlchemy engine
    )

    return df # The DataFrame containing the table data