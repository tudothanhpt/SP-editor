import pandas as pd
from typing import Tuple, List

from sp_editor.models.models import LoadCombinationsSelection
from sp_editor.repositories.etabsLoadCombos_repository import EtabsLoadCombosRepository


class LoadCombosService:
    def __init__(self,
                 etabsLoadCombos_repository: EtabsLoadCombosRepository):

        self.etabsLoadCombos_repository = etabsLoadCombos_repository

    def get_load_combo_lists(self) -> Tuple[List[str], List[str]]:
        """
        Retrieves unique load combinations and selected load combinations as two separate lists.

        :return: Tuple of (unique_combos, selected_combos)
        """
        # Assume the repository functions now return lists of dictionaries
        unique_data = self.etabsLoadCombos_repository.get_all_load_combos()  # List[dict]
        selection_data = self.etabsLoadCombos_repository.get_all_load_combo_selections()  # List[dict]

        # Extract the "uniqueloadCombos" values, filtering out None values
        unique_combos = unique_data["uniqueloadCombos"].dropna().tolist()
        selected_combos = selection_data["selectedLoadCombos"].dropna().tolist()

        return unique_combos, selected_combos

    def update_load_combo_selections(self, unique_combos: List[str], selected_combos: List[str]) -> None:
        """
        Updates the load combination selection data and writes it to the database.

        :param unique_combos: List of unique load combination names.
        :param selected_combos: List of selected load combination names.
        """
        data = []
        max_length = max(len(unique_combos), len(selected_combos))
        for i in range(max_length):
            orig = unique_combos[i] if i < len(unique_combos) else None
            selected = selected_combos[i] if i < len(selected_combos) else None
            data.append({
                "allloadCombos": orig,
                "selectedLoadCombos": selected
            })

        # Now, call the repository function with the list of dictionaries
        self.etabsLoadCombos_repository.update_combo_selections(data)
