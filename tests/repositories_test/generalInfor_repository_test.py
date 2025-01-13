import pytest
from sqlmodel import SQLModel, Session, create_engine
from sp_editor.models.models import GeneralInfor
from sp_editor.repositories.generalInfor_repository import GeneralInforRepository


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")  # Use in-memory SQLite for tests
    SQLModel.metadata.create_all(engine)  # Create tables
    yield lambda: Session(engine)


@pytest.fixture
def generalInfor_repository(session_factory):
    return GeneralInforRepository(session_factory)


def test_add_general_infor(generalInfor_repository):
    params = ["ACI", "Metric", "ASTM615", "Confined", "High"]
    general_infor = generalInfor_repository.add(params)

    assert general_infor.design_code == "ACI"
    assert general_infor.unit_system == "Metric"
    assert general_infor.bar_set == "ASTM615"
    assert general_infor.confinement == "Confined"
    assert general_infor.section_capacity == "High"


def test_update_general_infor(generalInfor_repository):
    params = ["ACI", "Metric", "ASTM615", "Confined", "High"]
    generalInfor_repository.add(params)

    updated_params = ["Eurocode", "Imperial", "PR_EN_10080", "Unconfined", "Low"]
    updated_infor = generalInfor_repository.update(updated_params)

    assert updated_infor.design_code == "Eurocode"
    assert updated_infor.unit_system == "Imperial"
    assert updated_infor.bar_set == "PR_EN_10080"
    assert updated_infor.confinement == "Unconfined"
    assert updated_infor.section_capacity == "Low"


def test_get_by_id(generalInfor_repository):
    params = ["ACI", "Metric", "ASTM615", "Confined", "High"]
    generalInfor_repository.add(params)

    retrieved_infor = generalInfor_repository.get_by_id(1)
    assert retrieved_infor.design_code == "ACI"
    assert retrieved_infor.unit_system == "Metric"
    assert retrieved_infor.bar_set == "ASTM615"
    assert retrieved_infor.confinement == "Confined"
    assert retrieved_infor.section_capacity == "High"
