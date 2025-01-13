import os.path
from contextlib import contextmanager

from PySide6.QtWidgets import QMessageBox
from sqlmodel import create_engine, SQLModel, Session


class FileService:
    def __init__(self):
        self._engine = None

    def new_database(self, db_url: str):
        """
        Create a new SQLite database with the URL from user machine
        :param db_url: file location
        :return: True
        """
        if self._confirm_overwrite(db_url):
            return self._create_database(db_url)

    def open_database(self, db_url: str):
        """
        Connect to an SQLite database with the URL from user selection
        :param db_url:
        :return: Truess
        """
        try:
            if not os.path.exists(db_url):
                raise FileNotFoundError("File not found")
            self._engine = create_engine(f"sqlite:///{db_url}", echo=True)
            return True
        except FileNotFoundError as e:
            self._show_error(str(e))
            return False
        except Exception as e:
            self._show_error(f"Error opening database:{e}")
            return False

    @contextmanager
    def session(self):
        """
        Provide a session with database which already been connected using create a new or open database
        :return: session:Session
        """
        if self._engine is None:
            raise RuntimeError(
                "Database not opened, Call open_database() or new_database() first."
            )
        with Session(self._engine) as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

    def _create_database(self, db_url):
        try:
            self._engine = create_engine(f"sqlite:///{db_url}", echo=True)
            SQLModel.metadata.create_all(self._engine)
            return True
        except Exception as e:
            self._show_error(f"Error creating database: {e}")
            return None

    def _confirm_overwrite(self, db_url):
        if os.path.exists(db_url):
            reply = QMessageBox.question(
                None,
                "File Exists",
                "A file with this name already exist. Do you want to overwrite it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return False
            else:
                os.remove(db_url)
        return True

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(None, "Error", message)
