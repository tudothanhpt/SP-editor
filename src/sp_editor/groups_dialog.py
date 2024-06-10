import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widgets.levelgroup_dialog import Ui_group_dialog
from sqlalchemy.engine.base import Engine


class Group_Dialog(qtw.QDialog, Ui_group_dialog):
    def __init__(self, engine: Engine | None = None, path: str | None = None):
        super().__init__()
        self.engine = engine
        self.current_path = path

        self.setupUi(self)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    group_dialog = Group_Dialog()
    group_dialog.show()
    sys.exit(app.exec())
