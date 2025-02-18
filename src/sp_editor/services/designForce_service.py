from dependency_injector.wiring import inject, Provide
import pandas as pd

from sp_editor.core.connect_etabs import get_pier_force_infor
from sp_editor.repositories.etabsLoadCombos_repository import EtabsLoadCombosRepository
from sp_editor.services import loadCombos_service
from sp_editor.services.etabsConnection_service import EtabsConnectionService
from sp_editor.services.loadCombos_service import LoadCombosService


class DesignForceService:
    @inject
    def __init__(
            self,
            etabsConnection_service: EtabsConnectionService = Provide[
                "ServiceContainer.etabsConnectionService"
            ],
            loadCombos_repository: EtabsLoadCombosRepository = Provide[
                "ServiceContainer.etabsLoadCombosRepository"
            ]

    ):
        self.etabsConnection_service = etabsConnection_service
        self.loadCombos_repository = loadCombos_repository

    def get_selected_combos(self) -> pd.DataFrame:
        """
        Get all selected load combos.
        :return:
        """
        return self.loadCombos_repository.get_all_load_combo_selections()

    def import_etabs_pier_design_force(self, selectedCombos: list[str]):
        #TODO: We might need to import only active pier design force here not all of them
        """
        Import ETABS pier design force
        :param selectedCombos:
        """
        # Retrieve ETABS API objects
        sap_model = self.etabsConnection_service.sap_model

        etabs_object = self.etabsConnection_service.etabs_object

        # Call helper function to get pier design force information from ETABS
        pier_design_force = get_pier_force_infor(sap_model, etabs_object, selectedCombos)

        # Store the pier design force into the database
        self.
