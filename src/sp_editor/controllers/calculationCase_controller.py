import os
import sys

from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6 import QtWidgets as qtw
from dependency_injector.wiring import inject, Provide

from sp_editor.containers.service_container import ServiceContainer
from sp_editor.core.connect_etabs import show_warning
from sp_editor.core.find_uniform_bars import plot_polygons
from sp_editor.core.global_variables import UnitSystem
from sp_editor.services.calculationCase_service import CalculationCaseService
from sp_editor.services.groupLevel_service import GroupLevelService
from sp_editor.services.rebar_service import RebarService
from sp_editor.widgets.load_calculation_case import Ui_calculationCase_dialog


class CalculationCaseController(qtw.QDialog, Ui_calculationCase_dialog):
    case_init = qtc.Signal(str)

    @inject
    def __init__(self,
                 rebar_service: RebarService = Provide[
                     ServiceContainer.rebar_service
                 ],
                 calculationCase_service: CalculationCaseService = Provide[
                     ServiceContainer.calculationCase_service
                 ],
                 groupLevel_service: GroupLevelService = Provide[
                     ServiceContainer.groupLevel_service
                 ]):
        super().__init__()

        self.current_unit = None
        self.material_Es = None
        self.material_Ec = None
        self.material_fy = None
        self.material_fc = None
        self.bar_spacing = None
        self.folder_name = None
        self.to_story = None
        self.from_story = None
        self.case_path = None
        self.current_path = None
        self.rho = None
        self.bar_no = None
        self.bar_area = None
        self.bar_cover = None
        self.sds_total_As = None
        self.concrete_Ag = None
        self.is_pier_name = False
        self.calculationCase_service = calculationCase_service
        self.groupLevel_service = groupLevel_service
        self.rebar_service = rebar_service

        self.level_list_model = None
        self.level_list = None
        self.groups_list = None
        self.sds_list = None

        self.sds_name = None
        self.tier_name = None
        self.pier_name = None

        # UI setup
        self.setupUi(self)

        # Initial load of all data

    def get_calculationCase_and_display(self):
        self.reload_data()
        # Connect UI signals
        self.cb_tier.currentTextChanged.connect(self.update_level_list)
        self.cb_tier.currentTextChanged.connect(self.update_pier_infor)
        self.cb_concrete.currentTextChanged.connect(
            lambda text: self.update_material_properties("concrete", self.cb_concrete.currentText())
        )
        self.cb_steel.currentTextChanged.connect(
            lambda text: self.update_material_properties("steel", self.cb_steel.currentText())
        )
        self.pb_makeSection.clicked.connect(self.make_section)
        self.pb_OK.clicked.connect(self.confirm_action)
        self.pb_Cancel.clicked.connect(self.cancel_action)

    def reload_data(self):
        """Fetches all necessary data from the database and updates the UI."""
        self.update_unit()
        self.update_group_box()
        self.update_section_designer_shape()
        self.update_materials()
        self.update_rebar_size()
        # self.update_level_list(self.cb_tier.currentText())
        self.update_pier_infor()
        self.update_material_properties("concrete", self.cb_concrete.currentText())
        self.update_material_properties("steel", self.cb_steel.currentText())

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
        self.tier_name = self.cb_tier.currentText()
        unique_piers = self.calculationCase_service.get_unique_pier_names_by_tier(self.tier_name)
        self.cb_pierdata.clear()
        self.cb_pierdata.addItems(unique_piers)

    def make_section(self):
        try:
            self.check_input()
            # defining necessary data for a creation section
            self.current_path = self.calculationCase_service.get_current_file_path()
            self.tier_name = self.cb_tier.currentText()
            self.pier_name = self.cb_pierdata.currentText()
            self.sds_name = self.cb_sectionDesignerShape.currentText()
            self.bar_no = self.cb_barSize.currentText()

            SDname = self.cb_sectionDesignerShape.currentText()
            # get bar area from selected bar number
            self.bar_area = self.calculationCase_service.get_rebar_area_by_size(self.bar_no)
            # get total rebar and rebar str for plotting
            (sds_total_bars, sds_rebar_list,
             offsetted_shapes, shape, rebar_list) = self.rebar_service.calculate_rebar_coordinates(
                self.bar_cover, self.bar_area, self.bar_spacing, SDname)
            # calling plotting function to display shape
            plot_polygons(self.f_3dview, offsetted_shapes, shape, rebar_list)

            # Calculate section properties
            self.concrete_Ag = self.calculationCase_service.get_SDS_properties(
                self.cb_sectionDesignerShape.currentText()
            )
            self.sds_total_As = round(self.bar_area * sds_total_bars, 2)
            self.rho = round((self.sds_total_As / self.concrete_Ag) * 100, 2)

            # display information into UI
            self.lb_quantities.setText(str(self.sds_total_As))
            self.lb_As.setText(str(self.sds_total_As))
            self.lb_Ag.setText(str(self.concrete_Ag))
            self.lb_Rho.setText(str(self.rho))

        except ValueError as ve:
            show_warning(f"ValueError in make_section: {ve}")
        except TypeError as te:
            show_warning(f"TypeError in make_section: {te}")
        except Exception as e:
            show_warning(f"Unexpected error in make_section: {e}")

    def confirm_action(self):
        try:
            self.create_folder()
            self.calculationCase_service.create_calculation_case(
                (self.tier_name, self.is_pier_name, self.folder_name, self.sds_name, self.pier_name,
                 self.bar_cover, self.bar_no, self.bar_area, self.bar_spacing,
                 self.concrete_Ag, self.sds_total_As, self.rho,
                 self.material_fc, self.material_fy, self.material_Ec, self.material_Es,
                 self.from_story, self.to_story, self.case_path)
            )
            self.case_init.emit(f"Calculation case for {self.tier_name} {self.pier_name} added")
            self.accept()
        except ValueError:
            show_warning("Can't create calculation case")
        except Exception as e:
            show_warning(f"Failed to create calculation case: {e}")

    def cancel_action(self):
        self.reject()

    def get_unique_items(self, items):
        return sorted(set(items))

    def get_top_and_bottom_level_of_tier(self):
        try:
            if not self.level_list:
                show_warning("<p>No level found. Please define your Tier first.<p>")
                return
            self.from_story = self.level_list[-1]
            self.to_story = self.level_list[0]
        except IndexError:
            show_warning("<p>No level found. Please define your Tier first.<p>")

    def check_input(self):
        status = qtg.Qt.CheckState.Checked
        if self.checkb_userPierName.checkState() == status:
            folder_name = self.cb_pierdata.currentText()
            self.is_pier_name = True
        else:
            folder_name = self.le_folderName.text()
            self.is_pier_name = False

        check_folder_name = {"Folder name": folder_name}

        check_material = {
            "fc": self.lb_fc.text(),
            "fy": self.lb_fy.text(),
            "Ec": self.lb_Ec.text(),
            "Es": self.lb_Es.text(),
        }
        check_geometry = {
            "Cover": self.le_cover.text(),
            "Spacing": self.le_spacing.text(),
        }
        for data_check in [check_folder_name, check_material, check_geometry]:
            for key, value in data_check.items():
                if not value:
                    error_message = (
                        f"<b>Failed to make section for display.<b> "
                        f"<p>PLease make sure: <p>"
                        f"<p> 1. Ensure you entered enough data <p>"
                        f"<p> Input data: {key} is missing.<p>"
                    )
                    show_warning(error_message)
                    raise ValueError
        try:
            self.folder_name = str(check_folder_name["Folder name"])
            self.bar_cover = float(check_geometry["Cover"])
            self.bar_spacing = float(check_geometry["Spacing"])
            self.material_fc = float(check_material["fc"])
            self.material_fy = float(check_material["fy"])
            self.material_Ec = float(check_material["Ec"])
            self.material_Es = float(check_material["Es"])
        except ValueError as e:
            error_message = (
                f"<b>Failed to make section for display.<b> "
                f"<p>Please make sure: <p>"
                f"<p>2. Ensure all numerical inputs are valid numbers.<p>"
                f"<p>Invalid data: {e}<p>"
            )
            show_warning(error_message)
            raise TypeError(f"Invalid data type: {e}")

    def update_unit(self):
        self.current_unit = self.calculationCase_service.get_current_unit()
        unit_area = "in2" if self.current_unit == str(UnitSystem.ENGLISH) else "mm2"
        self.lb_globalUnit.setText(self.current_unit)
        self.lb_unitArea.setText(unit_area)
        self.lb_unitAs.setText(unit_area)

    def create_folder(self):
        if self.current_path:
            # Extract the directory from the file path
            base_dir = os.path.dirname(self.current_path)

            if self.folder_name and self.tier_name:
                # Define the new folders to be created
                self.case_path = os.path.join(base_dir,self.tier_name, self.folder_name)
                self.case_path = os.path.normpath(self.case_path)
                try:
                    # Create the new directories
                    os.makedirs(self.case_path, exist_ok=True)
                except Exception as e:
                    qtw.QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')
            else:
                self.check_input()

        else:
            qtw.QMessageBox.warning(self, "No Input", "Please open a file first")
