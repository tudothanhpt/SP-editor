import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from sp_editor.widgets.load_calculation_case import Ui_calculationCase_dialog

from crud.cr_level_group import get_group_level, get_level_from_group, get_pierlabel_with_level
from crud.cr_load_case import get_sds_section_name, get_concrete_name, get_steel_name, get_rebar_size_name, \
    get_concrete_fc_Ec, get_steel_fy_Es, get_rebar_area_from_name

from sqlalchemy.engine.base import Engine


class CalculationCase_Dialog(qtw.QDialog, Ui_calculationCase_dialog):
    def __init__(self, engine: Engine | None = None, path: str | None = None, unit: str | None = None):
        super().__init__()
        self.bar_area = None
        self.concrete_list = None
        self.piers_list = None
        self.level_list = None
        self.sds_list = None
        self.groups_list = None
        self.engine = engine
        self.current_path = path
        self.current_unit = unit
        self.setupUi(self)

        self.update_group_box()
        self.update_section_designer_shape()
        self.update_concrete()
        self.update_steel()
        self.update_rebar_size()

        self.cb_tier.currentTextChanged.connect(self.update_level_list)
        self.cb_tier.currentTextChanged.connect(self.update_pier_infor)
        self.cb_concrete.currentTextChanged.connect(self.update_data_from_concrete)
        self.cb_steel.currentTextChanged.connect(self.update_data_from_steel)

        self.pb_makeSection.clicked.connect(self.make_section)

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
    def update_level_list(self):
        # TODO: get level list based on selected tier
        self.level_list = get_level_from_group(self.engine, self.cb_tier.currentText())
        self.level_list_model = qtc.QStringListModel()
        self.level_list_model.setStringList(self.level_list)
        self.lview_level.setModel(self.level_list_model)

    @qtc.Slot()
    def update_concrete(self):
        self.concrete_list = get_concrete_name(self.engine)
        self.cb_concrete.clear()
        self.cb_concrete.addItems(self.concrete_list)

    @qtc.Slot()
    def update_data_from_concrete(self):
        self.concrete_fc, self.concrete_Ec = get_concrete_fc_Ec(self.engine, self.cb_concrete.currentText())
        self.lb_fc.setText(str(self.concrete_fc))
        self.lb_Ec.setText(str(self.concrete_Ec))

    @qtc.Slot()
    def update_steel(self):
        # TODO: get fy from material database and display into combobox
        self.steel_list = get_steel_name(self.engine)
        self.cb_steel.clear()
        self.cb_steel.addItems(self.steel_list)

    @qtc.Slot()
    def update_data_from_steel(self):
        self.concrete_fy, self.concrete_Es = get_steel_fy_Es(self.engine, self.cb_steel.currentText())
        self.lb_fy.setText(str(self.concrete_fy))
        self.lb_Es.setText(str(self.concrete_Es))

    @qtc.Slot()
    def update_rebar_size(self):
        # TODO: get rebar size from rebar database and display into combobox
        self.rebar_list = get_rebar_size_name(self.engine)
        self.cb_barSize.clear()
        self.cb_barSize.addItems(self.rebar_list)

    @qtc.Slot()
    def update_pier_infor(self):
        # TODO: get pier infor from selected tier from database and display into listview
        self.piers_list = get_pierlabel_with_level(self.engine, self.level_list)
        pier_names_unique = self.get_unique_items(self.piers_list)
        self.cb_pierdata.clear()
        self.cb_pierdata.addItems(pier_names_unique)

    @qtc.Slot()
    def make_section(self):
        # TODO: make section from provided information then display 2D view of the section
        #  and calculated properties then display into widget

        self.check_input()

    @qtc.Slot()
    def create_folder(self):
        # TODO: Folder outer will be tier's name, folder inner will be
        #  pier's name(section desinger shape's name)
        pass

    @qtc.Slot()
    def confirm_action(self):
        pass

    @qtc.Slot()
    def cacel_all_action(self):
        pass

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
        if self.cb_barSize.currentIndex() == 0:
            self.bar_area = get_rebar_area_from_name(self.engine, self.cb_barSize.currentText())
        else:
            self.bar_area = self.le_barArea.text()

    def check_input(self):
        data_check = [self.lb_fc.text(), self.lb_fy.text(),
                      self.lb_Ec.text(), self.lb_Es.text(),

                      ]


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    calculation_case_dialog = CalculationCase_Dialog()
    calculation_case_dialog.show()
    sys.exit(app.exec())
