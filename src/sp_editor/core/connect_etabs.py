# -*- coding: utf-8 -*-
from typing import Any

import comtypes.client
import sys
import pandas as pd
import numpy as np
from pandas import DataFrame


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


lst_PierSDShape = list[dict[str, list[list[float]]]]


def get_story_infor() -> DataFrame:
    """
    returns: DataFrame

    Return dataframe of list level

    """
    SapModel, EtabsObject = connect_to_etabs(model_is_open=True)

    # get the table
    table_key: str = 'Story Definitions'

    # get the database table
    story_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName='')
    # Extract header and data
    header = story_db[2]
    data_values = story_db[4]

    # Group the data values into rows
    rows = [data_values[i:i + len(header)] for i in range(0, len(data_values), len(header))]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)

    # Select only the 'Story' and 'Height' columns
    df_selected = df[['Story', 'Height']]
    return df_selected


def get_sdshape_pierPolygon() -> lst_PierSDShape:
    """
    returns: lst_PierSDShape (list)
    
    Return list of corresponding [X,Y] values forming each pier SD shape

    """
    SapModel, EtabsObject = connect_to_etabs()

    # get the table
    table_key: str = 'Section Designer Shapes - Concrete Polygon'

    # get the database table
    sdshapes_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName='')
    lst_tblHeader: list = sdshapes_db[2]
    lst_tblValues: list = sdshapes_db[4]
    lst_Data: list[list] = [lst_tblValues[i:i + len(lst_tblHeader)] for i in
                            range(0, len(lst_tblValues), len(lst_tblHeader))]

    # Create DataFrame of concrete polygon
    df_SD: pd.DataFrame = pd.DataFrame(lst_Data, columns=lst_tblHeader)

    # get lst of unique SD shapes
    lst_unique_SDshape_names = df_SD['SectionName'].unique()

    # Create list of Piers' dictionary
    lst_PierSDShape: list = []
    for str_SDsectionname in lst_unique_SDshape_names:
        # Create a "sub" dataframe for section name
        df_sectionname = df_SD[df_SD['SectionName'] == str_SDsectionname]

        # Gather the corresponding list of [X,Y] forming the closed boundary.
        X_Y_pairs: list[list[float]] = df_sectionname[['X', 'Y']].astype(float).values.tolist()
        # Create a dictionary defining each section
        dict_Section: dict[str, list[list[float]]] = {str_SDsectionname: X_Y_pairs}

        # Create a list of PierSDshape
        lst_PierSDShape.append(dict_Section)

    return lst_PierSDShape;


def get_current_unit(SapModel) -> tuple[str, str, str]:
    force_units_ETABS: dict[str, int] = {"lb": 1, "kip": 2, "Kip": 2, "N": 3, "kN": 4, "KN": 4, "kgf": 5, "Kgf": 5,
                                         "tonf": 6, "Tonf": 6}
    length_units_ETABS: dict[str, int] = {"inch": 1, "ft": 2, "micron": 3, "mm": 4, "cm": 5, "m": 6}
    force: str = "lb"
    length: str = "inch"
    force_enum, len_enum, *argv = SapModel.GetPresentUnits_2()
    for key, value in force_units_ETABS.items():
        if force_enum == value:
            force = key
            break
    for key, value in length_units_ETABS.items():
        if len_enum == value:
            length = key
            break
    if force_enum <= 2 and len_enum <= 2:
        unitsystem = "English Unit"
    elif force_enum > 2 and len_enum > 2:
        unitsystem = "Metric Units"
    else:
        unitsystem = "Blend"
    return force, length, unitsystem


def read_table(SapModel, table_key: str) -> list[list[str]]:
    GroupName = table_key
    FieldKeyList = []
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []
    a: list[str] = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, FieldKeyList, GroupName, TableVersion,
                                                                   FieldsKeysIncluded, NumberRecords, TableData)
    lst_tableHeader = list(a[2])
    lst_tableContent = list(a[4])
    lst_Content = [lst_tableContent[i:i + len(lst_tableHeader)] for i in
                   range(0, len(lst_tableContent), len(lst_tableHeader))]

    return lst_Content


def SPcolumnPierPoint(lst_PierSDShape, pierIndex):
    # Split the values list into sublists
    list1 = lst_PierSDShape[pierIndex]

    # List of points (X, Y) - pop the outter bracket
    points = list(list1.values()).pop()
    points.append(points[0])

    # Convert points to the desired format
    formatted_points = [f"{point[0]}, {point[1]}" for point in points]

    # Join formatted points with newline characters
    spColumn_Points = "\n".join(formatted_points)

    # Add the length of the list at the beginning
    result = str(1) + f"\n{len(points)}\n{spColumn_Points}"
    return result


def SPcolumnPierLabel(lst_PierSDShape, pierIndex):
    # Split the values list into sublists
    list1 = lst_PierSDShape[pierIndex]

    PierLabel = str(list(list1.keys()).pop())

    # Add the length of the list at the beginning

    return PierLabel
