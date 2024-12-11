import sys

import pandas as pd
import sqlalchemy
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from sqlalchemy.engine.base import Engine

from sp_editor.core.mainwindow_context_menu import TableContextMenu
from sp_editor.database.mainWindow_model import MainWindowModel
from sp_editor.controllers.barest_dialog import BarSet_Dialog
from sp_editor.controllers.calculation_case_dialog import CalculationCase_Dialog
from sp_editor.controllers.combos_dialog import Combo_Dialog
from sp_editor.controllers.cti_file_making_dialog import CTIMakingDialog
from sp_editor.controllers.general_infor_dialog import GeneralInfor_Dialog
from sp_editor.controllers.groups_dialog import Group_Dialog
from sp_editor.controllers.import_etabs_dialog import ImportEtabs_Dialog
from sp_editor.controllers.material_dialog import Material_Dialog
from sp_editor.controllers.new_file_dialog import NewFile_Dialog
from sp_editor.controllers.open_file_dialog import OpenFile_Dialog
from sp_editor.controllers.batch_processor_dialog import BatchProcessorDialog
from sp_editor.controllers.about_dialog import AboutDialog
from sp_editor.core.connect_etabs import (
    get_story_infor,
    get_pier_label_infor,
    get_pier_force_infor,
    get_loadCombo_df_fromE,
    get_section_designer_shape_infor,
    set_global_unit,
)
from sp_editor.core.force_filter import get_pierforces_CTI_todb
from sp_editor.crud.cr_SD_shape import get_SDCoordinates_CTI_todb
from sp_editor.crud.cr_level_group import (
    get_level_to_db,
    get_pier_label_to_db,
    get_pier_design_force_to_db,
    get_sds_to_db,
)
from sp_editor.crud.cr_load_combo import (
    create_loadComboDB,
    create_loadComboSelectionDB,
    read_loadComboSelectionDB,
)
from sp_editor.widgets.main_window import Ui_mw_Main


