import pandas as pd
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QPoint
from PySide6.QtWidgets import QTableView,QAbstractItemView


class PandasModelMaterial(QAbstractTableModel):
    """A model to interface a pandas DataFrame with QTableView."""
    
    def __init__(self, df: pd.DataFrame = pd.DataFrame(), parent=None):
        super().__init__(parent)
        self.df = df

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Returns the header data for the given section and orientation."""
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.df.columns[section]
        elif orientation == Qt.Vertical:
            return self.df.index[section]

    def data(self, index, role=Qt.DisplayRole):
        """Returns the data for the given index."""
        if role != Qt.DisplayRole:
            return None

        if not index.isValid():
            return None

        return str(self.df.iloc[index.row(), index.column()])

    def setData(self, index, value, role=Qt.EditRole):
        """Sets the data for the given index and role."""
        if role == Qt.EditRole:
            self.df.iloc[index.row(), index.column()] = value
            return True
        return False

    def rowCount(self, parent=QModelIndex()):
        """Returns the number of rows in the model."""
        return len(self.df.index)

    def columnCount(self, parent=QModelIndex()):
        """Returns the number of columns in the model."""
        return len(self.df.columns)

    def sort(self, column, order):
        """Sorts the model by the given column and order."""
        colname = self.df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self.df.sort_values(colname, ascending=order == Qt.AscendingOrder, inplace=True)
        self.df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def flags(self, index):
        """Returns the item flags for the given index."""
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
    
    def update_data(self, df):
        self.df = df
        self.layoutChanged.emit()
    
class HighlightTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            self.selectRow(index.row())
        super().mouseMoveEvent(event)
