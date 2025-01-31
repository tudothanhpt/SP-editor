import os
import sys

from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6 import QtWidgets as qtw

from sp_editor.core.connect_etabs import show_warning
from sp_editor.core.global_variables import UnitSystem
from sp_editor.services.calculationCase_service import CalculationCaseService
from sp_editor.services.groupLevel_service import GroupLevelService
from sp_editor.services.rebar_service import RebarService
from sp_editor.widgets.load_calculation_case import Ui_calculationCase_dialog


class CalculationCaseController(qtw.QDialog, Ui_calculationCase_dialog):
    def __init__(self, rebar_service: RebarService,
                 calculationCase_service: CalculationCaseService,
                 groupLevel_service: GroupLevelService):
        super().__init__()

        self.calculationCase_service = calculationCase_service
        self.groupLevel_service = groupLevel_service
        self.rebar_service = rebar_service

        self.level_list_model = None
        self.level_list = None
        self.groups_list = None
        self.sds_list = None

        # UI setup
        self.setupUi(self)

        self.reload_data()  # Initial load of all data

        # Connect UI signals
        self.cb_tier.currentTextChanged.connect(self.update_level_list)
        self.cb_tier.currentTextChanged.connect(
            lambda text: self.update_pier_infor(text, self.level_list)
        )
        self.cb_concrete.currentTextChanged.connect(self.update_data_from_concrete)
        self.cb_steel.currentTextChanged.connect(self.update_data_from_steel)
        self.pb_makeSection.clicked.connect(self.make_section)
        self.pb_OK.clicked.connect(self.confirm_action)
        self.pb_Cancel.clicked.connect(self.cancel_action)

    def reload_data(self):
        """Fetches all necessary data from the database and updates the UI."""
        self.update_unit()
        self.update_group_box()
        self.update_section_designer_shape()
        self.update_concrete()
        self.update_steel()
        self.update_rebar_size()
        self.update_level_list(self.cb_tier.currentText())
        self.update_pier_infor()
        self.update_data_from_concrete(self.cb_concrete.currentText())
        self.update_data_from_steel(self.cb_steel.currentText())

    def update_group_box(self):
        unique_tiers = self.groupLevel_service.get_all_distinct_tiers()
        self.cb_tier.clear()
        self.cb_tier.addItems(unique_tiers)

    def update_section_designer_shape(self):
        unique_sds = self.calculationCase_service.get_all_sds_sections()
        self.cb_sectionDesignerShape.clear()
        self.cb_sectionDesignerShape.addItems(unique_sds)

    def update_level_list(self, tier_name):
        self.level_list = self.groupLevel_service.get_levels_by_tier(tier_name)
        self.get_top_and_bottom_level_of_tier()
        self.level_list_model = qtc.QStringListModel()
        self.level_list_model.setStringList(self.level_list)
        self.lview_level.setModel(self.level_list_model)

    def update_materials(self):
        """
        Update both concrete and steel material dropdowns at once.
        """
        concrete_list, steel_list = self.calculationCase_service.get_all_material_names()

        # Update Concrete Dropdown
        self.cb_concrete.clear()
        self.cb_concrete.addItems(concrete_list)

        # Update Steel Dropdown
        self.cb_steel.clear()
        self.cb_steel.addItems(steel_list)

    def update_material_properties(self, material_type: str, material_name: str):
        """
        Update material properties (Concrete or Steel) based on the selected material name.

        :param material_type: Type of material ("concrete" or "steel").
        :param material_name: Selected material name.
        """
        if material_type == "concrete":
            concrete_fc, concrete_Ec = self.calculationCase_service.get_concrete_properties(material_name)

            if concrete_fc is None or concrete_Ec is None:
                qtw.QMessageBox.critical(self, "Error", "Failed to retrieve concrete properties.")
            else:
                self.lb_fc.setText(str(concrete_fc))
                self.lb_Ec.setText(str(concrete_Ec))

        elif material_type == "steel":
            steel_fy, steel_Es = self.calculationCase_service.get_steel_properties(material_name)

            if steel_fy is None or steel_Es is None:
                qtw.QMessageBox.critical(self, "Error", "Failed to retrieve steel properties.")
            else:
                self.lb_fy.setText(str(steel_fy))
                self.lb_Es.setText(str(steel_Es))

        else:
            qtw.QMessageBox.critical(self, "Error", "Invalid material type.")

    def update_rebar_size(self):
        rebar_list = self.calculationCase_service.get_rebar_size_name()
        self.cb_barSize.clear()
        self.cb_barSize.addItems(rebar_list)

    def update_pier_infor(self):
        unique_piers = self.calculationCase_service.get_unique_pier_names_by_tier(self.level_list)
        self.cb_pierdata.clear()
        self.cb_pierdata.addItems(unique_piers)

    def make_section(self):
        try:
            self.check_input()
            cover = self.le_cover.text()
            spacing = self.le_spacing.text()
            SDname = self.cb_sectionDesignerShape.currentText()
            # get bar area from selected bar number
            bar_area = self.calculationCase_service.get_rebar_area_by_size(self.cb_barSize.currentText())
            # get total rebar and rebar str for plotting
            total_rebar, rebar_str = self.rebar_service.calculate_rebar_coordinates(cover, bar_area, spacing, SDname)
            # calling plotting function to display shape

            # TODO: Section desinger shape and total_rebar to calculate this
            concrete_Ag, sds_total_As, rho = self.calculationCase_service.get_SDS_properties(
                self.cb_sectionDesignerShape.currentText()
            )

            self.lb_quantities.setText(str(sds_total_As))
            self.lb_As.setText(str(sds_total_As))
            self.lb_Ag.setText(str(concrete_Ag))
            self.lb_Rho.setText(str(rho))

        except ValueError as ve:
            show_warning(f"ValueError in make_section: {ve}")
        except TypeError as te:
            show_warning(f"TypeError in make_section: {te}")

    def confirm_action(self):
        try:
            self.create_folder()
            self.calculation_case = self.calculationCase_service.add_calculation_case(
                self.tier_name, self.folder_name, self.sds_name, self.pier_name,
                self.bar_cover, self.bar_no, self.bar_area, self.bar_spacing,
                self.concrete_Ag, self.sds_total_As, self.rho,
                self.material_fc, self.material_fy, self.material_Ec, self.material_Es,
                self.from_story, self.to_story, self.case_path
            )
            self.case_init.emit(f"Calculation case for {self.tier_name} {self.pier_name} added")
            self.accept()
        except ValueError:
            show_warning("Can't create calculation case")

    def cancel_action(self):
        self.reject()

    def get_unique_items(self, items):
        return sorted(set(items))

    def get_top_and_bottom_level_of_tier(self):
        try:
            self.from_story = self.level_list[-1]
            self.to_story = self.level_list[0]
        except IndexError:
            show_warning("<p>No level found. Please define your Tier first.<p>")

    def check_input(self):
        required_fields = {
            "Folder Name": self.le_folderName.text(),
            "Cover": self.le_cover.text(),
            "Spacing": self.le_spacing.text(),
            "fc": self.lb_fc.text(),
            "fy": self.lb_fy.text(),
            "Ec": self.lb_Ec.text(),
            "Es": self.lb_Es.text(),
        }

        for key, value in required_fields.items():
            if not value:
                show_warning(f"Missing required input: {key}")
                raise ValueError(f"Missing value for {key}")

    def update_unit(self):
        self.current_unit = self.calculationCase_service.get_current_unit()
        unit_area = "in2" if self.current_unit == str(UnitSystem.ENGLISH) else "mm2"
        self.lb_globalUnit.setText(self.current_unit)
        self.lb_unitArea.setText(unit_area)
        self.lb_unitAs.setText(unit_area)
