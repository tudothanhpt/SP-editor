
from PySide6 import QtWidgets as qtw
from dependency_injector.wiring import inject, Provide

from sp_editor.containers.service_container import ServiceContainer
from sp_editor.core.global_variables import BarGroupType
from sp_editor.models.pandas_table_model import PandasModel
from sp_editor.services.barset_service import BarsetService
from sp_editor.services.generalInfor_service import GeneralInforService
from sp_editor.widgets.barSet_dialog import Ui_d_BarSet


class BarSetController(qtw.QDialog, Ui_d_BarSet):
    @inject
    def __init__(
        self,
        generalInfor_service: GeneralInforService = Provide[
            ServiceContainer.generalInfor_service
        ],
        barset_service: BarsetService = Provide[ServiceContainer.barset_service],
    ):
        super().__init__()

        self.general_infor = None
        self.barset_infor = None
        self.barset_service = barset_service
        self.generalInfor_service = generalInfor_service

        self.setupUi(self)

    def get_barset_and_display(self):
        # getting current barset name and barset table infor in a database
        self.general_infor = self.generalInfor_service.get_generalInfor()

        self.barset_infor = self.barset_service.get_all_barset()

        # display current barset name
        self.cb_BarSetList.clear()
        self.cb_BarSetList.addItems(list(str(barset) for barset in BarGroupType))
        current_text = self.general_infor.bar_set
        self.cb_BarSetList.setCurrentText(current_text)
        self.display_df_model()

        self.cb_BarSetList.currentTextChanged.connect(self.on_text_changed)

    def on_text_changed(self):
        """
        Get barset from current text in combobox and then load it to the database and display to the table view
        """
        current_barset = self.cb_BarSetList.currentText()
        self.barset_service.load_barsets_from_file(current_barset)
        self.display_df_model()

    def display_df_model(self):
        current_barset = self.barset_service.get_all_barset()
        model = PandasModel(current_barset)
        self.tbview_BarSet.setModel(model)
