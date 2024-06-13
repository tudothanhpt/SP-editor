import pandas as pd
from typing import Any, List
from pandas import DataFrame
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QListView, QPushButton
from PySide6.QtCore import QStringListModel
from core.connect_etabs import connect_to_etabs


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QListView Example")

        # Create a QListView
        self.list_view = QListView(self)

        # Create a QPushButton to trigger the data fetching and display
        self.fetch_button = QPushButton("Fetch Pier Force Data", self)
        self.fetch_button.clicked.connect(self.fetch_data)

        # Set layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.list_view)
        layout.addWidget(self.fetch_button)
        self.setLayout(layout)

    def fetch_data(self):
        sap_model, etabs_object = connect_to_etabs(True)
        design_combos = ['LC1_1.4D']
        output = get_pier_force_data(sap_model, etabs_object, design_combos)
        if not output.empty:
            self.display_data(output)

    def display_data(self, df: DataFrame):
        # Convert DataFrame to list of strings
        data_strings = df.apply(lambda row: ', '.join(row.values.astype(str)), axis=1).tolist()

        # Create a QStringListModel with the data
        model = QStringListModel(data_strings)

        # Set the model to the QListView
        self.list_view.setModel(model)


if __name__ == '__main__':
    # sap_model, etabs_object = connect_to_etabs(True)
    # design_combos = ['LC1_1.4D']
    # output = get_pier_force_data(sap_model, etabs_object, design_combos)
    # print(output)
    app = QApplication([])

    # Create and show the main window
    window = MainWindow()
    window.show()

    app.exec()
