
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from dependency_injector.wiring import inject

from sp_editor.services.groupLevel_service import GroupLevelService
from sp_editor.widgets.levelgroup_dialog import Ui_group_dialog


class GroupLevelController(qtw.QDialog, Ui_group_dialog):
    infor_updated = qtc.Signal(str)

    @inject
    def __init__(self, groupLevel_service: GroupLevelService):
        super().__init__()
        self.groupLevel_service = groupLevel_service

        # UI setup
        self.setupUi(self)
        self.selected_levels = []
        self.all_levels = []
        self.all_tiers = []
        self.pier_names = []

    def get_groupLevel_infor_and_display(self):
        """Initialize the dialog's UI and load data."""
        self.load_data()

        self.lview_storyName.selectionModel().selectionChanged.connect(
            self.update_selected_levels
        )
        self.pb_addGroup.clicked.connect(self.add_tier)
        self.pb_cancel.clicked.connect(self.cancel_changes)
        self.pb_OK.clicked.connect(self.confirm_changes)

        # Setup context menu for tier list view
        self.lview_groupName.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.lview_groupName.customContextMenuRequested.connect(
            self.show_tier_context_menu
        )

    def load_data(self):
        """Load levels and tiers into the UI."""
        all_levels = self.groupLevel_service.get_all_levels()
        self.all_tiers = self.groupLevel_service.get_all_tier_names()
        # get levels with tiers
        level_with_tiers = self.groupLevel_service.get_levels_with_tiers()

        # filter level to only include those without tiers
        self.all_levels = [
            level.story for level in all_levels if level.story not in level_with_tiers
        ]

        self.update_level_view()
        self.update_tier_view()

    def update_level_view(self):
        """Update the level list view."""
        level_model = qtc.QStringListModel(self.all_levels)
        self.lview_storyName.setModel(level_model)

    def update_tier_view(self):
        """Update the tier list view."""
        tier_model = qtc.QStringListModel(self.all_tiers)
        self.lview_groupName.setModel(tier_model)

    @qtc.Slot()
    def update_selected_levels(self):
        """Update selected levels."""
        indexes = self.lview_storyName.selectionModel().selectedIndexes()
        self.selected_levels = [index.data() for index in indexes]

        # get pier label based on a selected story
        self.pier_names = self.groupLevel_service.get_piers_by_levels(
            self.selected_levels
        )
        pier_model = qtc.QStringListModel(self.pier_names)
        self.lview_pierName.setModel(pier_model)

    @qtc.Slot()
    def add_tier(self):
        """Add a new tier to the selected levels."""
        tier_name = self.le_groupName.text().strip()
        if not tier_name or not self.selected_levels:
            qtw.QMessageBox.warning(
                self, "Warning", "Tier Name and Selected Levels cannot be empty."
            )
            return

        self.groupLevel_service.add_tier_to_levels(self.selected_levels, tier_name)

        self.all_tiers = self.groupLevel_service.get_all_tier_names()

        all_levels = self.groupLevel_service.get_all_levels()
        levels_with_tiers = self.groupLevel_service.get_levels_with_tiers()
        self.all_levels = [
            level.story for level in all_levels if level.story not in levels_with_tiers
        ]

        self.update_tier_view()
        self.update_level_view()

        # Clear the selected levels after adding the tier
        self.selected_levels = []
        self.lview_storyName.selectionModel().selectionChanged.connect(
            self.update_selected_levels
        )

    @qtc.Slot()
    def cancel_changes(self):
        """Cancel changes and close the dialog."""
        self.infor_updated.emit("Changes Cancelled")
        self.close()

    @qtc.Slot()
    def confirm_changes(self):
        """Confirm changes and close the dialog."""
        self.infor_updated.emit("Changes Confirmed")
        self.close()

    def show_tier_context_menu(self, position):
        """Show a context menu for tier list view."""
        menu = qtw.QMenu()
        delete_action = menu.addAction("Delete Tier")
        delete_action.triggered.connect(self.delete_tier)
        menu.exec_(self.lview_groupName.viewport().mapToGlobal(position))

    @qtc.Slot()
    def delete_tier(self):
        """Delete the selected tier and return levels to story list view."""
        selected_indexes = self.lview_groupName.selectionModel().selectedIndexes()
        if not selected_indexes:
            qtw.QMessageBox.warning(self, "Warning", "No tier selected.")
            return

        tier_name = selected_indexes[0].data()
        self.groupLevel_service.remove_tier_from_levels(tier_name)

        self.all_tiers = self.groupLevel_service.get_all_tier_names()

        all_levels = self.groupLevel_service.get_all_levels()
        levels_with_tiers = self.groupLevel_service.get_levels_with_tiers()
        self.all_levels = [
            level.story for level in all_levels if level.story not in levels_with_tiers
        ]

        self.update_tier_view()
        self.update_level_view()

        self.lview_storyName.selectionModel().selectionChanged.connect(
            self.update_selected_levels
        )
