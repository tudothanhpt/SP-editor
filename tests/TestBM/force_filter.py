import pandas as pd
import numpy as np
import comtypes.client

from sp_editor.crud.cr_pier_force import read_pierdesign_forceDB
from sp_editor.crud.cr_level_group import read_groupDB
from sqlmodel import create_engine
from sqlalchemy.engine import Engine
from typing import *
from sp_editor.crud.cr_load_combo import create_loadComboDB, create_loadComboSelectionDB, read_loadComboSelectionDB


#ENSURE THE 2 GIVEN DATAFRAMES' HEADERS TO BE ADDRESSED CORRECTLY FOLLOWING THE BELOW CONVENTION

def connect_to_etabs(model_is_open: bool, file_path: str | None = None) -> tuple:
    """
    Connect to an instance of ETABS and return the SapModel and EtabsObject.

    Parameters:
    model_is_open (bool): Indicates if a model is already open.
    file_path (str | None): The path to the ETABS file to open if a new instance is needed.

    Returns:
    tuple: SapModel and EtabsObject.
    """
    # Create API helper object
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

    if model_is_open:
        try:
            # Get the active ETABS object
            EtabsObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("No running instance of the program found or failed to attach.")
            sys.exit(-1)
    else:
        try:
            # Start a new instance of ETABS
            EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("Cannot start a new instance of the program.")
            sys.exit(-1)
        EtabsObject.ApplicationStart()

    SapModel = EtabsObject.SapModel
    if file_path:
        # Open the specified file
        ret = SapModel.File.OpenFile(file_path)
        if ret != 0:
            print(f"Failed to open file: {file_path}")
            sys.exit(-1)

    return SapModel, EtabsObject


def create_force_filter_df(df_PierForces: pd.DataFrame, df_Tier: pd.DataFrame) -> pd.DataFrame:
    """
    Merge two DataFrames on the 'Story' column, create new columns based on certain operations,
    and return the resulting DataFrame.

    Parameters:
    df1 (pd.DataFrame): Pier Forces DataFrame
    df2 (pd.DataFrame): Group Definition DataFrame

    Returns:
    df3 (pd.DataFrame: The merged DataFrame with new columns.
    """
    df_FilteredForces = df_PierForces.merge(df_Tier, on="Story", how='left')
    
    df_FilteredForces['ID3'] = (
        df_FilteredForces["Story"] + 
        df_FilteredForces["Pier"] + 
        df_FilteredForces["Combo"] + 
        df_FilteredForces["Location"]
    )
    
    df_FilteredForces['P_SPCol'] = np.round(df_FilteredForces['P'], 0).astype(float)*(-1)
    df_FilteredForces['Mx_SPCol'] = np.round(df_FilteredForces["M2"], 0).astype(float)
    df_FilteredForces['My_SPCol'] = np.round(df_FilteredForces["M3"], 0).astype(float)
    
    return df_FilteredForces

def force_filter_SPformat(df3: pd.DataFrame, pier_value: str, tier: str) -> tuple:
    """
    Merge two DataFrames on the 'Story' column, create new columns based on certain operations,
    filter rows based on specific conditions, and generate a formatted result string.

    Parameters:
    df3 (pd.DataFrame: The merged DataFrame with new columns.
    pier_value (str): The value to filter the 'Pier' column
    tier (str): The value to filter the 'Force Grouping' column

    Returns:
    tuple: A tuple containing the result string and the filtered DataFrame.
    """
    
    # Filter rows based on specific conditions
    filter_cond = (df3[HEADER_PIER] == pier_value) & (df3[HEADER_TIER] == tier)
    filter_df = df3.loc[filter_cond, ['P_SPCol', 'Mx_SPCol', 'My_SPCol']]
    
    # Create the 'Combined_Col' column by concatenating 'P_SPCol', 'Mx_SPCol', 'My_SPCol'
    filter_df['Combined_Col'] = filter_df.apply(
        lambda row: f"{row['P_SPCol']},{row['Mx_SPCol']},{row['My_SPCol']}", axis=1
    )
    
    # Get the total number of filtered rows
    total_rows = filter_df.shape[0]
    
    # Convert the 'Combined_Col' column values to a list
    combined_values = filter_df['Combined_Col'].to_list()
    
    # Join the list into a single string with each value on a new line
    load_string = '\n'.join(combined_values)
    
    # Create the result string
    result_string = f"{total_rows}\n{load_string}"
    
    return result_string, total_rows


def set_units_in_etabs_model(sap_model,enum_units: int):
    """
    Set the units in an ETABS model.

    Parameters:
    sap_model (comtypes.client._compointer): The ETABS model object.
    unit_system (int): The unit system to set.

    Returns:
    str: Success message or error message.
    """
    # Set the present units
    ret = sap_model.SetPresentUnits(enum_units)
    
    # Check if the units were successfully set
    if ret == 0:
        return "Units successfully set."
    else:
        return "Error setting units."

def get_pier_force_infor(sap_model: Any, list_combo_selection: list) -> pd.DataFrame:
    SapModel = sap_model
    table_key = 'Design Forces - Piers'
    # Set load combination selected for display
    design_combo = [""]
    SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay(list_combo_selection)
    # Get the database table
    pierforce_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName='')
    if pierforce_db[-1] != 0:
        error_message = (f"<b>Failed to get table for display.<b> "
                         f"<p>PLease make sure: <p>"
                         f"<p> 1. Ensure you have run ETABS <p>"
                         f"<p> 2. Ensure you have designed Piers with selected load combination <p>"
                         f"<p>PLease make sure you design wall with selected load combination. <p>"
                         f"<p> Return code: {pierforce_db[-1]}.<p>")
        return pd.DataFrame()

    # Extract header and data
    header = pierforce_db[2]
    data_values = pierforce_db[4]

    # Group the data values into rows
    rows = [data_values[i:i + len(header)] for i in range(0, len(data_values), len(header))]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)

    return df


def get_current_unit(SapModel) -> Tuple[str, str, str]:
    current_units = SapModel.GetPresentUnits()
    """    
    LB_IN = 1
    LB_FT = 2
    KIP_IN = 3
    KIP_FT = 4
    KN_MM = 5
    KN_M = 6
    N_MM = 7
    N_M = 8
    
    """
    
    if current_units < 4:
        enum_force = 4
        enum_Section = 1
        enum_cti = 0
    else:
        enum_force = 6
        enum_Section = 7
        enum_cti = 1
    return enum_force, enum_Section, enum_cti

from sp_editor.crud.cr_general_infor import get_infor


def main():
    engine_temppath = r"C:\Users\abui\Desktop\Git\Repo\SP-editor\tests\DemoNo1.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
    general_infor = get_infor(engine)
    CTI_unit = general_infor.unit_system
    print(CTI_unit)

if __name__ == "__main__":
    main()
