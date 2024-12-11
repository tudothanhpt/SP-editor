import sys
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from sp_editor.widgets.about_dialog_ui import Ui_d_About


class AboutDialog(qtw.QDialog, Ui_d_About):
    def __init__(self, parent: qtw.QWidget = None):
        super().__init__(parent)
        self.setupUi(self)
        self.pb_OK.clicked.connect(self.on_ok_clicked)
        self.label.setPixmap(qtg.QPixmap("icons/SP-EDITOR_PNG.png"))

    def on_ok_clicked(self):
        self.close()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = AboutDialog()
    window.show()
    sys.exit(app.exec())
