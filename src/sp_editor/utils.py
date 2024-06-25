import sys
import os
import comtypes.client
import errno
import csv
import pandas as pd

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from io import StringIO
from sqlalchemy.engine.url import make_url

def get_new_filename(suffix) -> str:
    rv, _ = qtw.QFileDialog.getSaveFileName(caption="New File", filter=suffix)
    if rv != '' and not rv.endswith(suffix): rv

    return rv


def open_url(url):
    qtg.QDesktopServices.openUrl(qtc.QUrl(url))


def about_dialog(parent, title, text):
    qtw.QMessageBox.about(parent, title, text)


def get_save_filename(suffix):
    rv, _ = qtw.QFileDialog.getSaveFileName(caption="Save File", filter='*.{}'.format(suffix))
    if rv != '' and not rv.endswith(suffix): rv += '.' + suffix

    return rv


def get_open_filename(suffix, curr_dir):
    rv, _ = qtw.QFileDialog.getOpenFileName(caption="Open Model File", dir=curr_dir, filter=suffix)
    if rv == '' and not rv.endswith(suffix):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), rv
        )

    return rv


def confirm(parent, title, msg):
    rv = qtw.QMessageBox.question(parent, title, msg, qtw.QMessageBox.Yes, qtw.QMessageBox.No)

    return True if rv == qtw.QMessageBox.Yes else False


def write_to_csv(data, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def select_csv_file() -> [str]:
    app = qtw.QApplication(sys.argv)
    dialog = qtw.QFileDialog()
    dialog.setNameFilter("CSV files (*.csv)")
    dialog.setViewMode(dialog.List)
    dialog.setFileMode(dialog.ExistingFile)

    if dialog.exec_():
        file_paths = dialog.selectedFiles()
        if file_paths:
            return file_paths[0]  # Return the first selected file path
    return None

def prompt_json_file(base_dir: str) -> None:
    """Prompt user to select a JSON file for loading data."""
    file_dialog = qtw.QFileDialog()
    file_dialog.setFileMode(qtw.QFileDialog.ExistingFile)
    file_dialog.setNameFilter("JSON files (*.json)")
    file_dialog.setDirectory(base_dir)
    if file_dialog.exec():
        file_path = file_dialog.selectedFiles()[0]
        return file_path

def read_json_to_df(json_file_path: str) -> pd.DataFrame:
    """Read a JSON file and return a pandas DataFrame."""
    with open(json_file_path, 'r') as file:
        json_data = file.read()

    # Use StringIO to create a stream from the JSON string
    json_stream = StringIO(json_data)

    # Read the JSON data into a pandas DataFrame
    df = pd.read_json(json_stream)
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
    
    return df

def write_string_to_file(folder_path, file_name, string_to_write):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(folder_path, file_name+".txt")
    
    # Write the text to the file
    with open(file_path, "w") as file:
        file.write(string_to_write)
        
def get_engine_path(engine):
    # Parse the engine's URL using SQLAlchemy's make_url
    url = make_url(engine.url)
    
    # Extract the path (for SQLite, the path starts with '/', so we strip the first character)
    db_path = url.database if url.drivername == 'sqlite' else url.database
    # Extract the folder that stores the database
    db_folder = os.path.dirname(db_path)
    
    return db_folder

def get_attribute_names(cls):
    return list(cls.__annotations__.keys())