class MainWindow(qtw.QMainWindow, Ui_mw_Main):
    def __init__(self):
        super().__init__()
        self.dialog_load_combos_selection = None
        self.dialog_calculation_case = None
        self.dialog_group = None
        self.current_path = None
        self.dialog_barset = None
        self.dialog_import_etabs = None
        self.dialog_open = None
        self.dialog_new = None
        self.current_engine = None
        self.sap_model = None
        self.etabs_object = None
        self.dialog_material = None
        self.cti_making = None
        self.dialog_batch_processor = None
        self.main_window_model = None
        self.dialog_about = None

        self.setupUi(self)
        self.set_active_action(False)

        # setup context menu
        self.context_menu = TableContextMenu(
            self.table_sumaryResults, self.main_window_model
        )
        self.table_sumaryResults.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.table_sumaryResults.customContextMenuRequested.connect(
            self.open_context_menu
        )
        self.context_menu.modify_action_finished.connect(self.update_display_results)
        self.context_menu.add_copy_action_finished.connect(self.update_display_results)
        self.context_menu.delete_action_finished.connect(self.update_display_results)

        # Setup action
        self.action_New.triggered.connect(self.new_file)
        self.action_Open.triggered.connect(self.open_file)
        self.a_ImportEtabs.triggered.connect(self.open_import_etabs)
        self.a_GeneralInfor.triggered.connect(self.set_general_infor)
        self.a_BarSet.triggered.connect(self.open_barset)
        self.a_MaterialProp.triggered.connect(self.open_material)
        self.a_Groups.triggered.connect(self.open_groups)
        self.a_Cases.triggered.connect(self.open_calculation_cases)
        self.actionDesign_Combos_Selection.triggered.connect(
            self.open_loadComboSelection
        )
        self.a_GetAllForce.triggered.connect(self.get_all_force)
        self.a_MakeSPcolumn.triggered.connect(self.make_spcolumn)
        self.a_BatchProcessor.triggered.connect(self.batch_processor)
        self.a_About.triggered.connect(self.open_about)

    @qtc.Slot()
    def new_file(self):
        self.dialog_new = NewFile_Dialog(self)
        self.dialog_new.path_new.connect(self.update_message)
        self.dialog_new.path_new.connect(self.set_current_path)
        self.dialog_new.engine_new.connect(self.set_current_engine)
        self.set_active_action(True)
        self.dialog_new.exec()
        self.init_display_table()

    @qtc.Slot()
    def open_file(self):
        self.dialog_open = OpenFile_Dialog(self)
        self.dialog_open.path_open.connect(self.update_message)
        self.dialog_open.path_open.connect(self.set_current_path)
        self.dialog_open.engine_open.connect(self.set_current_engine)
        self.set_current_engine(self.dialog_open.engine)
        results = self.dialog_open.exec()
        self.init_display_table()
        try:
            self.update_display_results()
        except sqlalchemy.exc.OperationalError:
            print("no data in database")

        self.set_active_action(True)

    @qtc.Slot()
    def open_import_etabs(self):
        self.dialog_import_etabs = ImportEtabs_Dialog()
        self.dialog_import_etabs.attach_etabs()
        self.dialog_import_etabs.lb_ActiveModel.setText(
            self.dialog_import_etabs.SapModel.GetModelFilename(IncludePath=False)
        )
        self.dialog_import_etabs.exec()

        self.sap_model = self.dialog_import_etabs.SapModel
        self.etabs_object = self.dialog_import_etabs.EtabsObject

        # Set ETABS units = engine units
        set_global_unit(self.sap_model, self.current_engine)

        # TODO: add widget to get load combo and story infor pierlabel below
        # get story label from api and then put into database
        df_story = get_story_infor(self.sap_model, self.etabs_object)
        get_level_to_db(self.current_engine, df_story)
        # get pier label from api then put into database
        df_pier_label = get_pier_label_infor(self.sap_model, self.etabs_object)
        get_pier_label_to_db(self.current_engine, df_pier_label)
        # get section designer shape into db
        df_sds_shape = get_section_designer_shape_infor(
            self.sap_model, self.etabs_object
        )
        get_sds_to_db(self.current_engine, df_sds_shape)
        get_SDCoordinates_CTI_todb(self.current_engine)
        # get Load combination from API and then put into database
        df_LC, df_LCselection = get_loadCombo_df_fromE(self.sap_model)
        create_loadComboDB(self.current_engine, df_LC)
        create_loadComboSelectionDB(self.current_engine, df_LCselection)
        ##############################################
        self.dialog_import_etabs.connected_etabs.connect(self.update_message)
        self.dialog_import_etabs.connected_etabs.connect(
            self.a_ImportEtabs.setEnabled(False)
        )
        self.set_active_action_postEtabs(True)

    @qtc.Slot()
    def set_general_infor(self):
        self.dialog_new = GeneralInfor_Dialog(self.current_engine)
        self.dialog_new.infor_updated.connect(self.update_message)
        self.dialog_new.exec()

    @qtc.Slot()
    def open_material(self):
        self.dialog_material = Material_Dialog(self.current_engine)
        self.dialog_material.exec()

    @qtc.Slot()
    def open_barset(self):
        self.dialog_barset = BarSet_Dialog(self.current_engine, self.current_path)
        self.dialog_barset.exec()

    @qtc.Slot()
    def open_groups(self):
        self.dialog_group = Group_Dialog(self.current_engine, self.current_path)
        self.dialog_group.exec()

    @qtc.Slot()
    def open_calculation_cases(self):
        self.dialog_calculation_case = CalculationCase_Dialog(
            self.current_engine, self.current_path
        )
        self.dialog_calculation_case.case_init.connect(self.update_message)
        self.dialog_calculation_case.case_init.connect(self.update_display_results)
        self.dialog_calculation_case.exec()

    @qtc.Slot()
    def open_loadComboSelection(self):
        self.dialog_load_combos_selection = Combo_Dialog(self.current_engine)
        self.dialog_load_combos_selection.exec()
        self.a_GetAllForce.setEnabled(True)

    @qtc.Slot()
    def get_all_force(self):
        df_combo_selection = read_loadComboSelectionDB(self.current_engine)
        list_combo_selection = (
            df_combo_selection["selectedLoadCombos"].dropna().unique().tolist()
        )
        # get pier design force and then put into database
        df_pier_design_force = get_pier_force_infor(
            self.sap_model, self.etabs_object, list_combo_selection
        )
        get_pier_design_force_to_db(self.current_engine, df_pier_design_force)
        get_pierforces_CTI_todb(self.current_engine)

    @qtc.Slot()
    def make_spcolumn(self):
        self.cti_making = CTIMakingDialog(self.current_engine)
        self.cti_making.cti_create.connect(self.update_message)
        self.cti_making.cti_create.connect(self.update_display_results)
        self.cti_making.exec()

    @qtc.Slot()
    def batch_processor(self):
        self.dialog_batch_processor = BatchProcessorDialog(self.current_engine)
        self.dialog_batch_processor.read_results_create.connect(self.update_message)
        self.dialog_batch_processor.read_results_create.connect(
            self.update_display_results
        )
        self.dialog_batch_processor.exec()

    @qtc.Slot()
    def open_about(self):
        self.dialog_about = AboutDialog()
        self.dialog_about.exec()

    def init_display_table(self):
        # TODO: display infor from database
        column_headers = [
            "SPColumn File",
            "Tier",
            "From Story",
            "To Story",
            "Pier",
            "Material Fc",
            "Material Fy",
            "Bar No",
            "Rho",
            "DCR",
            "Force Combo",
        ]
        df = pd.DataFrame(columns=column_headers)
        self.main_window_model = MainWindowModel(dataframe=df)
        self.table_sumaryResults.setModel(self.main_window_model)

    @qtc.Slot()
    def update_display_results(self):
        # TODO: display infor from database
        self.main_window_model.update_model_from_db(self.current_engine)
        self.table_sumaryResults.resizeColumnsToContents()

    @qtc.Slot(Engine)
    def set_current_engine(self, engine: Engine):
        self.current_engine = engine

    @qtc.Slot(str)
    def update_message(self, message: str):
        self.statusbar.showMessage(message)

    @qtc.Slot(str)
    def set_current_path(self, path: str):
        self.current_path = path

    @qtc.Slot()
    def set_active_action(self, mode: bool):
        self.a_ImportEtabs.setEnabled(mode)
        self.a_GeneralInfor.setEnabled(mode)
        self.a_MaterialProp.setEnabled(mode)
        self.a_BarSet.setEnabled(mode)
        self.a_Groups.setEnabled(mode)
        self.a_Cases.setEnabled(mode)
        self.actionDesign_Combos_Selection.setEnabled(mode)
        self.a_GetAllForce.setEnabled(False)
        self.a_MakeSPcolumn.setEnabled(False)
        self.a_BatchProcessor.setEnabled(False)

    @qtc.Slot()
    def set_active_action_postEtabs(self, mode: bool):
        self.a_Groups.setEnabled(mode)
        self.a_Cases.setEnabled(mode)
        self.actionDesign_Combos_Selection.setEnabled(mode)
        self.a_GetAllForce.setEnabled(False)
        self.a_MakeSPcolumn.setEnabled(True)
        self.a_BatchProcessor.setEnabled(True)

    @qtc.Slot()
    def open_context_menu(self, position):
        self.context_menu.path = self.current_path
        self.context_menu.engine = self.current_engine
        self.context_menu.exec(
            self.table_sumaryResults.viewport().mapToGlobal(position)
        )


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
