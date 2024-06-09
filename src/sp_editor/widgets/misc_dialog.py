import os
import sys
from PySide6.QtWidgets import QApplication, QMessageBox

def show_file_not_found_message(message: str):
    """
    Display a QMessageBox indicating that the database file does not exist.
    """
    app = QApplication(sys.argv)  # Initialize QApplication
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.setWindowTitle("File Not Found")
    msg_box.exec() 

def show_database_updated_message() -> None:
    """Display a message box informing the user that the database has been updated."""
    app = QApplication(sys.argv)  # Initialize QApplication
    msg_box = QMessageBox()
    msg_box.setText("The database has been successfully updated.")
    msg_box.setWindowTitle("Database Updated")
    msg_box.exec()
       
    
if __name__ == "__main__":
    show_database_updated_message()