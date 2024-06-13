import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from sp_editor.widgets.combos_selected_dialog import Ui_combosSelection_dialog
from sp_editor.database.list_model import ListModel
from sp_editor.crud.cr_load_combo import get_df_load_combinations_fromdb, create_df_to_db

from sqlmodel import Session, create_engine
from sqlalchemy.engine.base import Engine

table_name = 'loadcombinations'


# print(INITIAL_DF.to_dict("list"))

class Combo_Dialog(qtw.QDialog, Ui_combosSelection_dialog):

    def __init__(self, engine: Engine | None = None, path: str | None = None) -> None:
        super().__init__()
        self.lview_selectedCombos_model = None
        self.lview_combos_model = None
        self.lview_selectedCombos_list = None
        self.lview_combos_list = None
        self.engine = engine
        self.current_path = path

        self.setupUi(self)

        self.lview_combos_listIndices = None
        self.lview_selectedCombos_listIndices = None

        self.load_DB()

        self.lview_selectedCombos.setModel(self.lview_selectedCombos_model)
        # Connect buttons to the respective functions
        self.pb_select.clicked.connect(self.move_right)
        self.pb_deselect.clicked.connect(self.move_left)

        # Connect OK and Cancel buttons
        self.pb_ok.clicked.connect(self.on_ok_clicked)
        self.pb_cancel.clicked.connect(self.reject)

    def load_DB(self):

        self.tmpDF = get_df_load_combinations_fromdb(self.engine)

        self.lview_combos_list = self.tmpDF.iloc[:, 0].dropna().tolist()
        self.lview_selectedCombos_list = self.tmpDF.iloc[:, 1].dropna().tolist()

        self.lview_combos_model = ListModel(self.lview_combos_list)
        self.lview_selectedCombos_model = ListModel(self.lview_selectedCombos_list)

        self.lview_combos.setModel(self.lview_combos_model)
        self.lview_selectedCombos.setModel(self.lview_selectedCombos_model)

    def move_right(self):
        # Get selected indexes in the left list view
        selected_indexes = self.lview_combos.selectionModel().selectedIndexes()
        if selected_indexes:
            # Collect items and their original positions
            items_to_move = [(self.lview_combos.model().data(index, qtc.Qt.DisplayRole), index.row()) for index in
                             sorted(selected_indexes)]
            print(items_to_move)
            # Remove items from left list view
            for item, _ in reversed(items_to_move):
                self.lview_combos.model().remove_item_by_value(item)
            # Add items to right list view
            self.lview_selectedCombos.model().add_items(items_to_move)
            # Sort right list view by original order
            self.lview_selectedCombos.model().sort_items_by_original_order()
            self.lview_combos_listIndices = self.lview_combos.model().get_items_with_indices()
            self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()

    def move_left(self):
        # Get selected indexes in the right list view
        selected_indexes = self.lview_selectedCombos.selectionModel().selectedIndexes()
        if selected_indexes:
            # Collect items and their original positions
            items_to_move = [(self.lview_selectedCombos.model().data(index, qtc.Qt.DisplayRole), index.row()) for index
                             in sorted(selected_indexes)]
            print(items_to_move)
            # Remove items from right list view
            for item, _ in reversed(items_to_move):
                self.lview_selectedCombos.model().remove_item_by_value(item)
            # Add items to left list view
            self.lview_combos.model().add_items(items_to_move)
            # Sort left list view by original order
            self.lview_combos.model().sort_items_by_original_order()
            self.lview_combos_listIndices = self.lview_combos.model().get_items_with_indices()
            self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()

    def on_ok_clicked(self):
        print("List1 :")
        print(self.lview_combos_listIndices)
        print("List2 :")
        print(self.lview_selectedCombos_listIndices)
        tempdf = self.tmpDF
        for name, index in self.lview_combos_listIndices:
            tempdf.at[index, 'LoadCombinations'] = name
            tempdf.at[index, 'SelectedCombo'] = None
        # Update SelectedCombo column using List2
        for name, index in self.lview_selectedCombos_listIndices:
            tempdf.at[index, 'SelectedCombo'] = name
            tempdf.at[index, 'LoadCombinations'] = None

        print(tempdf)
        tempdf.to_sql(table_name, con=self.engine, if_exists='replace', index=False)


def main():
    """Main function to run the MaterialDialog."""
    app = qtw.QApplication(sys.argv)
    dialog = Combo_Dialog()
    dialog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
