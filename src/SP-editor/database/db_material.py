import pandas as pd
import sys
import os
sys.path.append(os.getcwd())
import json

import pandas as pd
from sqlmodel import Field, Session, SQLModel, create_engine, text
from sqlalchemy.engine import Engine  # Ensure compatibility with SQLModel
from typing import Optional, List, Dict, Any
from PyQt6.QtWidgets import QApplication, QMessageBox

def show_file_not_found_message(message: str):
    """
    Display a QMessageBox indicating that the database file does not exist.
    """
    app = QApplication(sys.argv)  # Initialize QApplication
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.setWindowTitle("File Not Found")
    msg_box.exec() 

class ConcreteMaterial(SQLModel, table=True):
    """
    Concrete material properties
    """
    id: int | None = Field(default=None, primary_key=True)
    name: Optional[str] = None
    fc: Optional[float] = None
    Ec: Optional[float] = None
    max_fc: Optional[float] = None
    beta_1: Optional[float] = None
    eu: Optional[float] = None


class SteelMaterial(SQLModel, table=True):
    """
    Steel material properties
    """
    id: int | None = Field(default=None, primary_key=True)
    name: Optional[str] = None
    fy: Optional[float] = None
    Es: Optional[float] = None
    ety: str = Field(default="0.0021")


def clear_tables(engine: Engine) -> None:
    """Clear all data from the MaterialSteel and MaterialConcrete tables.
    
    Args:
        engine (Engine): The database engine.
    """
    with Session(engine) as session:
        session.exec(text("DELETE FROM steelmaterial"))
        session.exec(text("DELETE FROM concretematerial"))
        session.commit()


def insert_json_to_db(engine: Engine, json_path: str) -> None:
    """Insert data from a JSON file into the database.
    
    Args:
        engine (Engine): The database engine.
        json_path (str): The path to the JSON file.
    
    Raises:
        FileNotFoundError: If the JSON file is not found.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    # Read the JSON file into a DataFrame
    df = pd.read_json(json_path)
    pseudo_dict: List[Dict[str, Any]] = df.to_dict(orient="records")

    # Remove 'id' field from each dictionary in the pseudo-dictionary
    for row in pseudo_dict:
        row.pop("id", None)

    with Session(engine) as session:
        # Clear existing data in the tables
        clear_tables(engine)

        # Insert new data with renumbered IDs starting from 0
        for idx, row in enumerate(pseudo_dict, start=0):
            row['id'] = idx
            material_concrete_instance = ConcreteMaterial(**row)
            material_steel_instance = SteelMaterial(**row)
            session.add(material_concrete_instance)
            session.add(material_steel_instance)

        # Commit the session to save the changes
        session.commit()


def set_engine(database_path: str) -> Optional[Engine]:
    """Create the SQLite database engine.
    
    Args:
        database_path (str): The file path to the SQLite database.
    
    Returns:
        Optional[Engine]: The created database engine, or None if the database file does not exist.
    """
    if not os.path.exists(database_path):
        show_file_not_found_message("No Existing Database")
        return None

    return create_engine(f"sqlite:///{database_path}", echo=False)


def create_material_db(engine: Optional[Engine]) -> None:
    """Create tables in the database if the engine is valid.
    
    Args:
        engine (Optional[Engine]): The database engine.
    """
    if engine is None:
        show_file_not_found_message("No Existing Database")
        return

    # Create tables defined by SQLModel in the database
    SQLModel.metadata.create_all(engine)

def initialize_basic_database(engine: Optional[Engine], json_path: str) -> None:
    """Initialize the basic database: create tables and insert data."""
    if engine:
        create_material_db(engine)
        try:
            insert_json_to_db(engine, json_path)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Failed to set up the database engine.")

def main() -> None:
    """Main function to set up the database and insert data from a JSON file."""
    # Define paths to the database and JSON file
    database_path = r"C:\Users\abui\Documents\BM\git\repo\SP-editor\tests\test.db"
    json_path = r"src\SP-editor\database\material_table\tb_ASTM_A615_rebarGr.json"

    # Set up the database engine
    engine = set_engine(database_path)
    initialize_basic_database(engine, json_path)

if __name__ == "__main__":
    main()