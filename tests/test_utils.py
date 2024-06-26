import pandas as pd
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate


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
        elif role == Qt.ItemDataRole.BackgroundRole and index.column() == 9:  # Assuming DCR column is at index 9
            value = self._dataframe.iloc[index.row(), index.column()]
            try:
                value = float(value)
            except ValueError:
                value = 1.0
            color = self.get_color_for_value(value)
            return QBrush(color)

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole):
        """Return DataFrame index as vertical header data and columns as horizontal header data"""
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._dataframe.columns[section])
            elif orientation == Qt.Orientation.Vertical:
                return str(self._dataframe.index[section])

        return None

    def update_model_from_db(self, engine):
        """Update model with new data from the database"""
        new_data = fetch_data_from_db(engine=engine)  # Fetch new data from database
        # Prepare data as list of lists (rows)
        # Convert to DataFrame
        column_headers = ["SPColumn File", "Tier", "From Story", "To Story", "Pier",
                          "Material Fc", "Material Fy", "Bar No", "Rho", "DCR",
                          "Force Combo"]

        new_df = new_data.set_axis(column_headers, axis=1)

        # Convert DCR column to numeric
        new_df['DCR'] = pd.to_numeric(new_df['DCR'], errors='coerce').fillna(1.0)

        # Update the model
        self.beginResetModel()
        self._dataframe = new_df
        self.endResetModel()

    def get_color_for_value(self, value):
        """Get color for value with gradient"""
        min_value, max_value = 0, 1
        value = min(max(value, min_value), max_value)
        ratio = (value - min_value) / (max_value - min_value)
        r = int(255 * (1 - ratio))
        g = int(255 * ratio)
        return QColor(r, g, 0)


class DCRDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        value = float(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        color = index.model().get_color_for_value(value)
        option.backgroundBrush = QBrush(color)
        super().paint(painter, option, index)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableView with Pandas DataFrame")
        self.resize(800, 600)

        self.table = QTableView()
        self.setCentralWidget(self.table)

        data = {
            "SPColumn File": ["t2_CORE4-ALL.cti", "t1_CORE4-ALL.cti"],
            "Tier": ["t2", "t1"],
            "From Story": ["Story21", "B1"],
            "To Story": ["Story38", "Story20"],
            "Pier": ["CORE4-ALL", "CORE4-ALL"],
            "Material Fc": [10.0, 10.0],
            "Material Fy": [60.0, 60.0],
            "Bar No": ["#18", "#18"],
            "Rho": [0.95, 0.95],
            "DCR": [0.57, 1.04],
            "Force Combo": [481, 1382]
        }
        df = pd.DataFrame(data)

        self.model = MainWindowModel(df)
        self.table.setModel(self.model)

        dcr_delegate = DCRDelegate(self.table)
        self.table.setItemDelegateForColumn(9, dcr_delegate)  # Assuming DCR column is at index 9


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
