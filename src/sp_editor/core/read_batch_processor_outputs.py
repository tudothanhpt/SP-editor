import pandas as pd
import os
import numpy as np
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt


def get_o_xlsx_paths_from_cti_paths(path_list):
    """
    Returns a list of new paths with "/outputs/" added to each directory path and ".xlsx" appended to each file name.

    Parameters:
    path_list (list): List of full file paths.

    Returns:
    list: List of new paths with ".xlsx" appended to file names and "/outputs/" added to directory paths.
    """
    # Get list of file names from full file paths without extensions and append ".xlsx"
    file_names = [os.path.basename(file_path) for file_path in path_list]
    file_name_output_xlsx = [os.path.splitext(file_name)[0] + ".xlsx" for file_name in file_names]

    # Get list of directory paths containing the files
    directories = [os.path.dirname(file_path) for file_path in path_list]
    
    # Create new paths with "/outputs/" added to each directory path and append ".xlsx" file names
    output_xlsx_paths = [os.path.join(directory, "outputs", output_xlsx) for directory, output_xlsx in zip(directories, file_name_output_xlsx)]
    
    return output_xlsx_paths    

def check_output_paths_exist(output_paths):
    """
    Checks if each output path in the list exists. Shows a single QMessageBox with a list of errors if any path does not exist.

    Parameters:
    output_paths (list): List of output paths to check.
    """
    errors = []

    for output_path in output_paths:
        if not os.path.exists(output_path):
            errors.append(f"<b>Warning:</b> The output '{output_path}' does not exist please make sure you have run the batch processor.")
                
    if errors:
        error_message = "<br>".join(errors)
        
        # Create a QMessageBox instance
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Errors Found")
        msg_box.setText(error_message)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        
        # Set text interaction flags to enable vertical scroll bar
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)

        # Execute the message box
        msg_box.exec()

def read_excel_sheet(filepath):
    """
    Read data from a specific sheet in an Excel file and return a DataFrame.

    Parameters:
    - filepath (str): Path to the Excel file.
    - sheet_name (str): Name of the sheet to read.

    Returns:
    - pd.DataFrame: DataFrame containing the data from the read sheet.
    """
    try:
        # Read the Excel file
        xl = pd.ExcelFile(filepath)
        # Select the sheet to read
        df = xl.parse(sheet_name="6", header=0, skiprows=3, usecols="B:K")
        # Create a custom headers - ensure no abnormal things among xls file
        custom_headers = ['Pu', 'Mux', 'Muy', 'phiPn', 'phiMnx', 'phiMny', 'NA_Depth', 'epsilon_t', 'phi', 'DCR']
        df = df.iloc[1:]
        df.columns = custom_headers
        # Create sub columns to match database
        df['spColumnFile'] = os.path.splitext(os.path.basename(filepath))[0]+".cti"
        # Rearrange the column to match database order
        # Return the read DataFrame
        return df
    
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"Error reading Excel file '{filepath}': {str(e)}")
        return None

def make_df_from_outputs(path_list):
    df_output = pd.DataFrame()
    for path in path_list:
        df = read_excel_sheet(path)
        df_output = pd.concat([df_output, df], ignore_index=True)
    
    df_output['id'] = range(1, len(df_output) + 1)
    df_output = df_output.loc[:,['id','spColumnFile','DCR','Pu', 'Mux', 'Muy']]
    
    return df_output

def max_dcr_from_outputs(df: pd.DataFrame):
   df_max_dcr_per_spColumn = df.loc[df.groupby("spColumnFile")["DCR"].idxmax()] 

   return (df_max_dcr_per_spColumn)

