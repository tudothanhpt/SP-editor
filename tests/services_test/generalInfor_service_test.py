import pytest
from sp_editor.models.models import GeneralInfor
from sp_editor.services.generalInfor_service import GeneralInforService
from sp_editor.repositories.generalInfor_repository import GeneralInforRepository


@pytest.fixture
def session_factory():
    from sqlmodel import SQLModel, Session, create_engine
    engine = create_engine("sqlite:///:memory:")  # Use in-memory SQLite for tests
    SQLModel.metadata.create_all(engine)  # Create tables
    yield lambda: Session(engine)


@pytest.fixture
def generaInfor_repository(session_factory):
    return GeneralInforRepository(session_factory)


@pytest.fixture
def generalInfor_service(generaInfor_repository):
    return GeneralInforService(generaInfor_repository)


def test_add_general_infor_service(generalInfor_service):
    params = ["ACI", "Metric", "ASTM615", "Confined", "High"]
    general_infor = generalInfor_service.add_generalInfor(params)

    assert general_infor.design_code == "ACI"
    assert general_infor.unit_system == "Metric"
    assert general_infor.bar_set == "ASTM615"
    assert general_infor.confinement == "Confined"
    assert general_infor.section_capacity == "High"


def test_update_general_infor_service(generalInfor_service):
    params = ["ACI", "Metric", "ASTM615", "Confined", "High"]
    generalInfor_service.add_generalInfor(params)

    updated_params = ["Eurocode", "Imperial", "PR_EN_10080", "Unconfined", "Low"]
    updated_infor = generalInfor_service.update_generalInfor(updated_params)

    assert updated_infor.design_code == "Eurocode"
    assert updated_infor.unit_system == "Imperial"
    assert updated_infor.bar_set == "PR_EN_10080"
    assert updated_infor.confinement == "Unconfined"
    assert updated_infor.section_capacity == "Low"


def test_get_general_infor_service(generalInfor_service):
    params = ["ACI", "Metric", "ASTM615", "Confined", "High"]
    generalInfor_service.add_generalInfor(params)

    retrieved_infor = generalInfor_service.get_generalInfor(1)
    assert retrieved_infor.design_code == "ACI"
    assert retrieved_infor.unit_system == "Metric"
    assert retrieved_infor.bar_set == "ASTM615"
    assert retrieved_infor.confinement == "Confined"
    assert retrieved_infor.section_capacity == "High"
