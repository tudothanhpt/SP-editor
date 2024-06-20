import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox


class InputCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Input Checker')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.le_folderName = QLineEdit(self)
        self.le_folderName.setPlaceholderText('Folder Name')
        layout.addWidget(self.le_folderName)

        self.lb_fc = QLineEdit(self)
        self.lb_fc.setPlaceholderText('fc')
        layout.addWidget(self.lb_fc)

        self.lb_fy = QLineEdit(self)
        self.lb_fy.setPlaceholderText('fy')
        layout.addWidget(self.lb_fy)

        self.lb_Ec = QLineEdit(self)
        self.lb_Ec.setPlaceholderText('Ec')
        layout.addWidget(self.lb_Ec)

        self.lb_Es = QLineEdit(self)
        self.lb_Es.setPlaceholderText('Es')
        layout.addWidget(self.lb_Es)

        self.le_cover = QLineEdit(self)
        self.le_cover.setPlaceholderText('Cover')
        layout.addWidget(self.le_cover)

        self.le_spacing = QLineEdit(self)
        self.le_spacing.setPlaceholderText('Spacing')
        layout.addWidget(self.le_spacing)

        self.check_button = QPushButton('Check Input', self)
        self.check_button.clicked.connect(self.check_input)
        layout.addWidget(self.check_button)

        self.setLayout(layout)

    def show_warning(self, message):
        QMessageBox.warning(self, 'Warning', message)

    def check_input(self):
        check_folder_name = {"Folder name": self.le_folderName.text()}

        check_material = {"fc": self.lb_fc.text(),
                          "fy": self.lb_fy.text(),
                          "Ec": self.lb_Ec.text(),
                          "Es": self.lb_Es.text()}

        check_geometry = {
            "Cover": self.le_cover.text(),
            "Spacing": self.le_spacing.text(),
        }

        for data_check in [check_folder_name, check_material, check_geometry]:
            for key, value in data_check.items():
                if not value:
                    error_message = (f"<b>Failed to make section for display.<b> "
                                     f"<p>Please make sure: <p>"
                                     f"<p>1. Ensure you entered enough data <p>"
                                     f"<p>Input data: {key} is missing.<p>")
                    self.show_warning(error_message)
                    return

        # If all checks passed, set the attributes
        self.folder_name = check_folder_name["Folder name"]
        self.bar_cover = float(check_geometry["Cover"])
        self.bar_spacing = float(check_geometry["Spacing"])
        self.material_fc = float(check_material["fc"])
        self.material_fy = float(check_material["fy"])
        self.material_Ec = float(check_material["Ec"])
        self.material_Es = float(check_material["Es"])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InputCheckerApp()
    ex.show()
    sys.exit(app.exec())
