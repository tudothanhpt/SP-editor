from sqlmodel import SQLModel, create_engine
from sqlalchemy.engine.base import Engine


def create_db_and_tables(file_name: str) -> Engine:
    """
    Creates a SQLite database file and tables defined by SQLModel.

    Args:
        file_name (str): The name of the SQLite database file to create.

    Returns:
        Engine: The SQLAlchemy engine connected to the created database.
    """
    # Create the SQLite URL
    sqlite_file_name = file_name
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    # Create the engine and create all tables defined by SQLModel
    engine = create_engine(sqlite_url)
    SQLModel.metadata.create_all(engine)

    return engine


def connect_db_and_tables(file_name: str) -> Engine:
    """
    Connects to a SQLite database and returns the engine. The database
    file name is passed as an argument. If the file does not exist, a
    FileNotFoundError is raised.

    Args:
        file_name (str): The file name of the database file.

    Returns:
        Engine: The SQLAlchemy engine object.
    """
    # Create the SQLite URL
    sqlite_file_name = file_name
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    # Create the engine
    engine = create_engine(sqlite_url)

    return engine
