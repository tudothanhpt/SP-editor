# -*- coding: utf-8 -*-
from typing import *

import pandas as pd
from shapely.geometry import Polygon

X = float
Y = float
POINT = Tuple[X, Y]
POLYLINE = List[POINT]
PIERSDSHAPE = Dict[str, List[POLYLINE]]
LST_PIERSDSHAPE = List[PIERSDSHAPE]


def find_key_index(data_list, key_to_find):
    index = None
    for idx, data_dict in enumerate(data_list):
        if key_to_find in data_dict:
            index = idx
            break
    return index


def restructure_sdshapeDF(df: pd.DataFrame) -> LST_PIERSDSHAPE:
    list_SD: LST_PIERSDSHAPE = []

    # Group the DataFrame by 'Section Name'
    for tier, group in df.groupby("sectionName"):
        shapes: List[POLYLINE] = []
        # Further group each tier by 'Shape Name'
        for shape, sub_group in group.groupby("shapeName"):
            # Extract the coordinates for each shape
            temp_coordinates = sub_group[["x", "y"]].values.tolist()

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


def spColumn_CTI_PierPoint(list_PierSDShape: LST_PIERSDSHAPE, PierSDName: str) -> str:
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
    for PierSDShape_dict in list_PierSDShape:
        if PierSDName in PierSDShape_dict:
            shapes = PierSDShape_dict[PierSDName]
            list_CTI_pierpoint.append(str(len(shapes)))  # Number of polylines
            for shape in shapes:
                list_CTI_pierpoint.append(
                    str(len(shape))
                )  # Length of the control point list
                for point in shape:
                    list_CTI_pierpoint.append(
                        f"{point[0]:.6f},{point[1]:.6f}"
                    )  # X,Y coordinates
            break

    str_CTI_pierpoint = "\n".join(list_CTI_pierpoint)

    return str_CTI_pierpoint


def shape_area(list_PierSDShape: LST_PIERSDSHAPE, PierSDName: str) -> str:
    area = 0

    for PierSDShape_dict in list_PierSDShape:
        if PierSDName in PierSDShape_dict:
            shapes = PierSDShape_dict[PierSDName]
            for shape in shapes:
                polygon = Polygon(shape)
                area += polygon.area

    return area


if __name__ == "__main__":
    main()
