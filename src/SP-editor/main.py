import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widgets.main_window import Ui_mw_Main
from import_etabs_dialog import ImportEtabs_Dialog


class MainWindow(qtw.QMainWindow, Ui_mw_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Setup action
        self.a_ImportEtabs.triggered.connect(self.open_import_etabs)
        self

    @qtc.Slot()
    def open_import_etabs(self):
        self.dialog = ImportEtabs_Dialog()
        self.dialog.exec()
        self.dialog.connected_etabs.connect(self.a_ImportEtabs.setEnabled(False))


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
