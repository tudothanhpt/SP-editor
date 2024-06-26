import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from sqlalchemy.engine.base import Engine
from sp_editor.database.database import connect_db_and_tables


class OpenFile_Dialog(qtw.QFileDialog):
    engine_open = qtc.Signal(Engine)  # Define a custom signal that emits an Engine object
    path_open = qtc.Signal(str)
    current_db = qtc.Signal(int)

    def __init__(self, parent: qtw.QMainWindow | None = None):
        super().__init__()
        self.engine = None
        self.dialog_open_path = None
        self.parent = parent

    @qtc.Slot()
    def open_file(self):
        extensions = "sp_editor file (*.spe)"
        root_path = sys.path[0]
        try:
            self.dialog_open_path, _ = qtw.QFileDialog.getOpenFileName(
                self, "Open File", root_path, extensions
            )
            if self.dialog_open_path:
                self.engine = connect_db_and_tables(self.dialog_open_path)
                self.path_open.emit(self.dialog_open_path)
                self.engine_open.emit(self.engine)  # Emit the signal with the engine
                self.current_db.emit(1)
            else:
                qtw.QMessageBox.warning(self.parent, "File not selected", "No file was selected", qtw.QMessageBox.Ok)
        except FileNotFoundError:
            qtw.QMessageBox.warning(self.parent, "File not found", "No such file or directory", qtw.QMessageBox.Ok)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = OpenFile_Dialog()
