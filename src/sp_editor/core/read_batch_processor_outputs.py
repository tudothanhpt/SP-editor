import pandas as pd
import os
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt


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
    file_name_output_xlsx = [
        os.path.splitext(file_name)[0] + ".xlsx" for file_name in file_names
    ]

    # Get list of directory paths containing the files
    directories = [os.path.dirname(file_path) for file_path in path_list]

    # Create new paths with "/outputs/" added to each directory path and append ".xlsx" file names
    output_xlsx_paths = [
        os.path.join(directory, "outputs", output_xlsx)
        for directory, output_xlsx in zip(directories, file_name_output_xlsx)
    ]

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
            errors.append(
                f"<b>Warning:</b> The output '{output_path}' does not exist please make sure you have run the batch processor."
            )

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
        msg_box.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )

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
        df = xl.parse(sheet_name="6", header=None, usecols="A:K")
        xl.close()
        # Locate
        row_index = df[
            df.apply(
                lambda row: row.astype(str).str.contains("No.", case=True).any(), axis=1
            )
        ].index[0]

        header_location = df.iloc[row_index]
        df = pd.DataFrame(df.values[row_index + 2 :], columns=header_location)
        # Create a custom headers - ensure no abnormal things among xls file
        custom_headers = [
            "No.",
            "Pu",
            "Mux",
            "Muy",
            "phiPn",
            "phiMnx",
            "phiMny",
            "NA_Depth",
            "epsilon_t",
            "phi",
            "DCR",
        ]
        df.columns = custom_headers
        # drop unit row
        df = df.iloc[1:]

        df["spColumnFile"] = os.path.splitext(os.path.basename(filepath))[0] + ".cti"
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

    df_output["id"] = range(1, len(df_output) + 1)

    df_output = df_output.loc[
        :, ["id", "spColumnFile", "DCR", "No.", "Pu", "Mux", "Muy"]
    ]
    print(df_output)
    return df_output


def max_dcr_from_outputs(df: pd.DataFrame):
    """
    This function takes a DataFrame and returns a new DataFrame containing the rows with the maximum DCR value
    for each unique spColumnFile. If a TypeError or ValueError occurs, a pseudo DataFrame is created and included.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the columns 'id', 'spColumnFile', 'DCR', 'Pu', 'Mux', and 'Muy'.

    Returns:
    pd.DataFrame: A DataFrame with the rows having the maximum DCR for each spColumnFile, or a pseudo DataFrame in case of error.
    """
    # Initialize an empty DataFrame to store the summary
    df_max_dcr_per_spColumn = pd.DataFrame(
        columns=["id", "spColumnFile", "DCR", "No.", "Pu", "Mux", "Muy"]
    )

    # Get unique values from the spColumnFile column
    unique_spColumnFiles = df["spColumnFile"].unique()

    for spColumnFile in unique_spColumnFiles:
        try:
            # Find the row with the maximum DCR for each spColumnFile
            max_dcr_row = df.loc[
                df.loc[df["spColumnFile"] == spColumnFile, "DCR"]
                .astype(str)
                .replace({">": ""})
                .astype(float)
                .idxmax()
            ]
            # Append the row to the summary DataFrame
            df_max_dcr_per_spColumn = pd.concat(
                [df_max_dcr_per_spColumn, max_dcr_row.to_frame().T], ignore_index=True
            )
        except (TypeError, ValueError) as e:
            print(
                f"TypeError or ValueError: {e} - Creating pseudo DataFrame for {spColumnFile}"
            )
            # Create pseudo DataFrame in case of error
            dict_max_os = {
                "id": ["-"],
                "spColumnFile": [spColumnFile],
                "DCR": ["o/s"],
                "Pu": ["Pu > Pmax"],
                "Mux": ["-"],
                "Muy": ["-"],
            }
            df_max_os = pd.DataFrame(dict_max_os)
            # Append the pseudo DataFrame to the summary DataFrame
            df_max_dcr_per_spColumn = pd.concat(
                [df_max_dcr_per_spColumn, df_max_os], ignore_index=True
            )

    return df_max_dcr_per_spColumn


if __name__ == "__main__":
    df = make_df_from_outputs(
        [
            "C:\\Users\\abui\\Desktop\\New folder\\t1\\P1\\outputs\\t1_P1.xlsx",
            "C:\\Users\\abui\\Desktop\\New folder\\t1\\P1\\outputs\\t1_P1_!.xlsx",
        ]
    )
    df1 = max_dcr_from_outputs(df)
    print(df1)
