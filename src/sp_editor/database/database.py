from sqlmodel import SQLModel, create_engine


def create_db_and_tables(file_name: str):
    sqlite_file_name = file_name
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url)
    SQLModel.metadata.create_all(engine)
    return engine


def connect_db_and_tables(file_name: str):
    sqlite_file_name = file_name
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url)
    return engine
