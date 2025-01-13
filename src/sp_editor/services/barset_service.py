import json
import os

from sp_editor import GLOBALPATH
from sp_editor.core.global_variables import BarGroupType
from sp_editor.repositories.barSet_repository import BarsetRepository


class BarsetService:
    def __init__(self, barset_repository: BarsetRepository):
        self.barset_repository = barset_repository
        self.global_path = GLOBALPATH

    def barset_list(self, barset: str):
        """
        Return the path to the JSON file for the given barset group type.
        """
        barset_mapping = {
            str(BarGroupType.ASTM615): os.path.join(
                self.global_path, "Property Libraries", "Barsets", "tb_ASTM_A615.json"
            ),
            str(BarGroupType.ASTM615M): os.path.join(
                self.global_path, "Property Libraries", "Barsets", "tb_ASTM_A615M.json"
            ),
            str(BarGroupType.PR_EN_10080): os.path.join(
                self.global_path, "Property Libraries", "Barsets", "tb_PrEN_10080.json"
            ),
            str(BarGroupType.CSA_G30_18): os.path.join(
                self.global_path, "Property Libraries", "Barsets", "tb_CSA_G30_18.json"
            ),
        }
        return barset_mapping.get(barset)

    def load_barsets_from_file(self, barset: str):
        """
        Loads barsets from the JSON file associated with the given barset group type
        and writes them to the database.
        """
        json_path = self.barset_list(barset)
        if not json_path:
            raise ValueError(f"Invalid barset type: {barset}")

        with open(json_path, "r") as f:
            barsets_data = json.load(f)

        # Pass the parsed data to the repository for import
        self.barset_repository.import_barsets(barsets_data)

    def get_all_barset(self):
        """
        Get all lists of rebar and transform to a dataframe model
        :return: dataframe type to be display under a table view model
        """
        barset_df = self.barset_repository.get_all()

        # Filter and order the columns based on the BarSet model
        columns_to_include = ["size", "diameter", "area", "weight"]
        filtered_df = barset_df[columns_to_include]

        return filtered_df
