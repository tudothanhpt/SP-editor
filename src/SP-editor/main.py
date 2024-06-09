import sys
from typing import Any

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widgets.main_window import Ui_mw_Main
from import_etabs_dialog import ImportEtabs_Dialog
from general_infor_dialog import GeneralInfor_Dialog
from open_file_dialog import OpenFile_Dialog
from new_file_dialog import NewFile_Dialog
from barest_dialog import BarSet_Dialog

from utils import select_csv_file, get_open_filename

from sqlalchemy.engine.base import Engine
from database.database import create_db_and_tables, connect_db_and_tables
from crud.cr_general_infor import get_infor


class MainWindow(qtw.QMainWindow, Ui_mw_Main):
    def __init__(self):
        super().__init__()
        self.current_path = None
        self.dialog_barset = None
        self.dialog_import_etabs = None
        self.dialog_open = None
        self.dialog_new = None
        self.current_engine = None
        self.sap_model = None
        self.etabs_object = None

        self.setupUi(self)
        self.set_active_action(False)

        # Setup action
        self.action_New.triggered.connect(self.new_file)
        self.action_Open.triggered.connect(self.open_file)
        self.a_ImportEtabs.triggered.connect(self.open_import_etabs)
        self.a_GeneralInfor.triggered.connect(self.set_general_infor)
        self.a_BarSet.triggered.connect(self.open_barset)

        # The `@qtc.Slot()` decorator in this code snippet is used to define a slot method in a

    # PyQt/PySide class. In PyQt/PySide, slots are used to handle signals emitted by widgets or other
    # objects. By decorating a method with `@qtc.Slot()`, you are explicitly marking that method as a
    # slot that can be connected to signals.
    # @qtc.Slot()
    @qtc.Slot()
    def new_file(self):
        self.dialog_new = NewFile_Dialog(self)
        self.dialog_new.path_new.connect(self.update_message)
        self.dialog_new.path_new.connect(self.set_current_path)
        self.dialog_new.engine_new.connect(self.set_current_engine)
        self.set_active_action(True)
        self.dialog_new.exec()

    @qtc.Slot()
    def open_file(self):
        self.dialog_open = OpenFile_Dialog(self)
        self.dialog_open.path_open.connect(self.update_message)
        self.dialog_open.path_open.connect(self.set_current_path)
        self.dialog_open.engine_open.connect(self.set_current_engine)
        self.set_active_action(True)
        self.dialog_open.open_file()

    @qtc.Slot()
    def open_import_etabs(self):
        self.dialog_import_etabs = ImportEtabs_Dialog()
        self.dialog_import_etabs.attach_etabs()
        self.dialog_import_etabs.lb_ActiveModel.setText(
            self.dialog_import_etabs.SapModel.GetModelFilename()
        )
        self.dialog_import_etabs.exec()

        self.sap_model = self.dialog_import_etabs.SapModel
        self.etabs_object = self.dialog_import_etabs.EtabsObject

        self.dialog_import_etabs.connected_etabs.connect(self.update_message)
        self.dialog_import_etabs.connected_etabs.connect(
            self.a_ImportEtabs.setEnabled(False)
        )

    @qtc.Slot()
    def open_barset(self):
        self.dialog_barset = BarSet_Dialog(self.current_engine, self.current_path)
        self.dialog_barset.exec()

    @qtc.Slot()
    def set_general_infor(self):
        self.dialog_new = GeneralInfor_Dialog(self.current_engine)
        self.dialog_new.infor_updated.connect(self.update_message)
        self.dialog_new.exec()

    @qtc.Slot(Engine)
    def set_current_engine(self, engine: Engine):
        self.current_engine = engine

    @qtc.Slot(str)
    def set_current_path(self, path: str):
        self.current_path = path

    @qtc.Slot(str)
    def update_message(self, message: str):
        self.statusbar.showMessage(message)

    @qtc.Slot()
    def set_active_action(self, mode: bool):
        self.a_ImportEtabs.setEnabled(mode)
        self.a_GeneralInfor.setEnabled(mode)
        self.a_MaterialProp.setEnabled(mode)
        self.a_BarSet.setEnabled(mode)
        self.a_Groups.setEnabled(mode)
        self.a_Cases.setEnabled(mode)
        self.a_GetAllForce.setEnabled(mode)
        self.a_MakeSPcolumn.setEnabled(mode)
        self.a_BatchProcessor.setEnabled(mode)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
