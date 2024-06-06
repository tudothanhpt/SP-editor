import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtSql as qsql

from sqlalchemy.engine.base import Engine
from crud.cr_barset import create_barset, get_barset

from core.global_variables import BarGroupType
from crud.cr_general_infor import get_infor
from widgets.barSet_dialog import Ui_d_BarSet


class BarSet_Dialog(qtw.QDialog, Ui_d_BarSet):
    def __init__(self, engine: Engine | None = None, path: str | None = None):
        super().__init__()

        self.engine = engine
        self.current_path = path
        self.infor = get_infor(self.engine)

        self.setupUi(self)
        self.create_connection()
        self.text_changed()
        self.cb_BarSetList.clear()
        self.cb_BarSetList.addItems(list(str(barset) for barset in BarGroupType))
        self.cb_BarSetList.setCurrentText(self.infor.bar_set)
        # self.cb_BarSetList.currentTextChanged.connect(self.text_changed)

    def text_changed(self):
        ctext = self.cb_BarSetList.currentText()

        model = qsql.QSqlTableModel()
        model.setTable("barset")
        self.tbview_BarSet.setModel(model)
        model.select()

    def create_connection(self):
        database = qsql.QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName(self.current_path)
        if not database.open():
            sys.exit(1)
        tables_needed = {"barset"}
        tables_not_found = tables_needed - set(database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(self, "Error",
                                     f"<p> The following table are missing"
                                     f"from the database:{tables_not_found}<p>")
            sys.exit(-1)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    barset_dialog = BarSet_Dialog()
    barset_dialog.show()
    sys.exit(app.exec())
