import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QLabel, QDialog


class CalculationWindow(QDialog):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Calculation Result")
        layout = QVBoxLayout()

        # Perform a simple calculation based on the current text
        try:
            number = int(text.split()[-1])  # Assuming the text format is "Item X"
            result = number * 2
            calculation_label = QLabel(f"The double of {number} is {result}")
        except ValueError:
            calculation_label = QLabel("Invalid number format")

        layout.addWidget(calculation_label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Item 1", "Item 2", "Item 3"])

        # Connect the currentTextChanged signal to a slot
        self.comboBox.currentTextChanged.connect(self.on_current_text_changed)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Manually trigger the slot for the initial current text
        self.on_current_text_changed(self.comboBox.currentText())

    def on_current_text_changed(self, text):
        print(f"Current text: {text}")

        # Display another window and perform some calculation
        self.display_calculation_window(text)

    def display_calculation_window(self, text):
        calculation_window = CalculationWindow(text)
        calculation_window.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
