import os
import sys

from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6 import QtWidgets as qtw
from sqlalchemy.engine.base import Engine

from controllers.calculation_case_dialog import CalculationCase_Dialog
from core.connect_etabs import show_warning
from core.find_uniform_bars import get_rebarCoordinates_str
from crud.cr_SD_shape import read_area
from crud.cr_level_group import get_group_level, get_level_from_group, get_pierlabel_with_level
from crud.cr_load_case import get_sds_section_name, get_concrete_name, get_steel_name, get_rebar_size_name, \
    get_concrete_fc_Ec, get_steel_fy_Es, get_rebar_area_from_name, create_calculation_case, get_current_unit, \
    update_calculation_case, get_concrete_name_from_properties, get_steel_name_from_properties
from sp_editor.core.global_variables import UnitSystem
from sp_editor.widgets.load_calculation_case import Ui_calculationCase_dialog


class CalculationCaseModify_Dialog(CalculationCase_Dialog):
    model_modify = qtc.Signal()

    def __init__(self, engine: Engine, path: str, data: list[str | float] = None, current_id=None, modify=False):
        super().__init__(engine, path)

        (id, tier, is_pier_name, folder, sds, pier, bar_cover, bar_no, bar_area, bar_spacing, concrete_ag, sds_as, rho,
         material_fc, material_fy, material_ec, material_es, from_story, to_story, case_path, sp_column_file,
         force_combo, dcr) = data
        self.engine = engine
        self.current_path = path

        self.current_id = current_id
        self.data = data
        self.modify = modify

        self.tier_name = tier
        self.is_pier_name = is_pier_name
        self.folder_name = folder
        self.sds_name = sds
        self.pier_name = pier
        self.concrete_Ag = concrete_ag
        self.sds_total_As = sds_as
        self.bar_no = bar_no
        self.bar_area = bar_area
        self.bar_cover = bar_cover
        self.bar_spacing = bar_spacing
        self.material_fc = material_fc
        self.material_fy = material_fy
        self.material_Ec = material_ec
        self.material_Es = material_es
        self.to_story = from_story
        self.from_story = to_story
        self.case_path = case_path

        self.concrete_name = get_concrete_name_from_properties(self.engine, self.material_fc, self.material_Ec)
        self.steel_name = get_steel_name_from_properties(self.engine, self.material_fy, self.material_Es)
        # Manually trigger the slot for the initial current text
        self.update_tier_name(self.tier_name)
        self.update_folder_name(self.is_pier_name, self.folder_name)
        self.update_level_list(self.tier_name)
        self.update_pier_infor(self.tier_name, self.level_list)
        self.update_data_from_concrete(self.concrete_name)
        self.update_data_from_steel(self.steel_name)
        self.update_rebar_and_cover(self.bar_spacing, self.bar_cover)
        self.make_section()

    def add_calculation_case(self):
        case = [self.tier_name, self.is_pier_name, self.folder_name, self.sds_name, self.pier_name,
                self.bar_cover, self.bar_no, self.bar_area, self.bar_spacing, self.concrete_Ag, self.sds_total_As,
                self.rho, self.material_fc, self.material_fy, self.material_Ec, self.material_Es,
                self.from_story, self.to_story,
                self.case_path]

        cal_case = update_calculation_case(self.engine, case, self.current_id)
        self.model_modify.emit()
        return cal_case

    def update_folder_name(self, is_pier_name, folder_name):
        if is_pier_name:
            status = qtg.Qt.CheckState.Checked

            self.checkb_userPierName.setCheckState(status)
        else:
            status = qtg.Qt.CheckState.Unchecked

            self.checkb_userPierName.setCheckState(status)
            self.le_folderName.setText(folder_name)

    def update_rebar_and_cover(self, bar_spacing, bar_cover):
        self.le_spacing.setText(str(bar_spacing))
        self.le_cover.setText(str(bar_cover))

    def update_tier_name(self, tier_name):
        self.cb_tier.setCurrentText(tier_name)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    calculation_case_modify_dialog = CalculationCase_Dialog()
    calculation_case_modify_dialog.show()
    sys.exit(app.exec())
