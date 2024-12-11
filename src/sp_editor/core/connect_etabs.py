# -*- coding: utf-8 -*-
from typing import Any
import sys

from PySide6 import QtWidgets as qtw
from sqlalchemy.engine.base import Engine
from sp_editor.crud.cr_general_infor import get_infor

import comtypes.client
import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import *


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
    helper = comtypes.client.CreateObject("ETABSv1.Helper")
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


def set_global_unit(SapModel, engine: Engine):
    general_infor = get_infor(engine)
    CTI_unit = general_infor.unit_system
    if CTI_unit == "English Unit":
        SapModel.SetPresentUnits(1)
    elif CTI_unit == "Metric Units":
        SapModel.SetPresentUnits(5)


def get_current_unit(SapModel) -> Tuple[int, int, int]:
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
    else:
        enum_force = 6
        enum_Section = 7
    return enum_force, enum_Section


def get_story_infor(sap_model: Any, etabs_object: Any) -> DataFrame:
    """
    returns: DataFrame

    Return dataframe of list level

    """
    SapModel = sap_model
    EtabsObject = etabs_object
    # get the table
    table_key: str = "Story Definitions"

    # get the database table
    story_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName="")
    # Extract header and data
    header = story_db[2]
    data_values = story_db[4]

    # Group the data values into rows
    rows = [
        data_values[i : i + len(header)]
        for i in range(0, len(data_values), len(header))
    ]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)

    # Select only the 'Story' and 'Height' columns
    df_selected = df[["Story", "Height"]]
    return df_selected


def get_pier_label_infor(sap_model: Any, etabs_object: Any) -> DataFrame:
    SapModel = sap_model
    EtabsObject = etabs_object
    # get the table
    table_key: str = "Area Assignments - Pier Labels"

    # get the database table
    story_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName="")
    # Extract header and data
    header = story_db[2]
    data_values = story_db[4]

    # Group the data values into rows
    rows = [
        data_values[i : i + len(header)]
        for i in range(0, len(data_values), len(header))
    ]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)

    return df


def get_pier_force_infor(
    sap_model: Any, etabs_object: Any, design_combo: list[str]
) -> DataFrame:
    SapModel = sap_model
    EtabsObject = etabs_object
    table_key = "Design Forces - Piers"

    enum_force, enum_Section = get_current_unit(SapModel)

    sap_model.SetPresentUnits(enum_force)

    # Set load combination selected for display
    SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay(design_combo)

    # Get the database table
    pierforce_db = SapModel.DatabaseTables.GetTableForDisplayArray(
        table_key, GroupName=""
    )
    if pierforce_db[-1] != 0:
        error_message = (
            f"<b>Failed to get table for display.<b> "
            f"<p>PLease make sure: <p>"
            f"<p> 1. Ensure you have run ETABS <p>"
            f"<p> 2. Ensure you have designed Piers with selected load combination <p>"
            f"<p>PLease make sure you design wall with selected load combination. <p>"
            f"<p> Return code: {pierforce_db[-1]}.<p>"
        )
        show_warning(error_message)
        return pd.DataFrame()

    # Extract header and data
    header = pierforce_db[2]
    data_values = pierforce_db[4]

    # Group the data values into rows
    rows = [
        data_values[i : i + len(header)]
        for i in range(0, len(data_values), len(header))
    ]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)
    message = f"{len(design_combo)} load combinations extracted."
    show_information(message)
    return df


def get_section_designer_shape_infor(sap_model: Any, etabs_object: Any) -> DataFrame:
    """

    Return list of corresponding [X,Y] values forming each pier SD shape

    """
    SapModel = sap_model
    EtabsObject = etabs_object

    enum_force, enum_Section = get_current_unit(SapModel)

    sap_model.SetPresentUnits(enum_Section)

    table_key = "Section Designer Shapes - Concrete Polygon"

    # Get the database table
    SDS_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName="")
    if SDS_db[-1] != 0:
        error_message = (
            f"<b>Failed to get table for display.<b> "
            f"<p>PLease make sure you defined general pier sections. <p>"
            f"<p> Return code: {SDS_db[-1]}.<p>"
        )
        show_warning(error_message)
        return pd.DataFrame()

    # Extract header and data
    header = SDS_db[2]
    data_values = SDS_db[4]

    # Group the data values into rows
    rows = [
        data_values[i : i + len(header)]
        for i in range(0, len(data_values), len(header))
    ]

    # Create the DataFrame
    df_SD = pd.DataFrame(rows, columns=header)

    df_SD["X"] = pd.to_numeric(df_SD["X"], errors="coerce")
    df_SD["X"] = np.round(df_SD["X"], 2)
    df_SD["Y"] = pd.to_numeric(df_SD["Y"], errors="coerce")
    df_SD["Y"] = np.round(df_SD["Y"], 2)
    df_SD = df_SD[["SectionType", "SectionName", "ShapeName", "X", "Y"]]

    return df_SD


