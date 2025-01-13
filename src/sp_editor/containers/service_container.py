from dependency_injector import containers, providers

from sp_editor.repositories.barSet_repository import BarsetRepository
from sp_editor.repositories.etabsLoadCombos_repository import EtabsLoadCombosRepository
from sp_editor.repositories.etabsPierLabel_repository import EtabsPierLabelRepository
from sp_editor.repositories.etabsStory_repository import EtabsStoryRepository
from sp_editor.repositories.generalInfor_repository import GeneralInforRepository
from sp_editor.repositories.etabsSectionDesignerShape_repository import (
    EtabsSectionDesignerShapeRepository,
)
from sp_editor.repositories.material_repository import MaterialRepository

from sp_editor.services import file_service
from sp_editor.services.barset_service import BarsetService
from sp_editor.services.etabsConnection_service import EtabsConnectionService
from sp_editor.services.etabsDataImport_service import EtabsDataImportService
from sp_editor.services.generalInfor_service import GeneralInforService
from sp_editor.services.groupLevel_service import GroupLevelService
from sp_editor.services.material_service import MaterialService


class ServiceContainer(containers.DeclarativeContainer):
    # Register all services here:
    config = providers.Configuration()

    # file service with session ready for repository
    file_service = providers.Singleton(file_service.FileService)

    # Etabs connection service with SapModel ready
    # TODO: provide etabs path if needed
    etabsConnection_service = providers.Singleton(EtabsConnectionService)

    # general infor tobe provide session and then repository tobe provided to service
    generalInfor_repository = providers.Factory(
        GeneralInforRepository, session_factory=file_service.provided.session
    )

    generalInfor_service = providers.Factory(
        GeneralInforService, generalInfor_repository=generalInfor_repository
    )

    # Barset repository and service
    barset_repository = providers.Factory(
        BarsetRepository, session_factory=file_service.provided.session
    )

    barset_service = providers.Factory(
        BarsetService, barset_repository=barset_repository
    )

    # Story data
    etabsStory_repository = providers.Factory(
        EtabsStoryRepository, session_factory=file_service.provided.session
    )

    # material concrete and rebar
    material_repository = providers.Factory(
        MaterialRepository, session_factory=file_service.provided.session
    )
    material_service = providers.Factory(
        MaterialService, material_repository=material_repository
    )

    # Group level
    groupLevel_service = providers.Factory(
        GroupLevelService, etabsStory_repository=etabsStory_repository
    )

    # Etabs data import repository and service

    # Pier Label data
    etabsPierLabel_repository = providers.Factory(
        EtabsPierLabelRepository, session_factory=file_service.provided.session
    )
    # Etabs section designer shape data
    etabsSectionDesignerShape_repository = providers.Factory(
        EtabsSectionDesignerShapeRepository,
        session_factory=file_service.provided.session,
    )
    # Etabs load combos data
    etabsLoadCombos_repository = providers.Factory(
        EtabsLoadCombosRepository, session_factory=file_service.provided.session
    )

    # all domain data need for init service
    etabsDataImport_service = providers.Factory(
        EtabsDataImportService,
        etabsConnection_service=etabsConnection_service,
        etabsStory_repository=etabsStory_repository,
        etabsPierLabel_repository=etabsPierLabel_repository,
        etabsSectionDesignerShape_repository=etabsSectionDesignerShape_repository,
        etabsLoadCombos_repository=etabsLoadCombos_repository,
    )
