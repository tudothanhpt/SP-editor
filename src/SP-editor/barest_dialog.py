import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtSql as qsql

from sqlalchemy.engine.base import Engine
from crud.cr_barset import create_barset, get_barset
from database.ui_table_sql.connection import create_connection, create_model

from core.global_variables import BarGroupType
from crud.cr_general_infor import get_infor
from widgets.barSet_dialog import Ui_d_BarSet


class BarSet_Dialog(qtw.QDialog, Ui_d_BarSet):
    def __init__(self, engine: Engine | None = None, path: str | None = None):
        super().__init__()

        self.engine = engine
        self.current_path = path
        self.table_name = "barset"
        self.infor = get_infor(self.engine)

        self.setupUi(self)
        create_connection(self, self.current_path, self.table_name)
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


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    barset_dialog = BarSet_Dialog()
    barset_dialog.show()
    sys.exit(app.exec())
