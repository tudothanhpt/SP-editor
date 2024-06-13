import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from sp_editor.widgets.combos_selected_dialog import Ui_Dialog
from sp_editor.utils import get_open_filename
from sp_editor.core.connect_etabs import connect_to_etabs, get_load_combinations
from sp_editor.database.list_model import ListModel
from sp_editor.crud.cr_load_combo import get_df_load_combinations_fromdb, create_df_to_db
from sp_editor.core.connect_etabs import connect_to_etabs

from sqlmodel import Session, create_engine
from typing import Any
from sqlalchemy.engine.base import Engine

engine_temppath = r"C:\Users\abui\Desktop\Git\repo\SP-editor\tests\TestBM\1235.spe"
engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
table_name='loadcombinations'
df_uLoadCombination = get_load_combinations(connect_to_etabs(model_is_open=True)[0])
create_df_to_db(engine,table_name, df_uLoadCombination)
INITIAL_DF = get_df_load_combinations_fromdb(engine)
INITIALDATA=INITIAL_DF.iloc[:, 0].dropna().tolist()


class Combo_Dialog(qtw.QDialog, Ui_Dialog):

    def __init__(self, parent: qtw.QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        
        self.lview_combos_listIndices = None
        self.lview_selectedCombos_listIndices = None
        
        self.lview_combos_model = self.load_DB()
        self.lview_selectedCombos_model = ListModel([])
        
        self.lview_selectedCombos.setModel(self.lview_selectedCombos_model)
        # Connect buttons to the respective functions
        self.pb_select.clicked.connect(self.move_right)
        self.pb_deselect.clicked.connect(self.move_left)

        # Connect OK and Cancel buttons
        self.pb_ok.clicked.connect(self.on_ok_clicked)
        self.pb_cancel.clicked.connect(self.reject)
    def load_DB(self):
        tmpDF =get_df_load_combinations_fromdb(engine)
        self.lview_combos_list = tmpDF.iloc[:, 0].dropna().tolist()
        self.lview_combos_model = ListModel(self.lview_combos_list)
        self.lview_combos.setModel(self.lview_combos_model)

    def move_right(self):
        # Get selected indexes in the left list view
        selected_indexes = self.lview_combos.selectionModel().selectedIndexes()
        print(selected_indexes)
        if selected_indexes:
            # Collect items and their original positions
            items_to_move = [(self.lview_combos.model().data(index, qtc.Qt.DisplayRole), index.row()) for index in sorted(selected_indexes)]
            print(items_to_move)
            # Remove items from left list view
            for item, _ in reversed(items_to_move):
                self.lview_combos.model().remove_item_by_value(item)
            # Add items to right list view
            self.lview_selectedCombos.model().add_items(items_to_move)
            # Sort right list view by original order
            self.lview_selectedCombos.model().sort_items_by_original_order()
            
            self.lview_combos_listIndices  = self.lview_combos.model().get_items_with_indices()
            self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()

    def move_left(self):
        # Get selected indexes in the right list view
        selected_indexes = self.lview_selectedCombos.selectionModel().selectedIndexes()
        if selected_indexes:
            # Collect items and their original positions
            items_to_move = [(self.lview_selectedCombos.model().data(index, qtc.Qt.DisplayRole), index.row()) for index in sorted(selected_indexes)]
            print(items_to_move)
            # Remove items from right list view
            for item, _ in reversed(items_to_move):
                self.lview_selectedCombos.model().remove_item_by_value(item)
            # Add items to left list view
            self.lview_combos.model().add_items(items_to_move)
            # Sort left list view by original order
            self.lview_combos.model().sort_items_by_original_order()
            
            self.lview_combos_listIndices  = self.lview_combos.model().get_items_with_indices()
            self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()
    
    def on_ok_clicked(self):
        print("List 1:")

     

        
        
def main():
    """Main function to run the MaterialDialog."""
    app = qtw.QApplication(sys.argv)
    dialog = Combo_Dialog()
    dialog.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()