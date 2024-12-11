from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction


from controllers.calculation_case_modify_dialog import CalculationCaseModify_Dialog
from crud.cr_load_case import get_calculation_case, delete_calculation_case


class TableContextMenu(QMenu):
    modify_action_finished = Signal()
    add_copy_action_finished = Signal()
    delete_action_finished = Signal()

    def __init__(self, table_view, model, parent=None):
        super().__init__(parent)
        self.emit_action_finished = None
        self.table_view = table_view
        self.model = model
        self.engine = None
        self.path = None

        self.current_data = None
        self.modify_dialog = None
        self.add_copy_dialog = None
        # Create actions
        self.add_copy_action = QAction("Add Copy of Load Case", self)
        self.modify_action = QAction("Modify/Show Load Case", self)
        self.delete_action = QAction("Delete Load Case", self)

        # Connect actions to slots
        self.add_copy_action.triggered.connect(self.add_copy_row)
        self.modify_action.triggered.connect(self.modify_row)
        self.delete_action.triggered.connect(self.delete_row)

        # Add actions to the menu
        self.addAction(self.add_copy_action)
        self.addAction(self.modify_action)
        self.addAction(self.delete_action)

    def get_selected_row(self):
        try:
            indexes = self.table_view.selectionModel().selectedRows()
            if indexes:
                return indexes[0].row()
            return None
        except Exception:
            QMessageBox.warning(self.table_view, "Warning", "No row selected")

    def modify_row(self):
        modify = True
        row = self.get_selected_row()
        if row is not None:
            row += 1
            # For simplicity, we update the row with hardcoded values
            self.current_data = get_calculation_case(self.engine, row)
            self.modify_dialog = CalculationCaseModify_Dialog(
                self.engine, self.path, self.current_data, row, modify
            )
            self.modify_dialog.model_modify.connect(self.emit_action_modify_finished)
            self.modify_dialog.exec()

    def add_copy_row(self):
        row = self.get_selected_row()
        modify = False
        if row is not None:
            row += 1
            # For simplicity, we update the row with hardcoded values
            self.current_data = get_calculation_case(self.engine, row)
            self.add_copy_dialog = CalculationCaseModify_Dialog(
                self.engine, self.path, self.current_data, row, modify
            )
            self.add_copy_dialog.model_modify.connect(
                self.emit_action_add_copy_finished
            )
            self.add_copy_dialog.exec()

    def delete_row(self):
        row = self.get_selected_row()
        if row is not None:
            delete_calculation_case(self.engine, row)
            self.delete_action_finished.emit()

    def emit_action_modify_finished(self):
        self.modify_action_finished.emit()

    def emit_action_add_copy_finished(self):
        self.add_copy_action_finished.emit()
