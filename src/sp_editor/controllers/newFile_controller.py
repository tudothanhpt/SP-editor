from dependency_injector.wiring import inject, Provide
from PySide6 import QtWidgets as qtw

from sp_editor.services.barset_service import BarsetService
from sp_editor.widgets.generalInfor_dialog import Ui_d_GeneralInfor
from sp_editor.core.global_variables import (
    DesignCode,
    BarGroupType,
    UnitSystem,
    ConfinementType,
    SectionCapacityMethod,
)
from sp_editor.services.file_service import FileService
from sp_editor.services.generalInfor_service import GeneralInforService
from sp_editor.containers.service_container import ServiceContainer


class NewFileController(qtw.QDialog, Ui_d_GeneralInfor):
    @inject
    def __init__(
            self,
            file_service: FileService = Provide[ServiceContainer.file_service],
            generalInfor_service: GeneralInforService = Provide[
                ServiceContainer.generalInfor_service
            ],
            barset_service: BarsetService = Provide[ServiceContainer.barset_service],
    ):
        super().__init__()

        # using 2 services in new file controller
        self.file_service = file_service
        self.generalInfor_service = generalInfor_service
        self.barset_service = barset_service

        self.setupUi(self)

        self.cb_DesignCode.clear()
        self.cb_DesignCode.addItems(list(str(code) for code in DesignCode))
        self.cb_DesignCode.setCurrentIndex(DesignCode.ACI_318_14.value)

        self.cb_UnitSystem.clear()
        self.cb_UnitSystem.addItems(list(str(us) for us in UnitSystem))
        self.cb_UnitSystem.setCurrentIndex(UnitSystem.ENGLISH.value)

        self.cb_BarSet.clear()
        self.cb_BarSet.addItems(list(str(barset) for barset in BarGroupType))
        self.cb_BarSet.setCurrentIndex(BarGroupType.ASTM615.value)

        self.cb_Confinement.clear()
        self.cb_Confinement.addItems(list(str(cf) for cf in ConfinementType))
        self.cb_Confinement.setCurrentIndex(ConfinementType.TIED.value)

        self.cb_SectionCapacity.clear()
        self.cb_SectionCapacity.addItems(list(str(sc) for sc in SectionCapacityMethod))
        self.cb_SectionCapacity.setCurrentIndex(
            SectionCapacityMethod.CRITICAL_CAPACITY.value
        )

        # connect function execute with OK button
        self.pb_Cancel.clicked.connect(self.close)
        self.pb_OK.clicked.connect(self.execute)

    def execute(self):
        file_path, _ = qtw.QFileDialog.getSaveFileName(
            self, "Create File", "", "sp_editor file (*.spe)"
        )
        if file_path:
            if self.file_service.new_database(file_path):  # Create also opens
                # adding along service when new file
                self._generalInfor_init(file_path)
                self._barsets_init()
                self.close()
                qtw.QMessageBox.information(
                    self, "Success", f"Database created at: {file_path}"
                )
            else:
                qtw.QMessageBox.critical(self, "Error", "Failed to create database.")

    def _generalInfor_init(self, file_path):
        """Init general infor in a database"""
        data_list = [
            self.cb_DesignCode.currentText(),
            self.cb_UnitSystem.currentText(),
            self.cb_BarSet.currentText(),
            self.cb_Confinement.currentText(),
            self.cb_SectionCapacity.currentText(),
        ]
        infor = self.generalInfor_service.add_generalInfor(data_list, file_path)

    def _barsets_init(self):
        """Init barsets in database"""
        barset_str = self.cb_BarSet.currentText()
        barset = self.barset_service.load_barsets_from_file(barset_str)
