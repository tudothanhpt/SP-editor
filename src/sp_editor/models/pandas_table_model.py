import logging
import sys
from typing import Any, Sequence
import pandas as pd
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw

from sqlmodel import SQLModel


class PandasModel(qtc.QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._dataframe = dataframe

    def rowCount(self, parent=qtc.QModelIndex()) -> int:
        return len(self._dataframe) if parent == qtc.QModelIndex() else 0

    def columnCount(self, parent=qtc.QModelIndex()) -> int:
        return len(self._dataframe.columns) + 1 if parent == qtc.QModelIndex() else 0

    def data(self, index: qtc.QModelIndex, role=qtc.Qt.ItemDataRole):
        if not index.isValid():
            return None
        if role == qtc.Qt.DisplayRole:
            if index.column() == 0:
                return str(self._dataframe.index[index.row()])
            return str(self._dataframe.iloc[index.row(), index.column() - 1])
        return None

    def headerData(
        self, section: int, orientation: qtc.Qt.Orientation, role: qtc.Qt.ItemDataRole
    ):
        if role == qtc.Qt.DisplayRole:
            if orientation == qtc.Qt.Horizontal:
                if section == 0:
                    return "Index"
                return str(self._dataframe.columns[section - 1])
            if orientation == qtc.Qt.Vertical:
                return str(self._dataframe.index[section])
        return None

    @staticmethod
    def sqlmodel_to_df(
        objects: Sequence[SQLModel | Any], set_index: bool = True
    ) -> pd.DataFrame:
        if not objects:
            return pd.DataFrame()

        records = []
        for obj in objects:
            try:
                record = obj.dict()
                records.append(record)
            except Exception as e:
                logging.error(f"Error serializing {obj}: {e}")
                raise

        columns = list(objects[0].__fields__.keys())
        df = pd.DataFrame.from_records(records, columns=columns)
        return df.set_index(columns[0]) if set_index else df


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
