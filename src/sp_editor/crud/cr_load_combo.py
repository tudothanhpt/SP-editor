import pandas as pd

from sp_editor.database.models import LoadCombinations, LoadCombinationsSelection

TB_UNIQUECOMBO = str(LoadCombinations.__name__).lower()
TB_COMBOSELECTION = str(LoadCombinationsSelection.__name__).lower()
TB_CS_HEADER_ORICOMBO = list(LoadCombinationsSelection.__fields__.keys())[1]
TB_CS_HEADER_SELECTEDCOMBO = list(LoadCombinationsSelection.__fields__.keys())[2]


def create_loadComboDB(engine, df: pd.DataFrame):
    """
    Writes a DataFrame to the 'loadcombinations' table in the database.

    Args:
        engine (sqlalchemy.engine.Engine): The database engine.
        df (pd.DataFrame): The DataFrame containing data to write.

    Raises:
        Exception: If an error occurs during the write operation.
    """
    try:
        # Write DataFrame to SQL
        # Write DataFrame to SQL
        df.to_sql(TB_UNIQUECOMBO,  # Table name
                  con=engine,  # SQLAlchemy engine
                  if_exists='replace',  # 'replace' if table already exists
                  index=False)  # Do not write index as a column
        print(f"DataFrame successfully written to table '{TB_UNIQUECOMBO}' in the database.")

    except Exception as e:
        # If an error occurs, print the error message
        print(f"An error occurred: {e}")


def create_loadComboSelectionDB(engine, df: pd.DataFrame):
    """
    Writes a DataFrame to the 'loadcombinationsselection' table in the database.

    Args:
        engine (sqlalchemy.engine.Engine): The database engine.
        df (pd.DataFrame): The DataFrame containing data to write.

    Raises:
        Exception: If an error occurs during the write operation.
    """
    try:
        # Write DataFrame to SQL
        # Write DataFrame to SQL
        df.to_sql(
            TB_COMBOSELECTION,  # Table name
            con=engine,  # SQLAlchemy engine
            if_exists='replace',  # 'replace' if table already exists
            index=False  # Do not write index as a column
        )
        print(
            f"DataFrame successfully written to table '{TB_COMBOSELECTION}' in the database."
        )
    except Exception as e:
        # If an error occurs, print the error message
        print(f"An error occurred: {e}")


def read_loadComboDB(engine):
    """
    Reads a SQL table into a pandas DataFrame.

    Parameters:
    engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.

    Returns:
    pd.DataFrame: The DataFrame containing the table data.
    """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name=TB_UNIQUECOMBO,  # Table name
        con=engine  # SQLAlchemy engine
    )

    return df


def read_loadComboSelectionDB(engine):
    """
    Reads the SQL table `TB_COMBOSELECTION` into a pandas DataFrame.

    Parameters:
    engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.

    Returns:
    pd.DataFrame: The DataFrame containing the table data.
    """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name=TB_COMBOSELECTION,  # The table to read
        con=engine  # The SQLAlchemy engine
    )

    return df  # The DataFrame containing the table data
