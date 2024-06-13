import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from sp_editor.widgets.levelgroup_dialog import Ui_group_dialog

from crud.cr_level_group import (get_level, get_pierlabel_with_level, get_group_level,
                                 update_group_level, create_level_group)
from database.pandas_table_model import PandasModel
from sqlalchemy.engine.base import Engine


class Group_Dialog(qtw.QDialog, Ui_group_dialog):
    def __init__(self, engine: Engine | None = None, path: str | None = None):
        super().__init__()
        self.group_model = None
        self.group_df = None
        self.groups_list = None
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
        if not text and self.select_stories is None:
            qtw.QMessageBox.warning(self, 'Warning', 'Group Name and'
                                                     ' Selected Stories cannot be empty')
        else:
            self.le_groupName.clear()
            groups = update_group_level(self.engine, self.select_stories, text)
            # get tier from group level table
            self.groups_list = get_group_level(self.engine)
            # using function to make list unique
            tier_names_unique = self.get_unique_items(self.groups_list)
            # using qstringlist model to transform and display model
            self.group_model = qtc.QStringListModel()
            self.group_model.setStringList(tier_names_unique)
            self.lview_groupName.setModel(self.group_model)
            self.update_level_list()

    @qtc.Slot()
    def display_level(self):
        # get level from level table
        self.level_list = get_level(self.engine)
        # using level_df to initiate level group table
        create_level_group(self.engine, self.level_list)
        # display level model
        self.level_model = qtc.QStringListModel()
        self.level_model.setStringList(self.level_list)
        self.lview_storyName.setModel(self.level_model)

    @qtc.Slot()
    def get_piers_from_selection(self, selected, deselected):
        # get selected stories and return it to list
        # self.lview_pierName.
        items = self.lview_storyName.selectionModel().selectedIndexes()
        self.select_stories = [item.data() for item in items]

        # get pier labels based on selected story
        self.pier_names = get_pierlabel_with_level(self.engine, self.select_stories)

        # using function to make list unique
        pier_names_unique = self.get_unique_items(self.pier_names)
        # using qstringlist model to transform and display model
        self.pier_model = qtc.QStringListModel()
        self.pier_model.setStringList(pier_names_unique)
        self.lview_pierName.setModel(self.pier_model)

    @qtc.Slot()
    def get_unique_items(self, items):
        # Remove duplicates while preserving order
        unique_items = []
        seen = set()
        for item in items:
            if item not in seen:
                unique_items.append(item)
                seen.add(item)
        return unique_items

    @qtc.Slot()
    def update_level_list(self):
        current_items = self.level_model.stringList()
        updated_items = [item for item in current_items
                         if item not in self.select_stories]
        self.level_model.setStringList(updated_items)
        if self.level_model is None:
            self.pier_model.setStringList([])


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    group_dialog = Group_Dialog()
    group_dialog.show()
    sys.exit(app.exec())
