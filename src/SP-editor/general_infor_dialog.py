import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from utils import  write_to_csv
from widgets.generalInfor_dialog import Ui_d_GeneralInfor
from core.global_variables import DesignCode, BarGroupType,UnitSystem,ConfinementType,SectionCapacityMethod


class GeneralInfor_Dialog(qtw.QDialog, Ui_d_GeneralInfor):
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
        datalist = [self.cb_DesignCode.currentText(),self.cb_UnitSystem.currentText(),self.cb_BarSet.currentText(),self.cb_Confinement.currentText(),self.cb_SectionCapacity.currentText()]
        write_to_csv(datalist,"user_data.csv")
        qtw.QMessageBox.information(self, "Information", "User information written successfully, please find the CSV file",)
        self.close()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    general_infor_dialog = GeneralInfor_Dialog()
    general_infor_dialog.show()
    sys.exit(app.exec())
