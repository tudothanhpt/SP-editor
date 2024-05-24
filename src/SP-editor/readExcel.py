import pandas as pd


def get_SPRequiredData_fromExcel(excel_path: str) -> tuple:
    """
    Get SPColumn file names and AutoCAD file paths from an Excel file.

    Args:
    - excel_path (str): The path to the Excel file.

    Returns:
    - spcolumn_filenames (list): List of SPColumn file names. [0]
    - numForceCombo (list): List of number of user combinations used for each SPcolFile [1]
    - forceSet (list): List of Forceset used for each SPcolFile [2]
    - acad_paths (list): List of AutoCAD file paths. [3]
    """
    # Specify the sheet name or index (zero-based) containing the data
    SHEETNAME = 'SPColumnFileManagement'

    # Read only columns A (1st column) and B (2nd column) from the Excel file
    df_SPmanagement = pd.read_excel(excel_path, sheet_name=SHEETNAME, skiprows=1, usecols="A:M")
    df_SPmanagement = df_SPmanagement.dropna()

    spcolumn_filenames = df_SPmanagement["SPColumnFile"].tolist()
    numForceCombo = df_SPmanagement["#Force Combos"].tolist()
    forceSet = df_SPmanagement["Force"].tolist()
    acad_paths = df_SPmanagement["DXF PATH"].tolist()
    lst_fc = df_SPmanagement["f'c (psi)"].tolist()
    lst_ec = df_SPmanagement["Ec (ksi)"].tolist()
    lst_fy = df_SPmanagement["fy (ksi)"].tolist()
    lst_es = df_SPmanagement["Es (ksi)"].tolist()
    return spcolumn_filenames,numForceCombo,forceSet, acad_paths,lst_fc,lst_ec,lst_fy,lst_es

def main():
    None

if __name__ == "__main__":
    main()