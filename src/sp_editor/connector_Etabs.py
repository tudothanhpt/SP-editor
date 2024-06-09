from utils import get_open_filename
import sys
import os
import pytabs
import errno

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg


def get_current_opened_etabs_name() -> str:
    sap_model = connect_to_etabs()[0]
    active_model = sap_model.GetModelFilename()

    return active_model


def connect_to_etabs(widget: qtw.QDialog, model_is_open: bool):
    global etabs_model
    while True:
        if model_is_open:
            etabs_model = pytabs.EtabsModel(attach_to_instance=model_is_open)
            print(etabs_model.model_path)
            break
        else:
            file_name = "ETABS Model Files (*.EDB)"
            root_path = sys.path[0]
            path = ""
            try:
                path = get_open_filename(file_name, root_path)
                etabs_model = pytabs.EtabsModel(attach_to_instance=model_is_open)
                etabs_model.open_model(path)
                print(path)
                break
            except FileNotFoundError:
                qtw.QMessageBox.warning(
                    widget,
                    "File not found",
                    "No such file or directory",
                    qtw.QMessageBox.StandardButton.Ok,
                )
                break
    return etabs_model
