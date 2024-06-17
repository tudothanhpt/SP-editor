import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from sp_editor.widgets.load_calculation_case import Ui_calculationCase_dialog

from crud.cr_level_group import get_group_level, get_level_from_group
from crud.cr_load_case import get_sds_section_name

from sqlalchemy.engine.base import Engine


class CalculationCase_Dialog(qtw.QDialog, Ui_calculationCase_dialog):
    def __init__(self, engine: Engine | None = None, path: str | None = None, unit: str | None = None):
        super().__init__()
        self.level_list = None
        self.sds_list = None
        self.groups_list = None
        self.engine = engine
        self.current_path = path
        self.current_unit = unit
        self.setupUi(self)

        self.update_group_box()
        self.update_section_designer_shape()
        self.cb_tier.currentTextChanged.connect(self.update_level_list)

    @qtc.Slot()
    def update_group_box(self):
        self.groups_list = get_group_level(self.engine, empty_tier=True)
        # using function to make list unique
        tier_names_unique = self.get_unique_items(self.groups_list)
        # display group into Tier combo box
        self.cb_tier.addItems(tier_names_unique)

    @qtc.Slot()
    def update_section_designer_shape(self):
        # TODO: get section designer shape from database and display into combobox
        self.sds_list = get_sds_section_name(self.engine)
        # using function to make list unique
        sds_names_unique = self.get_unique_items(self.sds_list)
        self.cb_sectionDesignerShape.addItems(sds_names_unique)

    @qtc.Slot()
    def update_level_list(self):
        # TODO: get level list based on selected tier
        self.level_list = get_level_from_group(self.engine, self.cb_tier.currentText())
        self.level_list_model = qtc.QStringListModel()
        self.level_list_model.setStringList(self.level_list)
        self.lview_level.setModel(self.level_list_model)

    @qtc.Slot()
    def update_concrete_fc(self):
        # TODO: get fc from material database and display into combobox
        pass

    @qtc.Slot()
    def update_steel_fy(self):
        # TODO: get fy from material database and display into combobox
        pass

    @qtc.Slot()
    def update_rebar_size(self):
        # TODO: get rebar size from rebar database and display into combobox
        pass

    @qtc.Slot()
    def update_level_infor(self):
        # TODO: get level infor from selected tier from database and display into listview
        pass

    @qtc.Slot()
    def update_pier_infor(self):
        # TODO: get pier infor from selected tier from database and display into listview
        pass

    @qtc.Slot()
    def create_folder(self):
        # TODO: Folder outer will be tier's name, folder inner will be
        #  pier's name(section desinger shape's name)
        pass

    @qtc.Slot()
    def make_section(self):
        # TODO: make section from provided information then display 2D view of the section
        #  and calculated properties then display into widget
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


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    calculation_case_dialog = CalculationCase_Dialog()
    calculation_case_dialog.show()
    sys.exit(app.exec())
