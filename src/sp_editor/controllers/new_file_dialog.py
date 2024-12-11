import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw

from sp_editor.crud.cr_barset import create_barset
from sp_editor.utils import get_new_filename

from sp_editor.widgets.generalInfor_dialog import Ui_d_GeneralInfor

from sqlalchemy.engine.base import Engine
from sp_editor.core.global_variables import (
    DesignCode,
    BarGroupType,
    UnitSystem,
    ConfinementType,
    SectionCapacityMethod,
)
from sp_editor.crud.cr_general_infor import create_infor
from sp_editor.database.database import create_db_and_tables


class NewFile_Dialog(qtw.QDialog, Ui_d_GeneralInfor):
    engine_new = qtc.Signal(Engine)
    path_new = qtc.Signal(str)

    def __init__(self, parent: qtw.QMainWindow | None = None):
        super().__init__()
        self.engine = None
        self.dialog_new_path = None
        self.parent = parent

        self.setupUi(self)

        self.cb_DesignCode.clear()
        self.cb_DesignCode.addItems(list(str(code) for code in DesignCode))
        self.cb_UnitSystem.clear()
        self.cb_UnitSystem.addItems(list(str(us) for us in UnitSystem))
        self.cb_BarSet.clear()
        self.cb_BarSet.addItems(list(str(barset) for barset in BarGroupType))
        self.cb_Confinement.clear()
        self.cb_Confinement.addItems(list(str(cf) for cf in ConfinementType))
        self.cb_SectionCapacity.clear()
        self.cb_SectionCapacity.addItems(list(str(sc) for sc in SectionCapacityMethod))

        self.pb_Cancel.clicked.connect(self.close)
        self.pb_OK.clicked.connect(self.new_file_general_infor)

    @qtc.Slot()
    def new_file_general_infor(self):
        extensions = "sp_editor file (*.spe)"
        data_list = [
            self.cb_DesignCode.currentText(),
            self.cb_UnitSystem.currentText(),
            self.cb_BarSet.currentText(),
            self.cb_Confinement.currentText(),
            self.cb_SectionCapacity.currentText(),
        ]
        try:
            self.dialog_new_path = get_new_filename(extensions)

            if self.dialog_new_path:
                self.engine = create_db_and_tables(self.dialog_new_path)

                infor = create_infor(self.engine, data_list)
                barset = create_barset(self.engine, infor.bar_set)
                self.path_new.emit(self.dialog_new_path)
                self.engine_new.emit(self.engine)
                self.close()
            else:
                qtw.QMessageBox.warning(
                    self.parent,
                    "File not selected",
                    "No file was selected",
                    qtw.QMessageBox.Ok,
                )
        except FileNotFoundError:
            qtw.QMessageBox.warning(
                self.parent,
                "File not found",
                "No such file or directory",
                qtw.QMessageBox.Ok,
            )


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    new_file_dialog = NewFile_Dialog()
    new_file_dialog.show()
    sys.exit(app.exec())
