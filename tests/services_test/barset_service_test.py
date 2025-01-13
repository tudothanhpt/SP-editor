import pytest
import json
from sp_editor.services.barset_service import BarsetService
from sp_editor.repositories.barSet_repository import BarsetRepository


@pytest.fixture
def session_factory():
    from sqlmodel import SQLModel, Session, create_engine
    engine = create_engine("sqlite:///:memory:")  # Use in-memory SQLite for tests
    SQLModel.metadata.create_all(engine)  # Create tables
    yield lambda: Session(engine)


@pytest.fixture
def barset_repository(session_factory):
    return BarsetRepository(session_factory)


@pytest.fixture
def barset_service(barset_repository, tmp_path):
    class MockBarsetService(BarsetService):
        def __init__(self, barset_repository):
            super().__init__(barset_repository)
            self.global_path = tmp_path

        def barset_list(self, barset: str):
            return self.global_path / f"{barset}.json"

    return MockBarsetService(barset_repository)


def test_load_barsets_from_file(barset_service, tmp_path):
    # Create mock JSON file
    barset_data = [
        {"size": "#4", "diameter": 12.7, "area": 126.7, "weight": 0.994},
        {"size": "#5", "diameter": 16.0, "area": 201.0, "weight": 1.5},
    ]
    barset_file = tmp_path / "ASTM615.json"
    with open(barset_file, "w") as f:
        json.dump(barset_data, f)

    # Call the service method
    barset_service.load_barsets_from_file("ASTM615")

    # Check if data was imported
    barsets = barset_service.barset_repository.get_all()
    assert len(barsets) == 2
    assert barsets[0].size == "#4"
    assert barsets[1].size == "#5"
