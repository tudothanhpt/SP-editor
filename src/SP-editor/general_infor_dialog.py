import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widgets.generalInfor_dialog import Ui_d_GeneralInfor


class GeneralInfor_Dialog(qtw.QDialog, Ui_d_GeneralInfor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pb_Cancel.clicked.connect(self.close)
        self.pb_OK.clicked.connect(self.update_general_infor)

    @qtc.Slot()
    def update_general_infor(self):
        pass


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    general_infor_dialog = GeneralInfor_Dialog()
    general_infor_dialog.show()
    sys.exit(app.exec())
