# -*- coding: utf-8 -*-
from typing import *
import sys


import comtypes.client
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


X = float
Y = float
POINT= Tuple[X, Y]
POLYLINE = List[POINT]
PIERSDSHAPE = Dict[str, List[POLYLINE]]
LST_PIERSDSHAPE = List[PIERSDSHAPE]

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

def get_sdshape_pierPolygon(SapModel) -> pd.DataFrame:
    

    """
    
    Return list of corresponding [X,Y] values forming each pier SD shape

    """

    # get the table
    table_key: str = "Section Designer Shapes - Concrete Polygon"

    # get the database table
    sdshapes_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName='')
    lst_tblHeader: list = sdshapes_db[2]
    lst_tblValues: list = sdshapes_db[4]
    lst_Data: list[list] = [lst_tblValues[i:i + len(lst_tblHeader)] for i in
                            range(0, len(lst_tblValues), len(lst_tblHeader))]

    # Create DataFrame of concrete polygon
    df_SD: pd.DataFrame = pd.DataFrame(lst_Data, columns=lst_tblHeader)
    df_SD['X'] = pd.to_numeric(df_SD['X'], errors='coerce')
    df_SD['X'] = np.round(df_SD['X'], 2)
    df_SD['Y'] = pd.to_numeric(df_SD['Y'], errors='coerce')
    df_SD['Y'] = np.round(df_SD['Y'], 2)
    df_SD = df_SD[['SectionName', 'ShapeName', 'X', 'Y']]
    print(df_SD)

    return df_SD

def restructure_sdshapeDF(df: pd.DataFrame) -> LST_PIERSDSHAPE:

    list_SD: LST_PIERSDSHAPE = []

    # Group the DataFrame by 'Section Name'
    for tier, group in df.groupby('SectionName'):
        shapes: List[POLYLINE] = [] 
        # Further group each tier by 'Shape Name'
        for shape, sub_group in group.groupby('ShapeName'):
            
            # Extract the coordinates for each shape
            temp_coordinates = sub_group[['X', 'Y']].values.tolist()
            
            # Convert list of lists to list of tuples
            coordinates: POLYLINE = [tuple(coord) for coord in temp_coordinates]
            
            # Ensure the polyline is closed by appending the first coordinate to the end if it's not already closed
            if coordinates[0] != coordinates[-1]:
                coordinates.append(coordinates[0])
            
            # Append the shape coordinates to the shapes list
            shapes.append(coordinates)
        
        # Append the tier and its shapes to the result list
        list_SD.append({tier: shapes})

    return list_SD

def spColumn_CTI_PierPoint(tiers: LST_PIERSDSHAPE, tier_name: str) -> str:
    """
    Formats the polylines for a specific tier.

    Args:
        tiers (LST_PIERSDSHAPE): List of dictionaries containing tier shapes data.
        tier_name (str): The name of the desired tier.

    Returns:
        str: Formatted string with the number of polylines and their coordinates for the specified tier.
    """
    list_CTI_pierpoint = []

    # Find the dictionary corresponding to the specified tier
    for tier_dict in tiers:
        if tier_name in tier_dict:
            shapes = tier_dict[tier_name]
            list_CTI_pierpoint.append(str(len(shapes)))  # Number of polylines
            for shape in shapes:
                list_CTI_pierpoint.append(str(len(shape)))  # Length of the control point list
                for point in shape:
                    list_CTI_pierpoint.append(f"{point[0]:.6f},{point[1]:.6f}")  # X,Y coordinates
            break
    
    str_CTI_pierpoint = "\n".join(list_CTI_pierpoint)

    return str_CTI_pierpoint

def plot_polylines(polylines: LST_PIERSDSHAPE) -> None:
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Use different colors for different shapes
    color_index = 0
    
    for tier_dict in polylines:
        for tier, shapes in tier_dict.items():
            plt.figure()
            for shape in shapes:
                xs, ys = zip(*shape)
                plt.plot(xs, ys, marker='o', color=colors[color_index % len(colors)])
                color_index += 1
            plt.title(f'Polylines for {tier}')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid(True)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.show()


def main():
    sap_model = connect_to_etabs(model_is_open=True)[0]
    df_sd= get_sdshape_pierPolygon(sap_model)
    lst_PierSDShape=restructure_sdshapeDF(df_sd)
    print(lst_PierSDShape)
    tier_name = 'Tier1.0'
    formatted_output = spColumn_CTI_PierPoint(lst_PierSDShape, tier_name)
    print(formatted_output)
    plot_polylines(lst_PierSDShape)
    
if __name__ == "__main__":
    main() 