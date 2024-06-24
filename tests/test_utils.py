import sys
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QMenu, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
import pandas as pd
from typing import Sequence, Any


class MainWindowPandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas DataFrame"""

    def __init__(self, dataframe: pd.DataFrame = pd.DataFrame(), parent=None, headers=None):
        super().__init__(parent)
        self._dataframe = dataframe
        if headers:
            self._dataframe.columns = headers

    def rowCount(self, parent=QModelIndex()) -> int:
        """Return row count of the pandas DataFrame"""
        return len(self._dataframe) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Return column count of the pandas DataFrame"""
        return len(self._dataframe.columns) if not parent.isValid() else 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        """Return data cell from the pandas DataFrame"""
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole):
        """Return DataFrame index as vertical header data and columns as horizontal header data"""
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._dataframe.columns[section])
            elif orientation == Qt.Orientation.Vertical:
                return str(self._dataframe.index[section])

        return None

    def update_dataframe(self, dataframe: pd.DataFrame, headers=None):
        """Update the model with a new DataFrame"""
        self.beginResetModel()
        self._dataframe = dataframe
        if headers:
            self._dataframe.columns = headers
        self.endResetModel()

    @staticmethod
    def sqlmodel_to_df(objects: Sequence[Any]) -> pd.DataFrame:
        """Converts SQLModel objects into a Pandas DataFrame"""
        if not objects:
            return pd.DataFrame()  # Return an empty DataFrame if the list is empty
        else:
            # Extract data from SQLModel objects
            data = [model.dict() for model in objects]
            # Get the column order from the first SQLModel object
            column_order = list(objects[0].__fields__.keys())
            # Convert the list of dictionaries to a pandas DataFrame
            df_out = pd.DataFrame(data)
            # Apply the column order
            df_out = df_out[column_order]
        return df_out


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QTableView with MainWindowModel')
        self.setGeometry(100, 100, 800, 600)

        # Create the QTableView
        self.table_view = QTableView(self)
        self.setCentralWidget(self.table_view)

        # Create a sample DataFrame
        data = {
            'Header1': [1, 2, 3],
            'Header2': ['A', 'B', 'C'],
            'Header3': [True, False, True]
        }
        df = pd.DataFrame(data)

        # Create a MainWindowModel with the sample DataFrame
        self.model = MainWindowPandasModel(dataframe=df, headers=['Header1', 'Header2', 'Header3'])
        self.table_view.setModel(self.model)

        # Set up context menu
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.open_context_menu)

    def open_context_menu(self, position):
        menu = QMenu()

        delete_action = QAction('Delete Row', self)
        delete_action.triggered.connect(self.delete_row)
        menu.addAction(delete_action)

        update_action = QAction('Update Row', self)
        update_action.triggered.connect(self.update_row)
        menu.addAction(update_action)

        duplicate_action = QAction('Duplicate Row', self)
        duplicate_action.triggered.connect(self.duplicate_row)
        menu.addAction(duplicate_action)

        menu.exec(self.table_view.viewport().mapToGlobal(position))

    def get_selected_row(self):
        indexes = self.table_view.selectionModel().selectedRows()
        if indexes:
            return indexes[0].row()
        return None

    def delete_row(self):
        row = self.get_selected_row()
        if row is not None:
            self.model.beginRemoveRows(QModelIndex(), row, row)
            self.model._dataframe = self.model._dataframe.drop(self.model._dataframe.index[row]).reset_index(drop=True)
            self.model.endRemoveRows()
        else:
            QMessageBox.warning(self, 'Warning', 'No row selected')

    def update_row(self):
        row = self.get_selected_row()
        if row is not None:
            # For simplicity, we update the row with hardcoded values
            self.model._dataframe.iloc[row] = [4, 'D', False]
            self.model.dataChanged.emit(self.model.index(row, 0), self.model.index(row, self.model.columnCount() - 1))
        else:
            QMessageBox.warning(self, 'Warning', 'No row selected')

    def duplicate_row(self):
        row = self.get_selected_row()
        if row is not None:
            self.model.beginInsertRows(QModelIndex(), row + 1, row + 1)
            new_row = self.model._dataframe.iloc[row].copy()
            self.model._dataframe = pd.concat([self.model._dataframe.iloc[:row + 1], pd.DataFrame([new_row]),
                                               self.model._dataframe.iloc[row + 1:]]).reset_index(drop=True)
            self.model.endInsertRows()
        else:
            QMessageBox.warning(self, 'Warning', 'No row selected')


# Test the MainWindowModel with a QTableView in a PySide6 application
if __name__ == "__main__":
    app = QApplication([])

    # Create the main window
    window = MainWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec())
