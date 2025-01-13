import pytest
from sqlmodel import SQLModel, Session, create_engine
from sp_editor.repositories.barSet_repository import BarsetRepository


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")  # Use in-memory SQLite for tests
    SQLModel.metadata.create_all(engine)  # Create tables
    yield lambda: Session(engine)


@pytest.fixture
def barset_repository(session_factory):
    return BarsetRepository(session_factory)


def test_add_barset(barset_repository):
    params = ["#4", 12.7, 126.7, 0.994]
    barset = barset_repository.add(params)

    assert barset.size == "#4"
    assert barset.diameter == 12.7
    assert barset.area == 126.7
    assert barset.weight == 0.994


def test_update_barset(barset_repository):
    params = ["#4", 12.7, 126.7, 0.994]
    barset = barset_repository.add(params)

    updated_params = ["#5", 16.0, 201.0, 1.5]
    updated_barset = barset_repository.update(barset.id, updated_params)

    assert updated_barset.size == "#5"
    assert updated_barset.diameter == 16.0
    assert updated_barset.area == 201.0
    assert updated_barset.weight == 1.5


def test_get_by_id(barset_repository):
    params = ["#4", 12.7, 126.7, 0.994]
    barset = barset_repository.add(params)

    retrieved_barset = barset_repository.get_by_id(barset.id)
    assert retrieved_barset.size == "#4"
    assert retrieved_barset.diameter == 12.7
    assert retrieved_barset.area == 126.7
    assert retrieved_barset.weight == 0.994


def test_get_all(barset_repository):
    params1 = ["#4", 12.7, 126.7, 0.994]
    params2 = ["#5", 16.0, 201.0, 1.5]
    barset_repository.add(params1)
    barset_repository.add(params2)

    barsets = barset_repository.get_all()
    assert len(barsets) == 2
    assert barsets[0].size == "#4"
    assert barsets[1].size == "#5"


def test_delete_by_id(barset_repository):
    params = ["#4", 12.7, 126.7, 0.994]
    barset = barset_repository.add(params)

    success = barset_repository.delete_by_id(barset.id)
    assert success

    retrieved_barset = barset_repository.get_by_id(barset.id)
    assert retrieved_barset is None


def test_import_barsets(barset_repository):
    barsets_data = [
        {"size": "#4", "diameter": 12.7, "area": 126.7, "weight": 0.994},
        {"size": "#5", "diameter": 16.0, "area": 201.0, "weight": 1.5},
    ]

    barset_repository.import_barsets(barsets_data)

    barsets = barset_repository.get_all()
    assert len(barsets) == 2
    assert barsets[0].size == "#4"
    assert barsets[1].size == "#5"
