from dependency_injector.wiring import inject, Provide
from PySide6 import QtWidgets as qtw

from sp_editor.controllers.barSet_controller import BarSetController
from sp_editor.controllers.calculationCase_controller import CalculationCaseController
from sp_editor.controllers.etabsImport_controller import EtabsImportController
from sp_editor.controllers.generalInfor_controller import GeneralInforController
from sp_editor.controllers.groupLevel_controller import GroupLevelController
from sp_editor.controllers.loadCombos_controller import LoadCombosController
from sp_editor.controllers.material_controller import MaterialController
from sp_editor.controllers.newFile_controller import NewFileController
from sp_editor.controllers.openFile_controller import OpenFileController
from sp_editor.widgets.main_window import Ui_mw_Main


class MainWindowController(qtw.QMainWindow, Ui_mw_Main):
    @inject
    def __init__(
        self,
        newFileController: NewFileController = Provide[
            "AppContainer.newFileController"
        ],
        openFileController: OpenFileController = Provide[
            "AppContainer.openFileController"
        ],
        etabsImportController: EtabsImportController = Provide[
            "AppContainer.etabsImportController"
        ],
        generalInforController: GeneralInforController = Provide[
            "AppContainer.generalInforController"
        ],
        barsetController: BarSetController = Provide["AppContainer.barSetController"],
        materialController: MaterialController = Provide[
            "AppContainer.materialController"
        ],
        groupLevelController: GroupLevelController = Provide[
            "AppContainer.groupLevelController"
        ],
        calculationCaseController: CalculationCaseController = Provide[
                "AppContainer.calculationCaseController"
        ],
        loadCombosController:LoadCombosController = Provide[
            "AppContainer.loadCombosController"
        ]
    ):
        super().__init__()

        self.newFile_controller = newFileController
        self.openFile_controller = openFileController
        self.etabsImport_controller = etabsImportController
        self.generalInfor_controller = generalInforController
        self.barSet_controller = barsetController
        self.material_controller = materialController
        self.groupLevel_controller = groupLevelController
        self.calculationCase_controller = calculationCaseController
        self.loadCombos_controller = loadCombosController

        self.setupUi(self)

        # Setup action
        self.action_New.triggered.connect(self.new_file)
        self.action_Open.triggered.connect(self.open_file)
        self.a_ImportEtabs.triggered.connect(self.import_etabs)
        self.a_GeneralInfor.triggered.connect(self.edit_generalInfor)
        self.a_BarSet.triggered.connect(self.edit_barset)
        self.a_MaterialProp.triggered.connect(self.edit_material)
        self.a_Groups.triggered.connect(self.edit_group)
        self.a_Cases.triggered.connect(self.edit_calculationCase)
        self.actionDesign_Combos_Selection.triggered.connect(self.edit_loadCombosSelection)

    def new_file(self):
        self.newFile_controller.show()
        # self.newFile_controller.execute()

    def open_file(self):
        self.openFile_controller.execute()

    def import_etabs(self):
        self.etabsImport_controller.attach_to_instance()
        self.etabsImport_controller.show()

    def edit_generalInfor(self):
        self.generalInfor_controller.get_general_infor_and_display()
        self.generalInfor_controller.show()

    def edit_barset(self):
        self.barSet_controller.get_barset_and_display()
        self.barSet_controller.show()

    def edit_material(self):
        self.material_controller.initialize_ui()
        self.material_controller.show()

    def edit_group(self):
        self.groupLevel_controller.get_groupLevel_infor_and_display()
        self.groupLevel_controller.show()

    def edit_calculationCase(self):
        self.calculationCase_controller.get_calculationCase_and_display()
        self.calculationCase_controller.show()

    def edit_loadCombosSelection(self):
        self.loadCombos_controller.get_loadCombos_and_display()
        self.loadCombos_controller.show()
