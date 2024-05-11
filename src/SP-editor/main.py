from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog
import sys
import ezdxf


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.create_autocad_file()
        self.SetupUI()

    def create_autocad_file(self):
        doc = ezdxf.new(setup=True)
        msp = doc.modelspace()
        msp.add_line((0, 0), (1, 0), dxfattribs={'layer': 'Mylayer'})
        doc.saveas('Myfile.dxf')

    def SetupUI(self):
        self.setWindowTitle('SP Editor')
        self.setFixedSize(500, 500)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())
