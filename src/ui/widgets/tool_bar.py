from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolBar, QToolButton, QMenu, QSizePolicy, QWidget

from src.ui.widgets.about_dialog import AboutDialog
from src.ui.widgets.manual_dialog import ManualDialog
from src.ui.widgets.history_dialog import HistoryDialog
from src.utilities.config_provider import config_setup
from src.utilities.error_handler import ErrorHandler


# noinspection PyUnresolvedReferences
class ToolBar(QToolBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("toolBar")
        self.setMovable(False)
        self.setFloatable(False)
        self.error_handler = ErrorHandler(self.parent())
        self.create_gui()
        self.load_setup()
        self.create_connection()

    def create_gui(self) -> None:
        options_menu = QMenu()
        self.app_history_action = QAction(self)
        self.app_history_action.setObjectName("appHistoryAction")
        options_menu.addAction(self.app_history_action)
        self.options_menu_button = QToolButton()
        self.options_menu_button.setObjectName("optionsMenuButton")
        self.options_menu_button.setMenu(options_menu)
        self.options_menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        about_menu = QMenu()
        self.app_manual_action = QAction(self)
        self.app_manual_action.setObjectName("appManualAction")
        self.about_app_action = QAction(self)
        self.about_app_action.setObjectName("aboutAppAction")
        about_menu.addAction(self.app_manual_action)
        about_menu.addAction(self.about_app_action)
        self.about_menu_button = QToolButton()
        self.about_menu_button.setObjectName("aboutMenuButton")
        self.about_menu_button.setMenu(about_menu)
        self.about_menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.addWidget(self.options_menu_button)
        self.addWidget(spacer)
        self.addWidget(self.about_menu_button)

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            if config:
                self.app_history_action.setText(config.get(f"{self.app_history_action.objectName()}Text", "History"))
                self.app_manual_action.setText(config.get(f"{self.app_manual_action.objectName()}Text", "Manual"))
                self.about_app_action.setText(config.get(f"{self.about_app_action.objectName()}Text", "About"))
                self.options_menu_button.setText(config.get(f"{self.options_menu_button.objectName()}Text", "Options"))
                self.about_menu_button.setText(config.get(f"{self.about_menu_button.objectName()}Text", "More"))
            else:
                self.app_history_action.setText("History")
                self.app_manual_action.setText("Manual")
                self.about_app_action.setText("About")
                self.options_menu_button.setText("Options")
                self.about_menu_button.setText("More")
                raise ValueError("Failed to load UI config")
        except Exception as e:
            self.error_handler.write_show_exception(e)

    def create_connection(self) -> None:
        self.app_history_action.triggered.connect(self.show_history_dialog)
        self.app_manual_action.triggered.connect(self.show_manual_dialog)
        self.about_app_action.triggered.connect(self.show_about_dialog)

    def show_history_dialog(self) -> None:
        settings_dialog = HistoryDialog(self.parent())
        settings_dialog.exec()

    def show_manual_dialog(self) -> None:
        manual_dialog = ManualDialog(self.parent())
        manual_dialog.exec()

    def show_about_dialog(self) -> None:
        about_dialog = AboutDialog(self.parent())
        about_dialog.exec()