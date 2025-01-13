from PySide6 import QtWidgets as qtw
from PySide6.QtWidgets import QMessageBox
from dependency_injector.wiring import inject, Provide

from sp_editor.containers.service_container import ServiceContainer
from sp_editor.models.models import MaterialConcrete, MaterialRebar
from sp_editor.models.pandas_table_model import PandasModel
from sp_editor.services.material_service import MaterialService
from sp_editor.widgets.material_dialog import Ui_d_material


class MaterialController(qtw.QDialog, Ui_d_material):
    @inject
    def __init__(
        self,
        material_service: MaterialService = Provide[ServiceContainer.material_service],
    ):
        super().__init__()

        self.setupUi(self)
        self.material_service = material_service

        self.active_material = "Concrete"  # Default to Concrete tab

    def initialize_ui(self):
        """
        Initialize UI components and connect signals to slots.
        """
        # Connect signals to slots
        self.pb_load.clicked.connect(self.load_material_data)
        self.tabWidget.currentChanged.connect(self.update_active_material)

        # # Set up table views for both tabs
        self.concrete_table_view = self.tbview_concrete
        self.concrete_table_view.setAlternatingRowColors(True)
        self.concrete_table_view.horizontalHeader().setStretchLastSection(True)
        self.concrete_table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        #
        self.steel_table_view = self.tbview_steel
        self.steel_table_view.setAlternatingRowColors(True)
        self.steel_table_view.horizontalHeader().setStretchLastSection(True)
        self.steel_table_view.setSelectionBehavior(qtw.QTableView.SelectRows)

    def update_active_material(self, index: int):
        """
        Update the active material based on the selected tab.
        :param index: Tab index (0 for Concrete, 1 for Steel).
        """
        self.active_material = "Concrete" if index == 0 else "Steel"

    def load_material_data(self):
        """
        Load material data based on the active tab and populate the table.
        """
        try:
            # Determine the material type and corresponding SQLModel class
            material_type = (
                "concrete" if self.active_material == "Concrete" else "rebar"
            )
            material_class = (
                MaterialConcrete if material_type == "concrete" else MaterialRebar
            )

            # Get the material path
            material_path = self.material_service.material_list(material_type)
            if not material_path:
                QMessageBox.warning(
                    self, "Error", f"Material path not found for {material_type}."
                )
                return

            # Ask the user to select a JSON file
            json_path, _ = qtw.QFileDialog.getOpenFileName(
                self, "Select Material File", material_path, "JSON Files (*.json)"
            )
            if not json_path:
                return

            # Load the material data into the database
            self.material_service.load_material_from_file(json_path, material_class)

            # Fetch all materials and display them in the corresponding table
            data = self.material_service.get_all_materials(material_class)
            self.populate_table(data, material_type)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def populate_table(self, data, material_type: str):
        """
        Populate the table view for the active material using PandasModel.
        :param data: A pandas DataFrame of material data.
        :param material_type: The material type ("concrete" or "rebar").
        """
        model = PandasModel(data)

        if material_type == "concrete":
            self.concrete_table_view.setModel(model)
        elif material_type == "rebar":
            self.steel_table_view.setModel(model)
