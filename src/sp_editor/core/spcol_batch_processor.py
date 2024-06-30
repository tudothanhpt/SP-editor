<<<<<<< HEAD
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
=======
import os
import subprocess
import pandas as pd
from PySide6.QtCore import Signal, QThread
from sqlalchemy.engine.base import Engine

# DEFAULT BY INSTALLATION, PLEASE CHANGE THIS IF NOT COMPATIBLE WITH YOUR COMPUTER'S SETTINGS
SPCOLUMN_PATH = r"C:\Program Files (x86)\StructurePoint\spColumn\spColumn.CLI.exe"
>>>>>>> 8c64ccd2a73bd296cb200aeea0859021b9ebeed6


class BatchProcessorThread(QThread):
    error = Signal(str)
    success = Signal(str)
    output = Signal(str)

<<<<<<< HEAD
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
=======
    def __init__(self, engine: Engine, input_files: list[str], options: list[str] = ["/rcsv"]):
        super().__init__()
        self.engine = engine
        self.options = options
        self.input_files = input_files

    def run(self):
        """
        This method is executed when the thread starts. It performs the following steps:
        
        1. Checks if the SPCOLUMN_PATH is valid.
        2. Reads the CTI summary database to get the input files.
        3. Creates a batch file containing commands to process the input files with spColumn.CLI.exe.
        4. Executes the batch file and captures the output.
        5. Emits signals based on the success or failure of the process.
        """
        try:
            # Step 1: Check if the spColumn executable exists
            if not os.path.isfile(SPCOLUMN_PATH):
                error_message = f"The file '{SPCOLUMN_PATH}' was not found. Please check the path and try again."
                self.error.emit(error_message)
                return
            # Step 2: check if the inputted list is empty
            try:
                if not self.input_files:
                    error_message = "The input file list is empty. Please provide a list of input files and try again."
                    self.error.emit(error_message)
                    return

            except Exception as e:
                error_message = f"An error occurred while reading the summary CTI database: {e}"
                self.error.emit(error_message)
                return

            # Step 3: Prepare the batch file path
            engine_folder_path = os.path.dirname(self.engine.url.database)
            batch_file_path = os.path.join(engine_folder_path, "run_spColumn.bat")

            # Write the batch file with commands
            with open(batch_file_path, 'w') as batch_file:
                for i in range(len(self.input_files)):
                    input_dir = os.path.dirname(self.input_files[i])
                    filename = os.path.basename(self.input_files[i])
                    filename = os.path.splitext(filename)[0]
                    output_folder = os.path.join(input_dir, "outputs")
                    os.makedirs(output_folder, exist_ok=True)
                    output_file = os.path.join(output_folder, filename)

                    # Write command line instructions to the batch file
                    batch_file.write(f'"{SPCOLUMN_PATH}" /i:"{self.input_files[i]}" /o:"{output_file}.out" ' + ' '.join(
                        self.options) + '\n')

            try:
                # Step 4: Execute the batch file
                process = subprocess.Popen(
                    [batch_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    text=True
                )
                for line in iter(process.stdout.readline, ''):
                    self.output.emit(line)
                process.stdout.close()
                process.wait()

                # Check for errors in execution
                if process.returncode != 0:
                    raise subprocess.CalledProcessError(process.returncode, process.args)

                # Step 5: Emit success signal
                self.success.emit(f"Batch file created and executed successfully: {batch_file_path}")
            except subprocess.CalledProcessError as e:
                error_message = f"Batch File Execution Error: {e}"
                self.error.emit(error_message)

        except FileNotFoundError:
            error_message = f"The file '{SPCOLUMN_PATH}' was not found. Please check the path and try again."
            self.error.emit(error_message)

        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            self.error.emit(error_message)
>>>>>>> 8c64ccd2a73bd296cb200aeea0859021b9ebeed6
