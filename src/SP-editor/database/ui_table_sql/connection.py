import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtSql as qsql


def create_connection(widget: qtw.QDialog, path: str, table_name: str):
    database = qsql.QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(path)
    if not database.open():
        sys.exit(1)
    tables_needed = {table_name}
    tables_not_found = tables_needed - set(database.tables())
    if tables_not_found:
        qtw.QMessageBox.critical(widget, "Error",
                                 f"<p> The following table are missing"
                                 f"from the database:{tables_not_found}<p>")
        sys.exit(-1)


def create_model(table_name: str):
    model = qsql.QSqlTableModel()
    model.setTable(table_name)
    return model
