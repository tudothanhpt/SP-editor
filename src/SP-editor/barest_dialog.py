import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtSql as qsql

from sqlalchemy.engine.base import Engine
from crud.cr_barset import create_barset, get_barset, update_barset
from database.pandas_table_model import PandasModel

from core.global_variables import BarGroupType
from crud.cr_general_infor import get_infor
from widgets.barSet_dialog import Ui_d_BarSet


class BarSet_Dialog(qtw.QDialog, Ui_d_BarSet):
    def __init__(self, engine: Engine | None = None, path: str | None = None):
        super().__init__()

        self.current_barset = None
        self.current_text = None
        self.engine = engine
        self.current_path = path
        self.table_name = "barset"
        self.infor = get_infor(self.engine)

        self.setupUi(self)

        self.cb_BarSetList.clear()
        self.cb_BarSetList.addItems(list(str(barset) for barset in BarGroupType))
        self.current_text = self.infor.bar_set
        self.cb_BarSetList.setCurrentText(self.current_text)
        self.display_df_model()
        self.cb_BarSetList.currentTextChanged.connect(self.text_changed)

    def text_changed(self):
        self.current_text = self.cb_BarSetList.currentText()
        update_barset(self.engine, self.current_text)
        self.display_df_model()

    def display_df_model(self):
        self.current_barset = get_barset(self.engine, self.current_text)
        barset_df = PandasModel.sqlmodel_to_df(self.current_barset)
        model = PandasModel(barset_df)
        self.tbview_BarSet.setModel(model)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    barset_dialog = BarSet_Dialog()
    barset_dialog.show()
    sys.exit(app.exec())
