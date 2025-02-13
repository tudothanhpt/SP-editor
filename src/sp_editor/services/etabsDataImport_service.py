from dependency_injector.wiring import inject, Provide

from sp_editor.core.connect_etabs import (
    get_story_infor,
    get_pier_label_infor,
    get_section_designer_shape_infor,
    get_loadCombo_df_fromE,
)
from sp_editor.repositories.etabsLoadCombos_repository import EtabsLoadCombosRepository
from sp_editor.repositories.etabsPierLabel_repository import EtabsPierLabelRepository
from sp_editor.repositories.etabsSectionDesignerShape_repository import (
    EtabsSectionDesignerShapeRepository,
)
from sp_editor.repositories.etabsStory_repository import EtabsStoryRepository
from sp_editor.services.etabsConnection_service import EtabsConnectionService


class EtabsDataImportService:
    @inject
    def __init__(
            self,
            etabsConnection_service: EtabsConnectionService = Provide[
                "ServiceContainer.etabsConnectionService"
            ],
            etabsStory_repository: EtabsStoryRepository = Provide[
                "ServiceContainer.etabsStoryRepository"
            ],
            etabsPierLabel_repository: EtabsPierLabelRepository = Provide[
                "ServiceContainer.etabsPierLabelRepository"
            ],
            etabsSectionDesignerShape_repository: EtabsSectionDesignerShapeRepository = Provide[
                "ServiceContainer.etabsSectionDesignerShapeRepository"
            ],
            etabsLoadCombos_repository: EtabsLoadCombosRepository = Provide[
                "ServiceContainer.etabsLoadCombosRepository"
            ],
    ):
        self.etabsConnection_service = etabsConnection_service
        self.etabsStory_repository = etabsStory_repository
        self.etabsPierLabel_repository = etabsPierLabel_repository
        self.etabsSectionDesignerShape_repository = etabsSectionDesignerShape_repository
        self.etabsLoadCombos_repository = etabsLoadCombos_repository

    def update_etabs_current_unit(self, cti_unit: str):
        # Retrieve ETABS API objects
        sap_model = self.etabsConnection_service.sap_model

        # Set up the unit inside etabs model
        if cti_unit == "English Unit":
            sap_model.SetPresentUnits(1)
        elif cti_unit == "Metric Units":
            sap_model.SetPresentUnits(5)

    def import_etabs_stories_infor(self):
        """
        Import ETABS stories information using the ETABS API and store it in the database.

        The `sap_model` and `etabs_object` are retrieved from `EtabsConnectionService`.
        """
        # Retrieve ETABS API objects
        sap_model = self.etabsConnection_service.sap_model

        etabs_object = self.etabsConnection_service.etabs_object

        # Call helper function to get story information from ETABS
        stories_df = get_story_infor(sap_model, etabs_object)

        # Store the stories information in the database
        self.etabsStory_repository.import_stories(stories_df)

    def import_etabs_pierLabel_infor(self):
        """
        Import ETABS pierLabel information using the ETABS API and store it in the database.
        """
        # Retrieve ETABS API objects
        sap_model = self.etabsConnection_service.sap_model

        etabs_object = self.etabsConnection_service.etabs_object

        # Call helper function to get pier label information from ETABS
        pierLabel_df = get_pier_label_infor(sap_model, etabs_object)

        # Store pier label into database
        self.etabsPierLabel_repository.import_pier_labels(pierLabel_df)

    def import_etabs_sectionDesignerShape_infor(self):
        """
        Import ETABS sectionDesignerShape information using the ETABS API and store it in the database.
        then convert this table to CTI file format
        """
        # Retrieve ETABS API objects
        sap_model = self.etabsConnection_service.sap_model

        etabs_object = self.etabsConnection_service.etabs_object

        # Call helper function to get section designer shape table information from ETABS
        section_designer_shape_df = get_section_designer_shape_infor(
            sap_model, etabs_object
        )

        # Store the Section designer shape information in the database
        self.etabsSectionDesignerShape_repository.import_section_designer_shapes(
            section_designer_shape_df
        )

        # Convert table section designer shape to CTI format in table sds_coordinates_cti
        self.etabsSectionDesignerShape_repository.get_SDCoordinates_CTI_todb()

    def import_etabs_loadCombos_infor(self):
        """
        Get total load combos from etabs and then create a load combos selection and load combos in database.
        """
        # Retrieve ETABS API objects
        sap_model = self.etabsConnection_service.sap_model

        # Call helper function to get section designer shape table information from ETABS
        df_LC, df_LCselection = get_loadCombo_df_fromE(sap_model)

        # calling repository function to add LC and LCselection to database
        self.etabsLoadCombos_repository.create_load_combos(df_LC)
        self.etabsLoadCombos_repository.create_load_combo_selections(df_LCselection)