def show_warning(message: str):
    msg_box = qtw.QMessageBox()
    msg_box.setIcon(qtw.QMessageBox.Warning)
    msg_box.setText(message)
    msg_box.setWindowTitle("Warning")
    msg_box.exec()


def show_information(message: str):
    msg_box = qtw.QMessageBox()
    msg_box.setIcon(qtw.QMessageBox.Information)
    msg_box.setText(message)
    msg_box.setWindowTitle("Information")
    msg_box.exec()


lst_PierSDShape = list[dict[str, list[list[float]]]]


def get_sdshape_pierPolygon() -> lst_PierSDShape:
    """
    returns: lst_PierSDShape (list)

    Return list of corresponding [X,Y] values forming each pier SD shape

    """
    SapModel, EtabsObject = connect_to_etabs()

    # get the table
    table_key: str = "Section Designer Shapes - Concrete Polygon"

    # get the database table
    sdshapes_db = SapModel.DatabaseTables.GetTableForDisplayArray(
        table_key, GroupName=""
    )
    lst_tblHeader: list = sdshapes_db[2]
    lst_tblValues: list = sdshapes_db[4]
    lst_Data: list[list] = [
        lst_tblValues[i : i + len(lst_tblHeader)]
        for i in range(0, len(lst_tblValues), len(lst_tblHeader))
    ]

    # Create DataFrame of concrete polygon
    df_SD: pd.DataFrame = pd.DataFrame(lst_Data, columns=lst_tblHeader)

    # get lst of unique SD shapes
    lst_unique_SDshape_names = df_SD["SectionName"].unique()

    # Create list of Piers' dictionary
    lst_PierSDShape: list = []
    for str_SDsectionname in lst_unique_SDshape_names:
        # Create a "sub" dataframe for section name
        df_sectionname = df_SD[df_SD["SectionName"] == str_SDsectionname]

        # Gather the corresponding list of [X,Y] forming the closed boundary.
        X_Y_pairs: list[list[float]] = (
            df_sectionname[["X", "Y"]].astype(float).values.tolist()
        )
        # Create a dictionary defining each section
        dict_Section: dict[str, list[list[float]]] = {str_SDsectionname: X_Y_pairs}

        # Create a list of PierSDshape
        lst_PierSDShape.append(dict_Section)

    return lst_PierSDShape


def read_table(SapModel, table_key: str) -> list[list[str]]:
    GroupName = table_key
    FieldKeyList = []
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []
    a: list[str] = SapModel.DatabaseTables.GetTableForDisplayArray(
        table_key,
        FieldKeyList,
        GroupName,
        TableVersion,
        FieldsKeysIncluded,
        NumberRecords,
        TableData,
    )
    lst_tableHeader = list(a[2])
    lst_tableContent = list(a[4])
    lst_Content = [
        lst_tableContent[i : i + len(lst_tableHeader)]
        for i in range(0, len(lst_tableContent), len(lst_tableHeader))
    ]

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


def get_loadCombo_df_fromE(SapModel) -> Tuple[DataFrame, DataFrame]:
    """
    Returns two dataframes: one with unique load combinations and another with all load combinations.
    The second dataframe also has a column for selected load combinations.

    Args:
        SapModel (Any): The SapModel object from ETABS.

    Returns:
        Tuple[DataFrame, DataFrame]: A tuple containing two dataframes.
    """
    # Get the table
    table_key: str = "Load Combination Definitions"

    # Get the database table
    story_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName="")

    # Extract header and data
    header = story_db[2]
    data_values = story_db[4]

    # Group the data values into rows
    rows = [
        data_values[i : i + len(header)]
        for i in range(0, len(data_values), len(header))
    ]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)

    # Get unique load combinations
    df_LC = df["Name"].unique()
    df_LC = pd.DataFrame(df_LC, columns=["uniqueloadCombos"])

    # Create dataframe with all load combinations and selected load combinations column
    df_LCselection = df_LC.rename(columns={"uniqueloadCombos": "allloadCombos"})
    df_LCselection["selectedLoadCombos"] = None

    return df_LC, df_LCselection
