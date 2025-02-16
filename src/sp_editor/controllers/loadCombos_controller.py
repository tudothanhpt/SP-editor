from dependency_injector.wiring import inject, Provide
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from typing import List, Tuple

from sp_editor.containers.service_container import ServiceContainer
from sp_editor.services.loadCombos_service import LoadCombosService
from sp_editor.widgets.combos_selected_dialog import Ui_combosSelection_dialog
from sp_editor.models.list_model import ListModel  # Custom list model for list view


class LoadCombosController(qtw.QDialog, Ui_combosSelection_dialog):
    def __init__(
            self,
            loadCombos_service: LoadCombosService = Provide[ServiceContainer.loadCombos_service],
            parent: qtw.QWidget = None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.loadCombos_service = loadCombos_service

        # Initialize empty values for lists/models
        self.unique_combos = []
        self.selected_combos = []
        self.ORDER_DICT = {}
        self.lview_combos_model = None
        self.lview_selectedCombos_model = None
        self.lview_combos_listIndices = []
        self.lview_selectedCombos_listIndices = []

        # Postponed initialization: call initialize_data() later once dependencies are ready.

    def get_loadCombos_and_display(self):
        """
        Initializes the load combination data and connects the UI signals.
        This function should be called after dependency injection is complete.
        """
        # Load initial data from the service: two lists for unique and selected combos.
        self.unique_combos, self.selected_combos = self.loadCombos_service.get_load_combo_lists()

        # Create an order dictionary to preserve the original order.
        self.ORDER_DICT = {combo: idx for idx, combo in enumerate(self.unique_combos)}

        # Create list models for both list views using our custom ListModel.
        self.lview_combos_model = ListModel(self.unique_combos, self.ORDER_DICT)
        self.lview_selectedCombos_model = ListModel(self.selected_combos, self.ORDER_DICT)

        # Set models to the list views.
        self.lview_combos.setModel(self.lview_combos_model)
        self.lview_selectedCombos.setModel(self.lview_selectedCombos_model)

        # Cache current indices (if needed for further processing).
        self.lview_combos_listIndices = self.lview_combos.model().get_items_with_indices()
        self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()

        # Connect UI signals to slots.
        self.pb_select.clicked.connect(self.move_right)
        self.pb_deselect.clicked.connect(self.move_left)
        self.pb_ok.clicked.connect(self.on_ok_clicked)
        self.pb_cancel.clicked.connect(self.reject)

    def move_right(self) -> None:
        """
        Move selected items from the left list view to the right list view.
        """
        # Get selected items from the left list view (sort in reverse to avoid index shifting issues)
        selected_indexes = sorted(
            self.lview_combos.selectionModel().selectedIndexes(),
            key=lambda idx: idx.row(),
            reverse=True
        )
        selected_items: List[Tuple[str, int]] = [
            (self.lview_combos.model().data(index, qtc.Qt.DisplayRole), index.row())
            for index in selected_indexes
        ]

        # Remove selected items from the left list view model
        for item, _ in selected_items:
            self.lview_combos.model().remove_item_by_value(item)

        # Clear selection after removal so that no stale selection remains
        self.lview_combos.clearSelection()

        # Emit layoutChanged to force the view to update
        self.lview_combos.model().layoutChanged.emit()

        # Add selected items to the right list view model and sort them
        self.lview_selectedCombos.model().add_items(selected_items)
        self.lview_selectedCombos.model().sort_items_by_original_order()

        # Update indices of both list models if needed
        self.lview_combos_listIndices = self.lview_combos.model().get_items_with_indices()
        self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()

    def move_left(self) -> None:
        """
        Move selected items from the right list view back to the left list view.
        """
        # Get selected items from the right list view (sorted in reverse order)
        selected_indexes = sorted(
            self.lview_selectedCombos.selectionModel().selectedIndexes(),
            key=lambda idx: idx.row(),
            reverse=True
        )
        selected_items: List[Tuple[str, int]] = [
            (self.lview_selectedCombos.model().data(index, qtc.Qt.DisplayRole), index.row())
            for index in selected_indexes
        ]

        # Remove selected items from the right list view model
        for item, _ in selected_items:
            self.lview_selectedCombos.model().remove_item_by_value(item)

        # Clear selection in the right list view
        self.lview_selectedCombos.clearSelection()

        # Emit layoutChanged for the right list view model
        self.lview_selectedCombos.model().layoutChanged.emit()

        # Add these items back to the left list view model and sort by original order
        self.lview_combos.model().add_items(selected_items)
        self.lview_combos.model().sort_items_by_original_order()

        # Update indices of both models
        self.lview_combos_listIndices = self.lview_combos.model().get_items_with_indices()
        self.lview_selectedCombos_listIndices = self.lview_selectedCombos.model().get_items_with_indices()

    def on_ok_clicked(self):
        """
        Called when OK is clicked. Updates the database with the selected load combos.
        """
        # Update the lists from the list models
        self.unique_combos = self.lview_combos.model().get_string_list()
        self.selected_combos = self.lview_selectedCombos.model().get_string_list()

        # Call service to update the database
        self.loadCombos_service.update_load_combo_selections(self.unique_combos, self.selected_combos)

        total = len(self.unique_combos) + len(self.selected_combos)
        selected_count = len(self.selected_combos)
        qtw.QMessageBox.information(self, "Notifications", f"{selected_count}/{total} selected!")
        self.accept()

    def print_current_state(self):
        print("Unique Combos:")
        print(self.lview_combos.model().stringList())
        print("Selected Combos:")
        print(self.lview_selectedCombos.model().stringList())
