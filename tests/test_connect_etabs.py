import sys
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
                               QLabel, QLineEdit, QVBoxLayout, QWidget, QStackedWidget)


class RebarWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout
        layout = QVBoxLayout()

        # Create the group box
        group_box = QGroupBox("Rebar")
        group_layout = QVBoxLayout()

        # Create the "Bars by" combo box
        self.bars_by_combo = QComboBox()
        self.bars_by_combo.addItems(["Size", "Area"])
        self.bars_by_combo.currentIndexChanged.connect(self.update_bar_size_widget)

        # Create the label and stacked widget for "Bar size"
        bar_size_label = QLabel("Bar size")
        self.bar_size_stacked_widget = QStackedWidget()

        # Create the combo box and line edit for "Bar size"
        self.bar_size_combo = QComboBox()
        self.bar_size_combo.addItems(["#3", "#4", "#5", "#6", "#7", "#8"])

        self.bar_size_line_edit = QLineEdit()

        # Add the combo box and line edit to the stacked widget
        self.bar_size_stacked_widget.addWidget(self.bar_size_combo)
        self.bar_size_stacked_widget.addWidget(self.bar_size_line_edit)

        # Create the rest of the labels and widgets
        spacing_label = QLabel("Spacing")
        self.spacing_edit = QLineEdit()

        quantities_label = QLabel("Quantities")
        self.quantities_edit = QLineEdit()

        # Add widgets to the group layout
        group_layout.addWidget(QLabel("Bars by"))
        group_layout.addWidget(self.bars_by_combo)
        group_layout.addWidget(bar_size_label)
        group_layout.addWidget(self.bar_size_stacked_widget)
        group_layout.addWidget(spacing_label)
        group_layout.addWidget(self.spacing_edit)
        group_layout.addWidget(quantities_label)
        group_layout.addWidget(self.quantities_edit)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        self.setLayout(layout)

        # Initialize the correct widget for "Bar size"
        self.update_bar_size_widget()

    def update_bar_size_widget(self):
        if self.bars_by_combo.currentText() == "Size":
            self.bar_size_stacked_widget.setCurrentWidget(self.bar_size_combo)
        else:
            self.bar_size_stacked_widget.setCurrentWidget(self.bar_size_line_edit)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = RebarWidget()
    widget.show()
    sys.exit(app.exec())
