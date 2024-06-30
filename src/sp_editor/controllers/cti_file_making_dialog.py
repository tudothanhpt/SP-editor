import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
import pandas as pd

from sp_editor.crud.cr_mainwindow import update_path_after_creation, fetch_data_from_db
from sp_editor.widgets.cti_file_making_dialog_ui import Ui_cti_making_dialog
from sp_editor.core.cti_data_merging import read_summaryCTI_DB, create_cti_summary_df, CTI_creation_from_list

from sqlmodel import create_engine
from typing import *
from sqlalchemy.engine.base import Engine


class CTIMakingDialog(qtw.QDialog, Ui_cti_making_dialog):
    cti_create = qtc.Signal()

    def __init__(self, engine, parent: qtw.QWidget = None):
        super().__init__(parent)
        self.setupUi(self)
        self.engine = None

        try:
            self.engine = engine
            create_cti_summary_df(self.engine)

            self.df_summaryCTI = read_summaryCTI_DB(engine)
            items = self.df_summaryCTI["ID2"].unique().tolist()
        except Exception as e:
            items = []

        self.model = self.create_model(items)
        self.lview_availCTI.setModel(self.model)

        self.pb_makefile.clicked.connect(self.on_makeCTI_clicked)
        self.pb_selectall.clicked.connect(self.on_pb_selectall_clicked)

    def create_model(self, items):
        model = qtg.QStandardItemModel(self)
        for item_text in items:
            item = qtg.QStandardItem(item_text)
            item.setCheckable(True)
            item.setCheckState(qtc.Qt.CheckState.Unchecked)
            model.appendRow(item)
        return model

    def on_makeCTI_clicked(self):
        checked_items = []
        model = self.lview_availCTI.model()  # Get the model instance
        for row in range(model.rowCount()):
            item = model.item(row)
            if item.checkState() == qtc.Qt.CheckState.Checked:
                checked_items.append(item.text())

        if not checked_items:
            self.show_warning()
        else:
            lst_CTIfile_fullpath = CTI_creation_from_list(self.engine, checked_items)
            # TODO: Test
            update_path_after_creation(self.engine)
            self.cti_create.emit()

            message = "CTI file created and stored:" + '\n'
            blank = "---------------------------------------------"

            text_with_message = '\n'.join([message + '\n' + path + '\n' + blank for path in lst_CTIfile_fullpath])
            self.t_action.setText(text_with_message + '\n')

    def on_pb_selectall_clicked(self):
        model = self.lview_availCTI.model()
        for row in range(model.rowCount()):
            item = model.item(row)
            item.setCheckState(qtc.Qt.CheckState.Checked)

    def show_warning(self):
        msg_box = qtw.QMessageBox()
        msg_box.setIcon(qtw.QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText("No CTI files have been selected!")
        msg_box.setInformativeText("Please select at least one item.")
        msg_box.setStandardButtons(qtw.QMessageBox.Ok)
        msg_box.exec()


if __name__ == "__main__":
    engine_temppath = r"tests\TestBM\demono1.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
    app = qtw.QApplication(sys.argv)
    dialog = CTIMakingDialog(engine)
    dialog.show()
    sys.exit(app.exec())
