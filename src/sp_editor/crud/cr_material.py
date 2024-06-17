import json
import os
import sys
from typing import Type, Literal, Sequence

import pandas as pd

from sqlmodel import Session, select, SQLModel
from sqlmodel import Field, Session, SQLModel, create_engine, text
from typing import Optional
from sqlalchemy.engine.base import Engine


def set_engine(database_path: str) -> Optional[Engine]:
    """Create the SQLite database engine.
    
    Args:
        database_path (str): The file path to the SQLite database.
    
    Returns:
        Optional[Engine]: The created database engine, or None if the database file does not exist.
    """
    if not os.path.exists(database_path):
        print("No Existing Database")
        return None

    return create_engine(f"sqlite:///{database_path}", echo=False)


def get_df_from_db(engine, table_name):
    """
    Retrieve data from the specified table in the database using a session and return it as a pandas DataFrame.

    :param engine: SQLAlchemy engine object
    :param table_name: Name of the table to retrieve data from
    :return: pandas DataFrame containing the table data
    """
    # Create a session
    with Session(engine) as session:
        # Retrieve data from the specified table
        query = text(f"SELECT * FROM {table_name}")
        result = session.exec(query)
        # Convert result to pandas DataFrame
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        if 'id' in df.columns:
            df = df.drop(columns=['id'])

    return df


def update_df_to_db(engine, db_table_name, df):
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


def main():
    database_path = r"C:\Users\abui\Documents\BM\git\repo\SP-editor\tests\test.db"
    engine = set_engine(database_path)


if __name__ == "__main__":
    main()
