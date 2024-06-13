import sys
import pandas as pd
from pandas import DataFrame

from sp_editor.database.models import LoadCombinations
from sqlmodel import Session, create_engine
from sqlalchemy.engine.base import Engine


def create_df_to_db(engine, db_table_name, df: pd.DataFrame):
    """
    Writes a DataFrame to an SQL database.

    Parameters:
    engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.
    table_name (str): The name of the table to write the DataFrame to.
    df (pd.DataFrame): The DataFrame to write to the SQL database.

    Returns:
    None
    """
    try:
        # Write DataFrame to SQL
        df.to_sql(db_table_name, con=engine, if_exists='replace', index=False)
        print(f"DataFrame successfully written to table '{db_table_name}' in the database.")

    except Exception as e:
        print(f"An error occurred: {e}")


def get_df_load_combinations_fromdb(engine):
    df = pd.read_sql_table(table_name='loadcombinations', con=engine)
    return df


if __name__ == "__main__":
    pass
