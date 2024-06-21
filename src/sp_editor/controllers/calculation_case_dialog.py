import os
import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from crud.cr_SD_shape import read_area
from sp_editor.widgets.load_calculation_case import Ui_calculationCase_dialog

from crud.cr_level_group import get_group_level, get_level_from_group, get_pierlabel_with_level
from crud.cr_load_case import get_sds_section_name, get_concrete_name, get_steel_name, get_rebar_size_name, \
    get_concrete_fc_Ec, get_steel_fy_Es, get_rebar_area_from_name

from core.connect_etabs import show_warning
from core.find_uniform_bars import get_rebarCoordinates_str

from sqlalchemy.engine.base import Engine


class CalculationCase_Dialog(qtw.QDialog, Ui_calculationCase_dialog):
    def __init__(self, engine: Engine | None = None, path: str | None = None, unit: str | None = None):
        super().__init__()
        self.tier_name = None
        self.folder_name = None
        self.sds_name = None
        self.pier_name = None
        self.concrete_Ag = None
        self.bar_area = None
        self.bar_cover = None
        self.bar_spacing = None
        self.material_fc = None
        self.material_fy = None
        self.material_Ec = None
        self.material_Es = None
        self.to_level = None
        self.from_level = None

        self.sds_rebar_list = None
        self.sds_total_bars = None
        self.rho = None

        self.concrete_list = None
        self.piers_list = None
        self.level_list = None
        self.sds_list = None
        self.groups_list = None

        self.engine = engine
        self.current_path = path
        self.current_unit = unit
        self.base_dir = None
        self.case_dir_name = None
        self.case_path = None

        self.setupUi(self)

        self.update_group_box()
        self.update_section_designer_shape()
        self.update_concrete()
        self.update_steel()
        self.update_rebar_size()

        self.cb_tier.currentTextChanged.connect(self.update_level_list)
        self.cb_tier.currentTextChanged.connect(lambda text: self.update_pier_infor(text, self.level_list))
        self.cb_concrete.currentTextChanged.connect(self.update_data_from_concrete)
        self.cb_steel.currentTextChanged.connect(self.update_data_from_steel)

        self.pb_makeSection.clicked.connect(self.make_section)

        self.pb_OK.clicked.connect(self.confirm_action)
        self.pb_Cancel.clicked.connect(self.cacel_all_action)

        # Manually trigger the slot for the initial current text
        self.update_level_list(self.cb_tier.currentText())
        self.update_pier_infor(self.cb_tier.currentText(), self.level_list)
        self.update_data_from_concrete(self.cb_concrete.currentText())
        self.update_data_from_steel(self.cb_steel.currentText())

    @qtc.Slot()
    def update_group_box(self):
        self.groups_list = get_group_level(self.engine, empty_tier=True)
        # using function to make list unique
        tier_names_unique = self.get_unique_items(self.groups_list)
        # display group into Tier combo box
        self.cb_tier.clear()
        self.cb_tier.addItems(tier_names_unique)

    @qtc.Slot()
    def update_section_designer_shape(self):
        # TODO: get section designer shape from database and display into combobox
        self.sds_list = get_sds_section_name(self.engine)
        # using function to make list unique
        sds_names_unique = self.get_unique_items(self.sds_list)
        self.cb_sectionDesignerShape.clear()
        self.cb_sectionDesignerShape.addItems(sds_names_unique)

    @qtc.Slot()
    def update_level_list(self, text):
        # TODO: get level list based on selected tier
        self.level_list = get_level_from_group(self.engine, text)
        self.get_top_and_bottom_level_of_tier()

        self.level_list_model = qtc.QStringListModel()
        self.level_list_model.setStringList(self.level_list)
        self.lview_level.setModel(self.level_list_model)

    @qtc.Slot()
    def update_concrete(self):
        self.concrete_list = get_concrete_name(self.engine)
        self.cb_concrete.clear()
        self.cb_concrete.addItems(self.concrete_list)

    @qtc.Slot()
    def update_data_from_concrete(self, text: str):
        self.concrete_fc, self.concrete_Ec = get_concrete_fc_Ec(self.engine, text)
        self.lb_fc.setText(str(self.concrete_fc))
        self.lb_Ec.setText(str(self.concrete_Ec))

    @qtc.Slot()
    def update_steel(self):
        # TODO: get fy from material database and display into combobox
        self.steel_list = get_steel_name(self.engine)
        self.cb_steel.clear()
        self.cb_steel.addItems(self.steel_list)
        self.cb_steel.setCurrentIndex(0)

    @qtc.Slot()
    def update_data_from_steel(self, text: str):
        self.concrete_fy, self.concrete_Es = get_steel_fy_Es(self.engine, text)
        self.lb_fy.setText(str(self.concrete_fy))
        self.lb_Es.setText(str(self.concrete_Es))

    @qtc.Slot()
    def update_rebar_size(self):
        # TODO: get rebar size from rebar database and display into combobox
        self.rebar_list = get_rebar_size_name(self.engine)
        self.cb_barSize.clear()
        self.cb_barSize.addItems(self.rebar_list)

    @qtc.Slot()
    def update_pier_infor(self, text: str, level):
        # TODO: get pier infor from selected tier from database and display into listview
        self.piers_list = get_pierlabel_with_level(self.engine, level)
        pier_names_unique = self.get_unique_items(self.piers_list)
        self.cb_pierdata.clear()
        self.cb_pierdata.addItems(pier_names_unique)

    @qtc.Slot()
    def make_section(self):
        try:
            # TODO: make section from provided information then display 2D view of the section
            #  and calculated properties then display into widget
            # check data input from user only check if any need data is None
            self.check_input()
            # get bar area from UI
            self.bar_area = self.get_bar_area()
            # get all other data need
            self.get_data_for_plot()
            # plot function
            self.sds_total_bars, self.sds_rebar_list = get_rebarCoordinates_str(self.f_3dview, self.engine,
                                                                                self.bar_cover, self.bar_area,
                                                                                self.bar_spacing, self.sds_name)

            self.concrete_Ag = round(read_area(self.engine, self.sds_name), 2)
            self.sds_total_As = round(self.bar_area * self.sds_total_bars, 2)
            self.rho = round((self.sds_total_As / self.concrete_Ag) * 100, 2)

            self.lb_quantities.setText(str(self.sds_total_bars))
            self.lb_As.setText(str(self.sds_total_As))
            self.lb_Ag.setText(str(self.concrete_Ag))
            self.lb_Rho.setText(str(self.rho))

        except ValueError as ve:
            # Handle missing value error
            print(f"ValueError in make_section: {ve}")
        except TypeError as te:
            # Handle type error
            print(f"TypeError in make_section: {te}")

    @qtc.Slot()
    def create_folder(self):
        if self.current_path:
            # Extract the directory from the file path
            self.base_dir = os.path.dirname(self.current_path)

            if self.folder_name and self.tier_name:
                # Define the new folders to be created
                self.case_dir_name = [self.tier_name, self.folder_name]

                self.case_path = os.path.join(self.base_dir, *self.case_dir_name)
                try:
                    # Create the new directories
                    os.makedirs(self.case_path, exist_ok=True)
                except Exception as e:
                    qtw.QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')
            else:
                self.check_input()

        else:
            qtw.QMessageBox.warning(self, 'No Input', 'Please open a file first')

    @qtc.Slot()
    def confirm_action(self):
        self.create_folder()

    @qtc.Slot()
    def cacel_all_action(self):
        self.close()

    @qtc.Slot()
    def get_unique_items(self, items):
        # Remove duplicates while preserving order
        unique_items = []
        seen = set()
        for item in items:
            if item not in seen:
                unique_items.append(item)
                seen.add(item)
        return unique_items

    def get_bar_area(self):
        if self.cb_barType.currentIndex() == 0:
            self.bar_area = get_rebar_area_from_name(self.engine, self.cb_barSize.currentText())
        else:
            self.bar_area = self.le_barArea.text()
            if float(self.bar_area) < 0:
                error_message = f"Area must be a positive number"
                show_warning(error_message)
        return float(self.bar_area)

    @qtc.Slot()
    def get_top_and_bottom_level_of_tier(self):
        self.from_level = self.level_list[-1]
        self.to_level = self.level_list[0]
        print(self.level_list)

    def check_input(self):
        status = qtg.Qt.CheckState.Checked
        if self.checkb_userPierName.checkState() == status:
            folder_name = self.cb_pierdata.currentText()
        else:
            folder_name = self.le_folderName.text()

        check_folder_name = {"Folder name": folder_name}

        check_material = {"fc": self.lb_fc.text(),
                          "fy": self.lb_fy.text(),
                          "Ec": self.lb_Ec.text(),
                          "Es": self.lb_Es.text()}
        check_geometry = {
            "Cover": self.le_cover.text(),
            "Spacing": self.le_spacing.text(),
        }
        for data_check in [check_folder_name, check_material, check_geometry]:
            for key, value in data_check.items():
                if not value:
                    error_message = (f"<b>Failed to make section for display.<b> "
                                     f"<p>PLease make sure: <p>"
                                     f"<p> 1. Ensure you entered enough data <p>"
                                     f"<p> Input data: {key} is missing.<p>")
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
            error_message = (f"<b>Failed to make section for display.<b> "
                             f"<p>Please make sure: <p>"
                             f"<p>2. Ensure all numerical inputs are valid numbers.<p>"
                             f"<p>Invalid data: {e}<p>")
            show_warning(error_message)
            raise TypeError(f"Invalid data type: {e}")

    def get_data_for_plot(self):
        self.tier_name = self.cb_tier.currentText()
        self.pier_name = self.cb_pierdata.currentText()
        self.sds_name = self.cb_sectionDesignerShape.currentText()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    calculation_case_dialog = CalculationCase_Dialog()
    calculation_case_dialog.show()
    sys.exit(app.exec())
