from dependency_injector import containers, providers

from sp_editor.containers.service_container import ServiceContainer
from sp_editor.controllers.barSet_controller import BarSetController
from sp_editor.controllers.calculationCase_controller import CalculationCaseController
from sp_editor.controllers.generalInfor_controller import GeneralInforController
from sp_editor.controllers.groupLevel_controller import GroupLevelController
from sp_editor.controllers.mainWindow_controller import MainWindowController
from sp_editor.controllers.material_controller import MaterialController
from sp_editor.controllers.newFile_controller import NewFileController
from sp_editor.controllers.openFile_controller import OpenFileController
from sp_editor.controllers.etabsImport_controller import EtabsImportController


class AppContainer(containers.DeclarativeContainer):
    # Import Services
    service_container = providers.Container(ServiceContainer)

    # provide services for controller
    newFile_controller = providers.Factory(
        NewFileController,
        file_service=service_container.file_service,
        generalInfor_service=service_container.generalInfor_service,
        barset_service=service_container.barset_service,
    )

    openFile_controller = providers.Factory(
        OpenFileController, file_service=service_container.file_service
    )

    etabsImport_controller = providers.Factory(
        EtabsImportController,
        etabsConnection_service=service_container.etabsConnection_service,
        etabsDataImport_service=service_container.etabsDataImport_service,
    )

    generalInfor_controller = providers.Factory(
        GeneralInforController,
        generalInfor_service=service_container.generalInfor_service,
    )

    barset_controller = providers.Factory(
        BarSetController,
        generalInfor_service=service_container.generalInfor_service,
        barset_service=service_container.barset_service,
    )

    material_controller = providers.Factory(
        MaterialController,
        material_service=service_container.material_service,
    )

    groupLevel_controller = providers.Factory(
        GroupLevelController, service_container.groupLevel_service
    )

    calculationCase_controller = providers.Factory(
        CalculationCaseController, service_container.calculationCase_service
    )

    # main window provides function
    mainWindow_controller = providers.Factory(
        MainWindowController,
        newFile_controller,
        openFile_controller,
        etabsImport_controller,
        generalInfor_controller,
        barset_controller,
        material_controller,
        groupLevel_controller,
        calculationCase_controller,
    )
