import sys
from typing import Any
import pandas as pd
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg


class PandasModel(qtc.QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        qtc.QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=qtc.QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == qtc.QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=qtc.QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == qtc.QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: qtc.QModelIndex, role=qtc.Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == qtc.Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(
            self, section: int, orientation: qtc.Qt.Orientation, role: qtc.Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == qtc.Qt.DisplayRole:
            if orientation == qtc.Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == qtc.Qt.Vertical:
                return str(self._dataframe.index[section])

        return None


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    df = pd.read_csv("iris.csv")

    view = qtw.QTableView()
    view.resize(800, 500)
    view.horizontalHeader().setStretchLastSection(True)
    view.setAlternatingRowColors(True)
    view.setSelectionBehavior(qtw.QTableView.SelectRows)

    model = PandasModel(df)
    view.setModel(model)
    view.show()
    app.exec()
