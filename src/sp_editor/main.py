import sys
from PySide6.QtWidgets import QApplication

from sp_editor.containers.controller_container import AppContainer
from sp_editor.controllers.mainWindow_controller import MainWindowController


def main():
    # Initialize QApplication
    app = QApplication(sys.argv)

    # Initialize the container
    container = AppContainer()
    container.init_resources()
    container.wire(modules=[__name__])

    # Resolve the main window controller from the container
    main_window: MainWindowController = container.mainWindow_controller()
    main_window.show()

    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
