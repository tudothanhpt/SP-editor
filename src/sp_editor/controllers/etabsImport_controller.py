from dependency_injector.wiring import inject, Provide
from PySide6 import QtWidgets as qtw

from sp_editor.containers.service_container import ServiceContainer
from sp_editor.services.etabsConnection_service import EtabsConnectionService
from sp_editor.services.etabsDataImport_service import EtabsDataImportService
from sp_editor.services.generalInfor_service import GeneralInforService
from sp_editor.widgets.importEtabs_dialog import Ui_d_ImportEtabs


class EtabsImportController(qtw.QDialog, Ui_d_ImportEtabs):
    @inject
    def __init__(
            self,
            etabsConnection_service: EtabsConnectionService = Provide[
                ServiceContainer.etabsConnection_service
            ],
            etabsDataImport_service: EtabsDataImportService = Provide[
                ServiceContainer.etabsDataImport_service
            ],
            generalInfor_service: GeneralInforService = Provide[
                ServiceContainer.generalInfor_service
            ],
    ):
        super().__init__()

        self.etabsConnection_service = etabsConnection_service
        self.etabsDataImport_service = etabsDataImport_service
        self.generalInfor_service = generalInfor_service

        self.setupUi(self)

        self.pb_Select.clicked.connect(self.confirm_attached)
        self.pb_OpenModel.clicked.connect(self.open_etabs_model)

    def attach_to_instance(self):
        """
        Attaches to an existing ETABS instance. If available using the service
        """
        try:
            success = self.etabsConnection_service.connect_to_etabs(
                attach_to_instance=True
            )
            if success:
                self.lb_ActiveModel.setText(
                    self.etabsConnection_service.sap_model.GetModelFileName(
                        IncludePath=False
                    )
                )
                qtw.QMessageBox.information(
                    self, "ETABS Connection", "Attached to an existing ETABS instance!"
                )
            else:
                qtw.QMessageBox.warning(
                    self,
                    "ETABS Connection",
                    "Could not connect to ETABS please open model instead!",
                )
                self.open_etabs_model()
        except Exception as e:
            qtw.QMessageBox.warning(self, "ETABS Connection", str(e))
        finally:
            self.close()

    def open_etabs_model(self):
        """
        Start a new instance of the ETABS model
        """
        try:
            model_path, _ = qtw.QFileDialog.getOpenFileName(
                self, "Open ETABS Model", "", "ETABS Model Files (*.edb)"
            )
            if model_path:
                success = self.etabsConnection_service.connect_to_etabs(
                    attach_to_instance=False, model_path=model_path
                )
                if success:
                    qtw.QMessageBox.information(
                        self,
                        "ETABS Connection",
                        f"Opened a new ETABS model{model_path}",
                    )
                    self.import_etabs_data()
                else:
                    qtw.QMessageBox.warning(
                        self, "ETABS Connection", "Could not open ETABS model!"
                    )
        except Exception as e:
            qtw.QMessageBox.warning(self, "ETABS Connection", str(e))
        finally:
            self.close()

    def confirm_attached(self):
        # TODO: added needed function to retrieve data from attached etabs model
        qtw.QMessageBox.warning(
            self, "ETABS Import", "All existing ETABS database will be deleted"
        )
        self.import_etabs_data()
        self.close()

    def import_etabs_data(self):
        """
        Calling the necessary service to get required information from the ETABS model
        """
        # checking the current unit in the database
        infor = self.generalInfor_service.get_generalInfor()
        unit = infor.unit_system if infor else None
        # change that current unit if needed compare to the current unit in etabs
        self.etabsDataImport_service.update_etabs_current_unit(unit)
        # story information
        self.etabsDataImport_service.import_etabs_stories_infor()
        # Pier label information
        self.etabsDataImport_service.import_etabs_pierLabel_infor()
        # Section Designer Shape information
        self.etabsDataImport_service.import_etabs_sectionDesignerShape_infor()
        # Load combos and load combos selection information
        self.etabsDataImport_service.import_etabs_loadCombos_infor()
