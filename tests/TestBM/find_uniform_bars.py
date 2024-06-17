import math
from typing import List, Tuple, Dict
from find_pier import connect_to_etabs, get_sdshape_pierPolygon, restructure_sdshapeDF, spColumn_CTI_PierPoint
from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing
import matplotlib.pyplot as plt

# Define type aliases for better readability and maintainability
X = float
Y = float
POINT = Tuple[X, Y]
POLYLINE = List[POINT]
PIERSDSHAPE = Dict[str, List[POLYLINE]]
LST_PIERSDSHAPE = List[PIERSDSHAPE]

def plot_polygons(polygons,shapes,rebar_list):
    """
    Plots a list of Shapely polygons using Matplotlib.

    :param polygons: List of Shapely Polygon objects to be plotted.
    :param fill: Boolean indicating whether to fill the polygons.
    :param alpha: Alpha value for polygon fill transparency.
    :param edge_color: Color of the polygon edges.
    :param edge_width: Width of the polygon edges.
    """
    
    plt.figure(figsize=(8, 8))
    
    for polygon in polygons:
        x, y = zip(*polygon)
        #plt.plot(x, y, color='b', linewidth=1, linestyle='--')

    for shape in shapes:
        x, y = zip(*shape)
        plt.plot(x, y, color='r', linewidth=1.5)
    
    x, y = zip(*rebar_list)
    plt.scatter(x, y, color='g',s=1)
    
    plt.title('Polygons')
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.show()

def offset_sdshapeDF(lst_PierSDShape, tier_name='Tier1.0', offset_distance=-5):
    """
    Processes the input DataFrame to extract shapes, apply an offset, and return the modified coordinates.

    :param tier_name: The name of the tier to filter shapes.
    :param offset_distance: The distance to offset the shapes.
    :param join_style: The join style for the offset.
    :return: List of coordinates for the offset shapes.
    """

    lst_offsetted_shapes = []
    area = 0
    # Iterate over the extracted shapes
    for tier_dict in lst_PierSDShape:
        if tier_name in tier_dict:
            shapes = tier_dict[tier_name]
            for shape in shapes:
                # Create a polygon and apply the offset
                polygon = Polygon(shape)
                area += (polygon.area)

                offset_polygon = polygon.buffer(offset_distance, join_style="mitre")
                offset_polygon_coords = [(round(x, 2), round(y, 2)) for x, y in offset_polygon.exterior.coords]
                lst_offsetted_shapes.append(offset_polygon_coords)

    print(area)
    
    return lst_offsetted_shapes

def extract_segments(lst_offsetted_shapes):

    """
    Input polyline to be extracted as list
    Return Values:
    list_segments (list) : List of  segments forming the polyline

    """
    segments_shapes = []
    for shape in lst_offsetted_shapes:
        num_points = len(shape)
        for i in range(num_points - 1):
            segment = [shape[i], shape[i + 1]]
            segments_shapes.append(segment)          
    return segments_shapes

def calculate_rebarpoints_for_segments(lst_offsetted_shapes, spacing):
    """
    @lst_polyline: list of offsetted polyline (with cover and half rebar diameter)
    @spacing: rebar spacing (user defined)
    Return Values:
    list_rebarsPts (list) : List of rebars' coordinates based on polyline segments and user-specified spacing
    """
    # Break polyline into segments 
    segments_shapes = extract_segments(lst_offsetted_shapes)
    
    temp_list_rebarsPts = []
    for segment in segments_shapes:
        start_point, end_point = segment
        # Calculate the control points for the current segment
        rounded_distance = math.sqrt(
            (end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2)
        num_points = math.ceil(rounded_distance / spacing)
        num_points = max(num_points, 2)
        x_diff = (end_point[0] - start_point[0]) / (num_points - 1)
        y_diff = (end_point[1] - start_point[1]) / (num_points - 1)
        control_points = [(round(start_point[0] + i * x_diff, 2), round(start_point[1] + i * y_diff, 2)) for i
                            in range(num_points)]
        # Append the calculated rebars point to the list of unique values
        temp_list_rebarsPts.append(control_points)
        
        
        # Remove duplicates from the list of rebars point
    list_rebarsPts = []

    for sublist in temp_list_rebarsPts:
        for lst_coordinates in sublist:
            list_rebarsPts.append(lst_coordinates)
    list_rebarsPts =list(set(list_rebarsPts))        
    return list_rebarsPts

def spColumn_CTI_Rebar(list_rebarsPts, rebarArea):
    """
    Converts a list of tuples into a multiline string format with a parameter added to each tuple.

    Args:
    - lst_rebarCoordiantes (list): The original list of tuples or lists of rebar coordiantes.
    - parameter: rebarArea.

    Returns:
    - str: The multiline string.
    """
    if isinstance(list_rebarsPts[0], tuple):
        modified_list = [(rebarArea,) + item for item in list_rebarsPts]
        modified_list = [(f"{area:.6f}", f"{x:.6f}", f"{y:.6f}") for (area, x, y) in modified_list]
    elif isinstance(list_rebarsPts[0], list):
        modified_list= [[rebarArea] + item for item in list_rebarsPts]
        modified_list = [(f"{area:.6f}", f"{x:.6f}", f"{y:.6f}") for [area, x, y] in modified_list]
    else:
        raise TypeError("Unsupported data format. Must be list of tuples or lists.")
    
    multiline_string_rebarPts = '\n'.join([','.join(map(str, item)) for item in modified_list])
    total_rebar = len(modified_list)
    multiline_string_rebarPts = str(total_rebar) + '\n' + multiline_string_rebarPts
    
    return multiline_string_rebarPts

def main():
    sap_model = connect_to_etabs(model_is_open=True)[0]
    df_sd= get_sdshape_pierPolygon(sap_model)
    lst_PierSDShape=restructure_sdshapeDF(df_sd)
    tier_name = 'Tier1.0'
    
    offsetted_shapes = offset_sdshapeDF(lst_PierSDShape, tier_name=tier_name, offset_distance=-5)
    formatted_output = spColumn_CTI_PierPoint(lst_PierSDShape, tier_name)
    segments_shapes=extract_segments(offsetted_shapes)
    
    rebar_list = calculate_rebarpoints_for_segments(offsetted_shapes, 24)
    multiline_string_rebarPts = spColumn_CTI_Rebar(rebar_list, 0.5)
    with open('sample.txt', 'w') as file:
        file.write(multiline_string_rebarPts)
    #print(formatted_output)
    #print(multiline_string_rebarPts)
    plot_polygons(offsetted_shapes,lst_PierSDShape[0][tier_name],rebar_list)
    
if __name__ == "__main__":
    main() 