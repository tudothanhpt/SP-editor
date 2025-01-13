import pytest
import os
from unittest.mock import patch, MagicMock
from sqlmodel import SQLModel
from sp_editor.services.file_service import FileService
from PySide6.QtWidgets import QMessageBox



@pytest.fixture
def file_service():
    return FileService()


@pytest.fixture
def temp_db_path(tmp_path):
    return tmp_path / "test.db"


def test_new_database_creates_file(file_service, temp_db_path):
    # Mock QMessageBox response to allow overwrite
    with patch("sp_editor.services.file_service.QMessageBox.question", return_value=QMessageBox.Yes):
        created = file_service.new_database(str(temp_db_path))

    assert created is True
    assert os.path.exists(temp_db_path)


def test_new_database_prevents_overwrite(file_service, temp_db_path):
    # Create a mock database file
    temp_db_path.touch()

    # Mock QMessageBox response to prevent overwrite
    with patch("sp_editor.services.file_service.QMessageBox.question", return_value=QMessageBox.No):
        created = file_service.new_database(str(temp_db_path))

    assert created is None  # Should not proceed with overwrite
    assert temp_db_path.exists()  # File should still exist


def test_open_database_success(file_service, temp_db_path):
    # Create a mock database file
    temp_db_path.touch()

    opened = file_service.open_database(str(temp_db_path))
    assert opened is True


def test_open_database_file_not_found(file_service):
    non_existent_path = "non_existent.db"

    with patch("sp_editor.services.file_service.QMessageBox.critical") as mock_error:
        opened = file_service.open_database(non_existent_path)

    assert opened is False
    mock_error.assert_called_once_with(None, "Error", "File not found")


def test_open_database_handles_exception(file_service, temp_db_path):
    # Mock an exception in `create_engine`
    with patch("sp_editor.services.file_service.create_engine", side_effect=Exception("Some error")):
        with patch("sp_editor.services.file_service.QMessageBox.critical") as mock_error:
            opened = file_service.open_database(str(temp_db_path))

    assert opened is False
    mock_error.assert_called_once_with(None, "Error", 'File not found')


def test_session_without_open_database(file_service):
    with pytest.raises(RuntimeError, match="Database not opened, Call open_database"):
        with file_service.session():
            pass


def test_session_with_open_database(file_service, temp_db_path):
    # Create and open the database
    file_service.new_database(str(temp_db_path))

    with file_service.session() as session:
        assert session is not None
        assert session.get_bind().url.database == str(temp_db_path)


def test_create_database_failure(file_service, temp_db_path):
    # Mock `create_engine` to raise an exception
    with patch("sp_editor.services.file_service.create_engine", side_effect=Exception("Creation error")):
        with patch("sp_editor.services.file_service.QMessageBox.critical") as mock_error:
            created = file_service.new_database(str(temp_db_path))

    assert created is None
    mock_error.assert_called_once_with(None, "Error", "Error creating database: Creation error")
