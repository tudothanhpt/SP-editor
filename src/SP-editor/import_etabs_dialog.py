import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widgets.importEtabs_dialog import Ui_d_ImportEtabs
from utils import get_open_filename, AttachToInstance, SpecifyPathEtabs


class ImportEtabs_Dialog(qtw.QDialog, Ui_d_ImportEtabs):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pb_Select.clicked.connect(self.attach_to_instance)
        self.pb_OpenModel.clicked.connect(self.open_etabs_file)

    @qtc.Slot()
    def attach_to_instance(self):
        # TODO: Import and add attach to instance function to connect to etabs
        AttachToInstance()

    @qtc.Slot()
    def open_etabs_file(self):
        file_name = "ETABS Model Files (*.EDB)"
        path = sys.path[0]
        rv = get_open_filename(file_name, path)
        SpecifyPathEtabs()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    import_dialog = ImportEtabs_Dialog()
    import_dialog.show()
    sys.exit(app.exec())
