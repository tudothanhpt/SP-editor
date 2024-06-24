import subprocess
import pandas as pd
import os
import sys
#from sp_editor.core.cti_data_merging import read_summaryCTI_DB
from sqlmodel import Session,create_engine
from sqlalchemy.engine.base import Engine
from sp_editor.utils import  get_engine_path

from PySide6 import QtWidgets as qtw

# Define the constant path to spColumn.CLI.exe
SPCOLUMN_PATH = r"D:\spColumn\StructurePoint\spColumn\spColumn.CLI.exe"



batch_file_path = r"C:\Users\abui\Desktop\Git\Repo\SP-editor\run_spColumn.bat"
def create_batch_file(engine, batch_file_path):
    options = ["/rcsv"]
    try:
        df_CTIsummary = read_summaryCTI_DB(engine)
        input_files = df_CTIsummary["PathAfterCreation"].tolist()
        filename = df_CTIsummary["ID2"].tolist()

        with open(batch_file_path, 'w') as batch_file:
            for i in range(len(df_CTIsummary)):
                input_dir = os.path.dirname(input_files[i])
                output_folder = os.path.join(input_dir, "outputs")
                os.makedirs(output_folder, exist_ok=True)
                output_file = os.path.join(output_folder, filename[i])

                batch_file.write(f'"{SPCOLUMN_PATH}" /i:"{input_files[i]}" /o:"{output_file}.out" ' + ' '.join(options) + '\n')

        return True, f"Batch file created successfully: {batch_file_path}"

    except FileNotFoundError:
        error_message = f"The file '{SPCOLUMN_PATH}' was not found. Please check the path and try again."
        return False, error_message

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        return False, error_message

def show_message_box(title, message):

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()

def read_summaryCTI_DB(engine):
    """
    """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name="ctisummary",  # The table to read
        con=engine  # The SQLAlchemy engine
    )
    return df  # The DataFrame containing the table data

if __name__ == "__main__":
    # Example SQLAlchemy engine setup (SQLite in this case)
    engine_temppath = r"C:\Users\AnhBui\Desktop\testCTI\12345.spe"
    engine = create_engine(f"sqlite:///{engine_temppath}")
    engine_path = get_engine_path(engine)
    batch_file_path = os.path.join(engine_path, "run_spColumn.bat")
    create_batch_file(engine, batch_file_path)
    print("done")
    os.startfile(batch_file_path)
