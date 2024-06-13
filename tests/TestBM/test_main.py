from typing import Any

import comtypes.client
import sys
import pandas as pd

from sp_editor.database.models import LoadCombinations
from sqlmodel import Session, create_engine, text
from sqlalchemy.engine.base import Engine
from pandas import DataFrame
from sqlmodel import Session

table_name='loadcombinations'

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

def get_load_combinations(SapModel) -> DataFrame:
    """
    returns: DataFrame

    Return dataframe of list level

    """
    # get the table
    table_key: str = 'Load Combination Definitions'
    # get the database table
    story_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName='')
    # Extract header and data
    header = story_db[2]
    data_values = story_db[4]

    # Group the data values into rows
    rows = [data_values[i:i + len(header)] for i in range(0, len(data_values), len(header))]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)
    df_uLoadCombination= df['Name'].unique()
    df_uLoadCombination = pd.DataFrame(df_uLoadCombination, columns=['LoadCombinations'])
    df_uLoadCombination["SelectedCombo"]= None
    print(df_uLoadCombination)
    #lst_uLoadCombination = df_uLoadCombination["Name"].tolist()
    return df_uLoadCombination


def create_df_to_db(engine, db_table_name, df:pd.DataFrame):
    try:
        # Write DataFrame to SQL
        df.to_sql(db_table_name, con=engine, if_exists='replace', index=False)
        print(f"DataFrame successfully written to table '{db_table_name}' in the database.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
 

if __name__ == '__main__':
    engine_temppath = r"C:\Users\abui\Desktop\Git\repo\SP-editor\tests\TestBM\1235.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
    table_name='loadcombinations'
    df_uLoadCombination = get_load_combinations(connect_to_etabs(model_is_open=True)[0])
    create_df_to_db(engine,table_name, df_uLoadCombination)
    #df_sorted = get_df_load_combinations_fromdb(engine)
    
