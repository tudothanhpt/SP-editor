import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from utils import write_to_csv, get_new_filename
from widgets.generalInfor_dialog import Ui_d_GeneralInfor
from core.global_variables import DesignCode, BarGroupType, UnitSystem, ConfinementType, SectionCapacityMethod
from crud.general_infor_crud import create_infor, update_infor
from database.database import create_db_and_tables


class GeneralInfor_Dialog(qtw.QDialog, Ui_d_GeneralInfor):
    new_file = qtc.Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cb_DesignCode.clear()
        self.cb_DesignCode.addItems(list(str(code) for code in DesignCode))
        self.cb_UnitSystem.clear()
        self.cb_UnitSystem.addItems(list(str(us) for us in UnitSystem))
        self.cb_BarSet.clear()
        self.cb_BarSet.addItems(list(str(barset) for barset in BarGroupType))
        self.cb_Confinement.clear()
        self.cb_Confinement.addItems(list(str(cf) for cf in ConfinementType))
        self.cb_SectionCapacity.clear()
        self.cb_SectionCapacity.addItems(list(str(sc) for sc in SectionCapacityMethod))

        self.pb_Cancel.clicked.connect(self.close)
        self.pb_OK.clicked.connect(self.update_general_infor)

    @qtc.Slot()
    def update_general_infor(self):
        extensions = "SP-editor file (*.spe)"

        data_list = [self.cb_DesignCode.currentText(), self.cb_UnitSystem.currentText(), self.cb_BarSet.currentText(),
                     self.cb_Confinement.currentText(), self.cb_SectionCapacity.currentText()]
        new_file = get_new_filename(extensions)
        self.engine = create_db_and_tables(new_file)
        infor = create_infor(self.engine, data_list)
        print(infor.design_code)
        self.close()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    general_infor_dialog = GeneralInfor_Dialog()
    general_infor_dialog.show()
    sys.exit(app.exec())
