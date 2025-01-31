import math

from sp_editor.repositories.etabsSectionDesignerShape_repository import EtabsSectionDesignerShapeRepository
from typing import Tuple, List, Dict
from shapely.geometry import Polygon
from sp_editor.core.find_pier import restructure_sdshapeDF


class RebarService:
    def __init__(
            self,
            etabsSectionDesignerShape_repository: EtabsSectionDesignerShapeRepository, ):
        self.etabsSectionDesignerShape_repository = etabsSectionDesignerShape_repository

    def calculate_rebar_coordinates(
            self, cover: float, bar_area: float, spacing: float, sd_name: str
    ) -> Tuple[int, str]:
        """
        Computes rebar coordinates based on input parameters.

        :return: (Total rebar count, multiline string of rebar coordinates)
        """
        bar_dia = math.sqrt(bar_area / math.pi) * 2
        offset_distance = (cover + (bar_dia / 2)) * (-1)

        # Read and process SDS database
        df_sd = self.etabsSectionDesignerShape_repository.read_sds_db()
        lst_PierSDShape = restructure_sdshapeDF(df_sd)

        idx = find_key_index(lst_PierSDShape, sd_name)
        PierSDShape = lst_PierSDShape[idx]

        offsetted_shapes = self.offset_sdshapeDF(lst_PierSDShape, sd_name, offset_distance)
        rebar_list = self.calculate_rebarpoints_for_segments(offsetted_shapes, spacing)

        total_rebar, multiline_string_rebarPts = self.spColumn_CTI_Rebar(rebar_list, bar_area)
        return total_rebar, multiline_string_rebarPts

    def offset_sdshapeDF(self, list_PierSDShape, PierSDName, offset_distance):
        lst_offsetted_shapes = []
        for tier_dict in list_PierSDShape:
            if PierSDName in tier_dict:
                shapes = tier_dict[PierSDName]
                for shape in shapes:
                    polygon = Polygon(shape)
                    offset_polygon = polygon.buffer(offset_distance, join_style="mitre")
                    offset_polygon_coords = [(round(x, 2), round(y, 2)) for x, y in offset_polygon.exterior.coords]
                    lst_offsetted_shapes.append(offset_polygon_coords)
        return lst_offsetted_shapes

    def calculate_rebarpoints_for_segments(self, lst_offsetted_shapes, spacing):
        segments_shapes = []
        for shape in lst_offsetted_shapes:
            for i in range(len(shape) - 1):
                segments_shapes.append([shape[i], shape[i + 1]])

        list_rebarsPts = []
        for segment in segments_shapes:
            start_point, end_point = segment
            dist = math.sqrt((end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2)
            num_points = max(math.ceil(dist / spacing), 2)
            x_diff, y_diff = (end_point[0] - start_point[0]) / (num_points - 1), (end_point[1] - start_point[1]) / (
                    num_points - 1)
            control_points = [(round(start_point[0] + i * x_diff, 2), round(start_point[1] + i * y_diff, 2)) for i in
                              range(num_points)]
            list_rebarsPts.extend(control_points)

        return list(set(list_rebarsPts))

    def spColumn_CTI_Rebar(self, list_rebarsPts, rebarArea):
        modified_list = [(rebarArea, x, y) for x, y in list_rebarsPts]
        modified_list = [(f"{area:.6f}", f"{x:.6f}", f"{y:.6f}") for (area, x, y) in modified_list]
        multiline_string_rebarPts = "\n".join([",".join(map(str, item)) for item in modified_list])
        return len(modified_list), f"{len(modified_list)}\n{multiline_string_rebarPts}"


def find_key_index(data_list, key_to_find):
    for idx, data_dict in enumerate(data_list):
        if key_to_find in data_dict:
            return idx
    return None
