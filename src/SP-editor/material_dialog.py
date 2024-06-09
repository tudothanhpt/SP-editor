import sys
import os
sys.path.append(os.getcwd())
import pandas as pd
from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog, QApplication, QHeaderView, QTableView, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QPoint, QModelIndex
from sqlalchemy.engine import Engine

from widgets.material_dialog import Ui_d_material
from widgets.misc_dialog import show_database_updated_message
from database.pandas_model_material import PandasModelMaterial
from crud.cr_material import set_engine, get_df_from_db, update_df_to_db
from utils import read_json_to_df, prompt_json_file
INITDATA_CONC = {
    "name": [None],
    "fc": [None],
    "Ec": [None],
    "max_fc": [None],
    "beta_1": [None],
    "eu": [None]
}

INITDATA_STEEL = {
    "name": [None],
    "fy": [None],
    "Es": [None],
    "ety": [None]
}

DB_TBLNAME_CONC = "materialconcrete"
DB_TBLNAME_REBAR = "materialrebar"

class Material_Dialog(QtWidgets.QDialog, Ui_d_material):
    """Dialog class to handle user interactions for material data."""
    
    def __init__(self, engine: Engine, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.engine = engine
        self.db_dir = '.\\src\\SP-editor\\database\\material_table\\'
        # Define headers for the tables
        headers_concrete = ["name", "fc", "Ec", "max_fc", "beta_1", "eu"]
        headers_steel = ["name", "fy", "Es", "ety"]
        # Set up table headers
        self.setup_table_headers(self.tbview_concrete, headers_concrete)
        self.setup_table_headers(self.tbview_steel, headers_steel)

        # Connect signals to slots
        self.pb_apply.clicked.connect(self.apply_table_data)
        self.pb_load.clicked.connect(self.load_table_data)
        self.pb_add.clicked.connect(self.on_add_clicked)
        self.pb_delete.clicked.connect(self.on_delete_clicked)

        # Set context menu policy and connect context menu
        for view, menu_func in [(self.tbview_concrete, self.on_context_menu), 
                                (self.tbview_steel, self.on_context_menu_steel)]:
            view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            view.customContextMenuRequested.connect(menu_func)

        self.display_data_from_db()
        
    def setup_table_headers(self, table_view: QTableView, headers: list) -> None:
        """Set up table headers for the given table view."""
        model = PandasModelMaterial(pd.DataFrame(columns=headers))
        table_view.setModel(model)
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        table_view.setSelectionBehavior(QTableView.SelectRows)
    
    def display_data_from_db(self) -> None:
        """Initialize table data with current db values."""
        df_db_concrete=get_df_from_db(engine=self.engine,table_name=DB_TBLNAME_CONC)
        df_db_rebar=get_df_from_db(engine=self.engine,table_name=DB_TBLNAME_REBAR)
        model_df_db_concrete :PandasModelMaterial = PandasModelMaterial(df_db_concrete)
        model_df_db_rebar = PandasModelMaterial(df_db_rebar)
        self.tbview_concrete.setModel(model_df_db_concrete)
        self.tbview_steel.setModel(model_df_db_rebar)
        
    def load_table_data(self) -> None:
        """Load data into the current tab's table from the selected JSON file."""

        json_file_path=prompt_json_file(self.db_dir)
        
        current_tab = self.tabWidget.currentIndex()
        if current_tab == 0:
            table_view = self.tbview_concrete
        elif current_tab == 1:
            table_view = self.tbview_steel
        else:
            return

        if self.engine and json_file_path:
            self.load_data_to_table(table_view, json_file_path)
    
    def load_data_to_table(self, table_view: QTableView, json_file_path: str) -> None:
        """Load data into the specified table view from the SQL database and append it to the existing data."""

        model: PandasModelMaterial = table_view.model()
        new_df = read_json_to_df(json_file_path)

        if model and hasattr(model, 'df') and model.df is not None:
            combined_df = pd.concat([model.df, new_df], ignore_index=True)
            model.update_data(combined_df)
        else:
            model = PandasModelMaterial(new_df)
            table_view.setModel(model)

        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def apply_table_data(self) -> None:
        """Save table data back to the SQL database."""

        self.save_dbdata_from_tableview(self.tbview_concrete, DB_TBLNAME_CONC)
        self.save_dbdata_from_tableview(self.tbview_steel, DB_TBLNAME_REBAR)
        QMessageBox().information(self, "Success", "Data saved successfully!")
    
    def save_dbdata_from_tableview(self, table_view: QTableView, table_name: str) -> None:
        """Save data from the specified table view back to the SQL database."""
        model : PandasModelMaterial = table_view.model()
        if model and hasattr(model, 'df') and model.df is not None:
            update_df_to_db(self.engine,table_name,model.df)
    
    def on_delete_clicked(self) -> None:
        """Clear the data in the table views."""
        self.modify_table_data(self.clear_data)

    def on_add_clicked(self) -> None:
        """Handle adding a new material entry."""
        active_tab = self.tabWidget.currentIndex()
        
        if active_tab == 0:  # Assuming the first tab is for concrete
            self.add_row_to_table(self.tbview_concrete)
        elif active_tab == 1:  # Assuming the second tab is for steel
            self.add_row_to_table(self.tbview_steel)
    
    def add_row_to_table(self, view: QTableView) -> None:
        """Add a new row to the specified table view."""
        model = view.model()
        if model:
            row_count = model.rowCount()
            model.beginInsertRows(QModelIndex(), row_count, row_count)
            new_row = pd.Series([""] * len(model.df.columns), index=model.df.columns)
            model.df = model.df._append(new_row, ignore_index=True)
            model.endInsertRows()

    def modify_table_data(self, modify_func) -> None:
        """Modify data in both tables using the provided function."""
        for view in [self.tbview_concrete, self.tbview_steel]:
            model = view.model()
            if model:
                modify_func(model)
                
    def clear_data(self, model: PandasModelMaterial) -> None:
        """Clear data in the given model."""
        model.beginResetModel()
        model.df.drop(model.df.index, inplace=True)
        model.endResetModel()

    
    def on_context_menu(self, point: QPoint) -> None:
        """Create and display a context menu with a delete action for concrete table."""
        self.show_context_menu(self.tbview_concrete, point)
    
    def on_context_menu_steel(self, point: QPoint) -> None:
        """Create and display a context menu with a delete action for steel table."""
        self.show_context_menu(self.tbview_steel, point)
    
    def show_context_menu(self, view: QTableView, point: QPoint) -> None:
        """Show context menu with delete action for the given table view."""
        context_menu = QtWidgets.QMenu(view)
        delete_action = context_menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_selected_row(view))
        context_menu.exec(view.mapToGlobal(point))
    
    def delete_selected_row(self, view: QTableView) -> None:
        """Delete the selected row(s) from the given table view."""
        selection_model = view.selectionModel()
        selected_indexes = selection_model.selectedRows()
        if selected_indexes:
            model = view.model()
            if model and hasattr(model, 'df') and model.df is not None:
                model.beginResetModel()
                for index in sorted(selected_indexes, reverse=True):
                    model.df.drop(index.row(), inplace=True)
                model.df.reset_index(drop=True, inplace=True)
                model.endResetModel()

def main():
    """Main function to run the MaterialDialog."""
    app = QApplication(sys.argv)
    database_path = r"C:\\Users\\abui\\Documents\\BM\\git\\repo\\SP-editor\\tests\\demoAB1.spe"
    engine = set_engine(database_path)

    if engine:
        dialog = Material_Dialog(engine)
        dialog.show()
        sys.exit(app.exec())
    else:
        print("Failed to set up the database engine.")

if __name__ == "__main__":
    main()
