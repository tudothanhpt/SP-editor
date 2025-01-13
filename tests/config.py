import pytest

from sp_editor.repositories.generalInfor_repository import GeneralInforRepository
from sp_editor.services.barset_service import BarsetService
from sp_editor.services.generalInfor_service import GeneralInforService


@pytest.fixture
def session_factory():
    from sqlmodel import SQLModel, Session, create_engine
    engine = create_engine("sqlite:///:memory:")  # Use in-memory SQLite for tests
    SQLModel.metadata.create_all(engine)  # Create tables
    yield lambda: Session(engine)


@pytest.fixture
def repository(session_factory):
    return GeneralInforRepository(session_factory)





@pytest.fixture
def barset_service(repository, tmp_path):
    class MockBarsetService(BarsetService):
        def __init__(self, barset_repository):
            super().__init__(barset_repository)
            self.global_path = tmp_path

        def barset_list(self, barset: str):
            return self.global_path / f"{barset}.json"

    return MockBarsetService(repository)
