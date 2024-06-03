import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widgets.main_window import Ui_mw_Main
from import_etabs_dialog import ImportEtabs_Dialog
from general_infor_dialog import GeneralInfor_Dialog
from utils import select_csv_file

from database.database import create_db_and_tables


class MainWindow(qtw.QMainWindow, Ui_mw_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Setup action
        self.a_ImportEtabs.triggered.connect(self.open_import_etabs)
        self.action_New.triggered.connect(self.set_general_infor)
        self.action_Open.triggered.connect(self.get_general_infor)

        # The `@qtc.Slot()` decorator in this code snippet is used to define a slot method in a

    # PyQt/PySide class. In PyQt/PySide, slots are used to handle signals emitted by widgets or other
    # objects. By decorating a method with `@qtc.Slot()`, you are explicitly marking that method as a
    # slot that can be connected to signals.
    # @qtc.Slot()
    def open_import_etabs(self):
        self.dialog = ImportEtabs_Dialog()
        self.dialog.exec()
        self.dialog.connected_etabs.connect(self.a_ImportEtabs.setEnabled(False))

    @qtc.Slot()
    def set_general_infor(self):
        self.dialog_new = GeneralInfor_Dialog()
        self.dialog_new.exec()

    @qtc.Slot()
    def get_general_infor(self):
        pass
        # self.dialog_open = qtw.QFileDialog()
        # self.dialog.setNameFilter("CSV files (*.csv)")
        # self.dialog.setViewMode(qtw.QFileDialog.List)
        # self.dialog.setFileMode(qtw.QFileDialog.ExistingFile)
        # if self.dialog.exec():
        #     file_paths = self.dialog.selectedFiles()
        #     if file_paths:
        #         csv_file_path = file_paths[0]
        #         print(csv_file_path)
        #         return csv_file_path


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
