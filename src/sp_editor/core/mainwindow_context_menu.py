from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction

import pandas as pd
from sqlalchemy import Engine

from sp_editor.controllers.calculation_case_modify_dialog import CalculationCaseModify_Dialog
from sp_editor.crud.cr_load_case import get_calculation_case


class TableContextMenu(QMenu):
    def __init__(self, table_view, model, parent=None):
        super().__init__(parent)
        self.table_view = table_view
        self.model = model
        self.engine = None
        self.path = None

        self.current_data = None
        self.update_dialog = None
        # Create actions
        self.update_action = QAction('Update Load Case', self)
        self.duplicate_action = QAction('Duplicate Load Case', self)
        self.delete_action = QAction('Delete Load Case', self)

        # Connect actions to slots
        self.update_action.triggered.connect(self.update_row)
        self.duplicate_action.triggered.connect(self.duplicate_row)
        self.delete_action.triggered.connect(self.delete_row)

        # Add actions to the menu
        self.addAction(self.update_action)
        self.addAction(self.duplicate_action)
        self.addAction(self.delete_action)

    def get_selected_row(self):
        indexes = self.table_view.selectionModel().selectedRows()
        if indexes:
            return indexes[0].row()
        return None

    def update_row(self):
        modify = True
        row = self.get_selected_row()
        if row is not None:
            row += 1
            # For simplicity, we update the row with hardcoded values
            self.current_data = get_calculation_case(self.engine, row)
            self.update_dialog = CalculationCaseModify_Dialog(self.engine, self.path, self.current_data, row, modify)
            self.update_dialog.exec()
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

    def delete_row(self):
        row = self.get_selected_row()
        if row is not None:
            self.model.beginRemoveRows(QModelIndex(), row, row)
            self.model._dataframe = self.model._dataframe.drop(self.model._dataframe.index[row]).reset_index(drop=True)
            self.model.endRemoveRows()
        else:
            QMessageBox.warning(self.table_view, 'Warning', 'No row selected')
