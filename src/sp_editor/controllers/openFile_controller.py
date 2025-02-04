from dependency_injector.wiring import inject, Provide
from PySide6 import QtWidgets as qtw

from sp_editor.services.file_service import FileService

from sp_editor.containers.service_container import ServiceContainer
from sp_editor.services.generalInfor_service import GeneralInforService


class OpenFileController(qtw.QDialog):
    @inject
    def __init__(
            self, file_service: FileService = Provide[ServiceContainer.file_service],
            generalInfor_service: GeneralInforService = Provide[
                ServiceContainer.generalInfor_service],
    ):
        super().__init__()

        self.file_service = file_service
        self.generalInfor_service = generalInfor_service

    def execute(self):
        file_path, _ = qtw.QFileDialog.getOpenFileName(
            self, "Open File", "", "sp_editor file (*.spe)"
        )
        if file_path:
            if self.file_service.open_database(file_path):
                # TODO Read database to make it consistent file path and so on
                qtw.QMessageBox.information(
                    self, "Success", f"Database opened from: {file_path}"
                )
            else:
                qtw.QMessageBox.critical(self, "Error", "Failed to open database.")


