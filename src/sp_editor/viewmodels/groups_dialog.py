import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from sp_editor.widgets.levelgroup_dialog import Ui_group_dialog

from crud.cr_level_group import get_level, get_pierlabel_with_level, update_group_level, create_level_group
from database.pandas_table_model import PandasModel
from sqlalchemy.engine.base import Engine


class Group_Dialog(qtw.QDialog, Ui_group_dialog):
    def __init__(self, engine: Engine | None = None, path: str | None = None):
        super().__init__()
        self.level_df = None
        self.pier_model = None
        self.level_model = None
        self.select_stories = None
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
        text = self.le_groupName.text()
        if not text:
            qtw.QMessageBox.warning(self, 'Warning', 'Group Name cannot be empty')
        else:
            groups = update_group_level(self.pier_model, self.select_stories, text)
            print(groups)

    @qtc.Slot()
    def display_level(self):
        self.level_list = get_level(self.engine)
        self.level_df = PandasModel.sqlmodel_to_df(self.level_list)[['story']]
        create_level_group(self.engine, self.level_df['story'])
        self.level_model = PandasModel(self.level_df)
        self.lview_storyName.setModel(self.level_model)

    @qtc.Slot()
    def get_piers_from_selection(self, selected, deselected):
        # get selected stories and return it to list
        # self.lview_pierName.
        items = self.lview_storyName.selectionModel().selectedIndexes()
        self.select_stories = [item.data() for item in items]

        # get pier labels based on selected story
        self.pier_names = get_pierlabel_with_level(self.engine, self.select_stories)

        # using set to make list unique
        pier_names_unique = self.get_unique_items(self.pier_names)
        print(pier_names_unique)
        # using qstringlist model to transform model
        self.pier_model = qtc.QStringListModel()
        self.pier_model.setStringList(pier_names_unique)
        self.lview_pierName.setModel(self.pier_model)

    @qtc.Slot()
    def get_unique_items(self, piernames):
        # Remove duplicates while preserving order
        unique_piernames = []
        seen = set()
        for piername in piernames:
            if piername not in seen:
                unique_piernames.append(piername)
                seen.add(piername)
        return unique_piernames


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    group_dialog = Group_Dialog()
    group_dialog.show()
    sys.exit(app.exec())
