import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widgets.importEtabs_dialog import Ui_d_ImportEtabs
from utils import get_open_filename
from core.connect_etabs import connect_to_etabs, get_story_infor

from typing import Any


class ImportEtabs_Dialog(qtw.QDialog, Ui_d_ImportEtabs):
    connected_etabs = qtc.Signal(str)

    def __init__(self):
        super().__init__()
        self.EtabsObject = None
        self.SapModel = None
        self.setupUi(self)

        self.pb_Select.clicked.connect(self.attach_to_instance)
        self.pb_OpenModel.clicked.connect(self.open_etabs_file)

    def attach_etabs(self):
        try:
            model_is_open = True
            self.SapModel, self.EtabsObject = connect_to_etabs(model_is_open)
        except AttributeError:
            self.open_etabs_file()

    @qtc.Slot()
    def attach_to_instance(self):
        # TODO: Import and add attach to instance function to connect to etabs
        self.custom_signal_emit()
        qtw.QMessageBox.information(self, "Etabs Imported", "File imported successfully",
                                    qtw.QMessageBox.StandardButton.Ok)
        self.close()

    @qtc.Slot()
    def open_etabs_file(self):
        model_is_open = False
        file_name = "ETABS Model Files (*.EDB)"
        root_path = sys.path[0]
        path = ""
        try:
            path = get_open_filename(file_name, root_path)
            self.SapModel, self.EtabsObject = connect_to_etabs(model_is_open, path)
            self.custom_signal_emit()
            self.close()
        except FileNotFoundError:
            qtw.QMessageBox.warning(self, "File not found", "No such file or directory",
                                    qtw.QMessageBox.StandardButton.Ok)

    def custom_signal_emit(self):
        model_name = self.SapModel.GetModelFilename()
        self.connected_etabs.emit(model_name)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    import_dialog = ImportEtabs_Dialog()
    import_dialog.show()
    sys.exit(app.exec())
