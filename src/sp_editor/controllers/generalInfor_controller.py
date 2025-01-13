from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from dependency_injector.wiring import inject, Provide

from sp_editor.containers.service_container import ServiceContainer
from sp_editor.services.generalInfor_service import GeneralInforService
from sp_editor.widgets.generalInfor_dialog import Ui_d_GeneralInfor

from sp_editor.core.global_variables import (
    DesignCode,
    BarGroupType,
    UnitSystem,
    ConfinementType,
    SectionCapacityMethod,
)


class GeneralInforController(qtw.QDialog, Ui_d_GeneralInfor):
    infor_updated = qtc.Signal(str)

    @inject
    def __init__(
        self,
        generalInfor_service: GeneralInforService = Provide[
            ServiceContainer.generalInfor_service
        ],
    ):
        self.generalInfor_service = generalInfor_service
        super().__init__()
        # setup UI from widget
        self.setupUi(self)
        self.infor = None

    def update_general_infor(self):
        data_list = [
            self.cb_DesignCode.currentText(),
            self.cb_UnitSystem.currentText(),
            self.cb_BarSet.currentText(),
            self.cb_Confinement.currentText(),
            self.cb_SectionCapacity.currentText(),
        ]
        self.infor = self.generalInfor_service.update_generalInfor(data_list)
        self.infor_updated.emit("General information updated")
        self.close()

    def get_general_infor_and_display(self):
        # getting current general infor in database
        self.infor = self.generalInfor_service.get_generalInfor()

        self.cb_DesignCode.clear()
        self.cb_DesignCode.addItems(list(str(code) for code in DesignCode))
        self.cb_DesignCode.setCurrentText(self.infor.design_code)

        self.cb_UnitSystem.clear()
        self.cb_UnitSystem.addItems(list(str(us) for us in UnitSystem))
        self.cb_UnitSystem.setCurrentText(self.infor.unit_system)

        self.cb_BarSet.clear()
        self.cb_BarSet.addItems(list(str(barset) for barset in BarGroupType))
        self.cb_BarSet.setCurrentText(self.infor.bar_set)

        self.cb_Confinement.clear()
        self.cb_Confinement.addItems(list(str(cf) for cf in ConfinementType))
        self.cb_Confinement.setCurrentText(self.infor.confinement)

        self.cb_SectionCapacity.clear()
        self.cb_SectionCapacity.addItems(list(str(sc) for sc in SectionCapacityMethod))
        self.cb_SectionCapacity.setCurrentText(self.infor.section_capacity)

        self.pb_Cancel.clicked.connect(self.close)
        self.pb_OK.clicked.connect(self.update_general_infor)
