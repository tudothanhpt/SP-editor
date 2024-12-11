import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw


from sp_editor.widgets.generalInfor_dialog import Ui_d_GeneralInfor

from sqlalchemy.engine.base import Engine
from sp_editor.core.global_variables import (
    DesignCode,
    BarGroupType,
    UnitSystem,
    ConfinementType,
    SectionCapacityMethod,
)
from sp_editor.crud.cr_general_infor import update_infor, get_infor


class GeneralInfor_Dialog(qtw.QDialog, Ui_d_GeneralInfor):
    infor_updated = qtc.Signal(str)

    def __init__(self, engine: Engine | None = None):
        super().__init__()
        self.engine = engine
        self.infor = get_infor(self.engine)

        self.setupUi(self)

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

    @qtc.Slot()
    def update_general_infor(self):
        data_list = [
            self.cb_DesignCode.currentText(),
            self.cb_UnitSystem.currentText(),
            self.cb_BarSet.currentText(),
            self.cb_Confinement.currentText(),
            self.cb_SectionCapacity.currentText(),
        ]
        self.infor = update_infor(self.engine, data_list)
        self.infor_updated.emit("General information updated")
        self.close()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    general_infor_dialog = GeneralInfor_Dialog()
    general_infor_dialog.show()
    sys.exit(app.exec())
