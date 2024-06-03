import pandas as pd
from typing import Any, List, Tuple, Union
import comtypes.client
from comtypes import COMError
import read_excel
import time
import math

def get_active_ACADdocument():
    try:
        time.sleep(2) #Voodoo line of BM's magic
        acad = comtypes.client.GetActiveObject("AutoCAD.Application")
        return acad.ActiveDocument
    except Exception as e:
        print("Error:", e)
        return None


def is_file_open(acad, file_path):
    # Get the open documents
    documents = acad.Documents

    # Iterate through the open documents
    for doc in documents:
        # Compare the paths
        if doc.FullName.lower() == file_path.lower():
            return True  # File is already open
    return False  # File is not open

def open_autocad_file(file_path: str) -> Union[object, None]:
    """
    Open an AutoCAD file.

    Args:
    - file_path (str): The path to the AutoCAD file.

    Returns:
    - acaddoc (object or None): The active AutoCAD document object if successful, otherwise None.
    """
    try:
    # Try to get a running instance of AutoCAD
        acad = comtypes.client.GetActiveObject("AutoCAD.Application")
    except:
        acad = comtypes.client.CreateObject("AutoCAD.Application", dynamic=True)
    
    # Create an instance of the AutoCAD application
    acad.visible = True
    # Check if the file is already open
    if is_file_open(acad, file_path):
        acaddoc = get_active_ACADdocument()
    else:
        # Open the specified drawing file
        acad.Documents.Open(file_path)
        acaddoc = get_active_ACADdocument()
    return acaddoc

def getVerticesList_fromCAD(acaddoc: Any) -> List[List[Tuple[float, float]]]:
    """
    Extracts the vertices list from CAD entities.

    Args:
        acaddoc (Any): The CAD document..

    Returns:
        List[List[Tuple[float, float]]]: A list of vertices for each polyline found.
    """
    ACADLAYER_POLYLINE = "PL"
    ACADOBJECTNAME_POLYLINE="AcDbPolyline"
    
    while acaddoc is None:
        acaddoc = get_active_ACADdocument()
    print("READING: "+acaddoc.Name)
    modelspace = acaddoc.ModelSpace  # Model space of the CAD document
    vertices = []  # List to store vertices for each polyline
    num_polyline = 0  # Counter for the number of polylines found

    # Iterate through entities in the model space
    for entity in modelspace:
        # Check if the entity is a polyline and belongs to the specified layer
        if entity.objectname == ACADOBJECTNAME_POLYLINE and entity.layer == ACADLAYER_POLYLINE:
            # Extract coordinates of the polyline
            a = list(entity.coordinates)
            # Group coordinates into pairs to represent vertices
            pairs = [(a[i],a[i + 1]) for i in range(0, len(a), 2)]
            vertices.append(pairs)  # Append the vertices to the list
            num_polyline += 1  # Increment the counter for each polyline found

    # If only one polyline is found, return its vertices directly
    acaddoc.close()
    return vertices

def format_vertices_for_spcolumn(coordinates: List[List[Tuple[float, float]]]) -> str:
    """
    Convert CAD coordinates to SPcol format.

    Args:
    - coordinates (list): List of coordinate tuples for multiple polylines.

    Returns:
    - formatted_output (str): SPcol formatted string.
    """
    formatted_output: List[str] = []

    # Get the total number of sublists (polylines)
    total_sublists: int = len(coordinates)
    formatted_output.append(str(total_sublists))

    # Iterate over each sublist (polyline)
    for sublist in coordinates:
        # Get the total number of points in the sublist
        total_points_sublist: int = len(sublist)
        # Append the total number of points in the sublist
        formatted_output.append(str(total_points_sublist))
        # Format and append the coordinates for each point in the sublist
        for point in sublist:
            formatted_output.append(f"{point[0]},{point[1]}")

    # Join the formatted output with newline characters
    formatted_output_str: str = "\n".join(formatted_output)

    return formatted_output_str

def get_rebarinfo_fromCAD(acaddoc) -> List[Tuple[float, float, float]]:
    """
    Extract rebar information from an AutoCAD DXF file.
    
    This function opens an AutoCAD DXF file, iterates through the entities
    in the model space, and collects information about circles. It returns
    a list of tuples, each containing the area, center X coordinate, and
    center Y coordinate of a circle.
    
    Args:
        file_path (str): The path to the AutoCAD DXF file.
        
    Returns:
        List[Tuple[float, float, float]]: A list of tuples containing the area, 
                                           center X, and center Y coordinates of each circle.
    """
    ACADLAYER_CIRCLE = "Rebar"
    ACADOBJECTNAME_CIRCLE="AcDbCircle"
    
    # while acaddoc is None:
    #     acaddoc = get_active_ACADdocument()
            
    modelspace = acaddoc.ModelSpace
    list_rebarinfo: List[Tuple[float, float, float]] = []
    
    for entity in modelspace:
        if entity.ObjectName == ACADOBJECTNAME_CIRCLE and entity.layer == ACADLAYER_CIRCLE:
            center_coor: Tuple[float, float, float] = entity.Center
            center_x = round(center_coor[0], 2)
            center_y = round(center_coor[1], 2)
            radius = entity.Radius
            area = round(math.pi * (radius ** 2), 2)
            temp_rebarinfo = (area, center_x, center_y)
            list_rebarinfo.append(temp_rebarinfo)
    acaddoc.close()
    return list_rebarinfo  
    
def format_rebar_info_for_spcolumn(list_rebarinfo: List[Tuple[float, float, float]]) -> str:
    """
    Format the rebar information for an SPColumn CTI file.

    This function takes a list of tuples containing rebar information
    (area, center X, center Y) and formats it into a string suitable for
    an SPColumn CTI file. The first line of the string contains the number
    of rebar entries. Each subsequent line contains the area, center X,
    and center Y of a rebar, separated by commas.

    Args:
        list_rebarinfo (List[Tuple[float, float, float]]): A list of tuples containing
                                                          the area, center X, and center Y
                                                          coordinates of each rebar.

    Returns:
        str: A formatted string containing the rebar information for an SPColumn CTI file.
    """
    if list_rebarinfo is None:
        formatted_output_str=0
    else:   
        formatted_output_str: str = str(len(list_rebarinfo))
        
        for rebar_info in list_rebarinfo:
            each_rebar_str: str = ",".join(str(coordinate) for coordinate in rebar_info)
            formatted_output_str += "\n" + each_rebar_str
    
    return formatted_output_str

def main():
    return True
    
if __name__ == "__main__": 
    main()