import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from sqlalchemy.engine.base import Engine
from database.database import connect_db_and_tables


class OpenFile_Dialog(qtw.QFileDialog):
    engine_open = qtc.Signal(Engine)  # Define a custom signal that emits an Engine object
    path_open = qtc.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = None
        self.dialog_open_path = None
        self.open_file(parent)

    @qtc.Slot()
    def open_file(self, parent=None):
        extensions = "SP-editor file (*.spe)"
        root_path = sys.path[0]
        try:
            self.dialog_open_path, _ = qtw.QFileDialog.getOpenFileName(
                self, "Open File", root_path, extensions
            )
            if self.dialog_open_path:
                print(self.dialog_open_path)
                self.engine = connect_db_and_tables(self.dialog_open_path)
                self.path_open.emit(self.dialog_open_path)
                self.engine_open.emit(self.engine)  # Emit the signal with the engine
            else:
                qtw.QMessageBox.warning(self, "File not selected", "No file was selected", qtw.QMessageBox.Ok)
        except FileNotFoundError:
            qtw.QMessageBox.warning(parent, "File not found", "No such file or directory", qtw.QMessageBox.Ok)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = OpenFile_Dialog()
    sys.exit(app.exec())
