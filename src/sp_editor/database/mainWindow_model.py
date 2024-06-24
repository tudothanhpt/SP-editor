import sys
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QMenu, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
import pandas as pd
from typing import Sequence, Any


class MainWindowModel(QAbstractTableModel):
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
