import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from sp_editor.widgets.levelgroup_dialog import Ui_group_dialog

from crud.cr_level_group import get_level
from database.pandas_table_model import PandasModel
from sqlalchemy.engine.base import Engine


class Group_Dialog(qtw.QDialog, Ui_group_dialog):
    def __init__(self, engine: Engine | None = None, path: str | None = None):
        super().__init__()
        self.level_list = None
        self.engine = engine
        self.current_path = path

        self.setupUi(self)
        self.display_level()
        (self.lview_storyName.selectionModel()
         .selectionChanged.connect(self.get_piers_from_selection))
        self.pb_addGroup.clicked.connect(self.add_group)

    @qtc.Slot()
    def add_group(self):
        pass

    @qtc.Slot()
    def display_level(self):
        self.level_list = get_level(self.engine)
        level_df = PandasModel.sqlmodel_to_df(self.level_list)
        model = PandasModel(level_df[['story']])
        self.lview_storyName.setModel(model)

    @qtc.Slot()
    def get_piers_from_selection(self, selected, deselected):
        self.lview_pierName.clear()
        items = self.lview_storyName.selectionModel().selectedIndexes()
        for i in list(items):
            self.lview_pierName.addItems(i.data())


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    group_dialog = Group_Dialog()
    group_dialog.show()
    sys.exit(app.exec())
