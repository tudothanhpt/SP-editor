import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from sqlalchemy.engine.base import Engine
from sp_editor.database.database import connect_db_and_tables
from database.mainWindow_model import MainWindowModel


class OpenFile_Dialog(qtw.QFileDialog):
    engine_open = qtc.Signal(Engine)  # Define a custom signal that emits an Engine object
    path_open = qtc.Signal(str)
    current_db = qtc.Signal(Engine)

    def __init__(self, parent: qtw.QMainWindow | None = None):
        super().__init__(parent)  # Make sure to pass the parent here
        self.engine = None
        self.dialog_open_path = None
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Open File")
        self.setNameFilter("sp_editor file (*.spe)")
        self.setDirectory(sys.path[0])
        self.fileSelected.connect(self.on_file_selected)

    @qtc.Slot(str)
    def on_file_selected(self, file_path):
        self.dialog_open_path = file_path
        if self.dialog_open_path:
            try:
                self.engine = connect_db_and_tables(self.dialog_open_path)
                self.path_open.emit(self.dialog_open_path)
                self.current_db.emit(self.engine)
                self.engine_open.emit(self.engine)  # Emit the signal with the engine
            except FileNotFoundError:
                qtw.QMessageBox.warning(self.parent, "File not found", "No such file or directory", qtw.QMessageBox.Ok)
        else:
            qtw.QMessageBox.warning(self.parent, "File not selected", "No file was selected", qtw.QMessageBox.Ok)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    open_file_dialog = OpenFile_Dialog()
    sys.exit(app.exec())
