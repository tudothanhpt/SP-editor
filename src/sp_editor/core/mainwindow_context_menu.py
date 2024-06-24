from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction

import pandas as pd


class TableContextMenu(QMenu):
    def __init__(self, table_view, model, parent=None):
        super().__init__(parent)
        self.table_view = table_view
        self.model = model

        # Create actions
        self.delete_action = QAction('Delete Row', self)
        self.update_action = QAction('Update Row', self)
        self.duplicate_action = QAction('Duplicate Row', self)

        # Connect actions to slots
        self.delete_action.triggered.connect(self.delete_row)
        self.update_action.triggered.connect(self.update_row)
        self.duplicate_action.triggered.connect(self.duplicate_row)

        # Add actions to the menu
        self.addAction(self.delete_action)
        self.addAction(self.update_action)
        self.addAction(self.duplicate_action)

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
            QMessageBox.warning(self.table_view, 'Warning', 'No row selected')

    def update_row(self):
        row = self.get_selected_row()
        if row is not None:
            # For simplicity, we update the row with hardcoded values
            self.model._dataframe.iloc[row] = [4, 'D', False]
            self.model.dataChanged.emit(self.model.index(row, 0), self.model.index(row, self.model.columnCount() - 1))
        else:
            QMessageBox.warning(self.table_view, 'Warning', 'No row selected')

    def duplicate_row(self):
        row = self.get_selected_row()
        if row is not None:
            self.model.beginInsertRows(QModelIndex(), row + 1, row + 1)
            new_row = self.model._dataframe.iloc[row].copy()
            self.model._dataframe = pd.concat([self.model._dataframe.iloc[:row + 1], pd.DataFrame([new_row]),
                                               self.model._dataframe.iloc[row + 1:]]).reset_index(drop=True)
            self.model.endInsertRows()
        else:
            QMessageBox.warning(self.table_view, 'Warning', 'No row selected')
