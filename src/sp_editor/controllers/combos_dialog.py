import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
import pandas as pd

from sp_editor.widgets.combos_selected_dialog import Ui_combosSelection_dialog
from sp_editor.database.list_model import ListModel
from sp_editor.crud.cr_load_combo import read_loadComboDB, read_loadComboSelectionDB
from sp_editor.crud.cr_load_combo import TB_COMBOSELECTION, TB_CS_HEADER_SELECTEDCOMBO, TB_CS_HEADER_ORICOMBO

from sqlmodel import create_engine
from typing import *
from sqlalchemy.engine.base import Engine


class Combo_Dialog(qtw.QDialog, Ui_combosSelection_dialog):

    def __init__(self, engine: Engine, parent: qtw.QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.engine = engine

        self.INIT_DF = read_loadComboDB(self.engine)
        print(self.INIT_DF)
        self.INIT_LIST = self.INIT_DF["uniqueloadCombos"].to_list()
        self.ORDER_DICT = {string: index for index, string in enumerate(self.INIT_LIST)}

        self.load_DB(self.engine)

        # Connect buttons to the respective functions
        self.pb_select.clicked.connect(self.move_right)
        self.pb_deselect.clicked.connect(self.move_left)

        # Connect OK and Cancel buttons
        self.pb_ok.clicked.connect(self.on_ok_clicked)
        self.pb_cancel.clicked.connect(self.reject)

    def load_DB(self, engine: Engine) -> None:
        """
        Load data from the database and set up the list models.

        Args:
            engine (Engine): The SQLAlchemy engine to connect to the database.

        Returns:
            None
        """

        self.tmpDF: pd.DataFrame = read_loadComboSelectionDB(engine)
        print(self.tmpDF)

        self.lview_combos_list: list[str] = self.tmpDF.iloc[:, 0].dropna().tolist()
        self.lview_selectedCombos_list: list[str] = self.tmpDF.iloc[:, 1].dropna().tolist()

        self.lview_combos_model: ListModel = ListModel(self.lview_combos_list, self.ORDER_DICT)
        self.lview_selectedCombos_model: ListModel = ListModel(self.lview_selectedCombos_list, self.ORDER_DICT)

        self.lview_combos.setModel(self.lview_combos_model)
        self.lview_selectedCombos.setModel(self.lview_selectedCombos_model)

        self.lview_combos_listIndices: List[Tuple[str, int]] = self.lview_combos.model().get_items_with_indices()
        self.lview_selectedCombos_listIndices: List[
            Tuple[str, int]] = self.lview_selectedCombos.model().get_items_with_indices()

    def move_right(self) -> None:
        """
        Move selected items from the left list view to the right list view.

        Returns:
            None
        """
        # Get selected items from the left list view
        selected_items: List[Tuple[str, int]] = [
            (self.lview_combos.model().data(index, qtc.Qt.DisplayRole), index.row())
            for index in sorted(self.lview_combos.selectionModel().selectedIndexes())
        ]

        # Remove selected items from the left list view
        for item, _ in reversed(selected_items):
            self.lview_combos.model().remove_item_by_value(item)

        # Add selected items to the right list view
        self.lview_selectedCombos.model().add_items(selected_items)
        self.lview_selectedCombos.model().sort_items_by_original_order()

        # Update indices of the lists
        self.lview_combos_listIndices = self.lview_combos.model().get_items_with_indices()
        self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()

    def move_left(self):
        # Get selected items from the right list view
        selected_items = [
            (self.lview_selectedCombos.model().data(index, qtc.Qt.DisplayRole), index.row())
            for index in sorted(self.lview_selectedCombos.selectionModel().selectedIndexes())
        ]

        # Remove selected items from the right list view
        for item, _ in reversed(selected_items):
            self.lview_selectedCombos.model().remove_item_by_value(item)

        # Add selected items to the left list view
        self.lview_combos.model().add_items(selected_items)

        # Sort left list view by original order
        self.lview_combos.model().sort_items_by_original_order()

        # Update indices of the lists
        self.lview_combos_listIndices = self.lview_combos.model().get_items_with_indices()
        self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()

    def on_ok_clicked(self):
        """Update database table with selected items."""
        for combo_name, index in self.lview_combos_listIndices:
            self.tmpDF.at[index, TB_CS_HEADER_ORICOMBO] = combo_name
            self.tmpDF.at[index, TB_CS_HEADER_SELECTEDCOMBO] = None

        for selected_combo_name, index in self.lview_selectedCombos_listIndices:
            self.tmpDF.at[index, TB_CS_HEADER_SELECTEDCOMBO] = selected_combo_name
            self.tmpDF.at[index, TB_CS_HEADER_ORICOMBO] = None

        totalCombos = len(self.lview_combos_listIndices)
        totalSelectedCombos = len(self.lview_selectedCombos_listIndices)
        total = totalCombos + totalSelectedCombos

        self.tmpDF.to_sql(TB_COMBOSELECTION, con=self.engine, if_exists='replace', index=False)

        qtw.QMessageBox().information(self, "Notifications", f"{totalSelectedCombos}/{total} selected!")
        self.close()

       

    def print_current_state(self):
        print("List1 :")
        print(self.lview_combos_listIndices)
        print("List2 :")
        print(self.lview_selectedCombos_listIndices)


def main():
    """Main function to run the Get Combination Dialog."""
    engine_temppath = r"C:\Users\abui\Desktop\Git\repo\SP-editor\tests\TestBM\DEMONO1.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
    app = qtw.QApplication(sys.argv)
    dialog = Combo_Dialog(engine)
    dialog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
