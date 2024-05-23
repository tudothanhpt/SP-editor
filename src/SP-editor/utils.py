import sys
import os
import comtypes.client

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg


def AttachToInstance():
    """
        Return Values:
        SapModel (type cOAPI pointer)
        EtabsObject (type cOAPI pointer)
        """
    # attach to a running instance of ETABS
    try:
        # get the active ETABS object
        EtabsObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
    # create SapModel object
    SapModel = EtabsObject.SapModel
    # setEtabsUnits()
    return SapModel, EtabsObject

def SpecifyPathEtabs():
    ProgramPath = "C:\Program Files\Computers and Structures\ETABS 21\ETABS.exe"
    # create API helper object
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    try:
        # 'create an instance of the ETABS object from the specified path
        myETABSObject = helper.CreateObject(ProgramPath)
    except (OSError, comtypes.COMError):
        print("Cannot start a new instance of the program from " + ProgramPath)
        sys.exit(-1)
    else:
        try:
            # create an instance of the ETABS object from the latest installed ETABS
            myETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("Cannot start a new instance of the program.")
            sys.exit(-1)
        # start ETABS application
    myETABSObject.ApplicationStart()


def open_url(url):
    qtg.QDesktopServices.openUrl(qtc.QUrl(url))


def about_dialog(parent, title, text):
    qtw.QMessageBox.about(parent, title, text)


def get_save_filename(suffix):
    rv, _ = qtw.QFileDialog.getSaveFileName(caption="Save File", filter='*.{}'.format(suffix))
    if rv != '' and not rv.endswith(suffix): rv += '.' + suffix

    return rv


def get_open_filename(suffix, curr_dir):
    rv, _ = qtw.QFileDialog.getOpenFileName(caption="Open Model File", dir=curr_dir, filter=suffix)
    if rv != '' and not rv.endswith(suffix): rv += '.' + suffix

    return rv


def confirm(parent, title, msg):
    rv = qtw.QMessageBox.question(parent, title, msg, qtw.QMessageBox.Yes, qtw.QMessageBox.No)

    return True if rv == qtw.QMessageBox.Yes else False
