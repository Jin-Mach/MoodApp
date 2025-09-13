import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from src.utilities.logger_provider import get_logger
from src.utilities.config_provider import config_setup
from src.utilities.support_provider import SupportProvider


class ErrorHandler(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("errorHandler")
        self.setLayout(self.create_gui())
        self.load_setup()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.error_text_label = QLabel()
        self.error_text_label.setObjectName("errorTextLabel")
        self.error_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout = QHBoxLayout()
        self.continue_button = QPushButton()
        self.continue_button.setObjectName("continueButton")
        self.continue_button.clicked.connect(self.close)
        self.cancel_button = QPushButton()
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.close_application)
        button_layout.addStretch()
        button_layout.addWidget(self.continue_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addWidget(self.error_text_label)
        main_layout.addLayout(button_layout)
        return main_layout

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            self.default_text = config.get(f"{self.error_text_label.objectName()}Text", "Error")
            if config:
                self.error_text_label.setText(config.get(self.default_text, "Error:"))
                self.continue_button.setText(config.get(f"{self.continue_button.objectName()}Text", "Continue"))
                self.cancel_button.setText(config.get(f"{self.cancel_button.objectName()}Text", "Close"))
            else:
                self.error_text_label.setText(self.default_text)
                self.continue_button.setText("Continue")
                self.cancel_button.setText("Cancel")
                raise ValueError("Failed to load UI config")
        except Exception as e:
            self.write_show_exception(e, False)

    def close_application(self) -> None:
        self.close()
        sys.exit(1)

    def write_show_exception(self, exception: Exception, show_dialog: bool = True, continue_visible: bool = True,
                             cancel_visible: bool = False) -> None:
        if not self.parent() or not self.parent().isVisible():
            SupportProvider.centre_on_screen(self)
        if show_dialog:
            self.error_text_label.setText(f"{self.default_text}\n{type(exception).__name__}: {exception}")
            self.continue_button.setVisible(continue_visible)
            self.cancel_button.setVisible(cancel_visible)
            self.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.exec()
        logger = get_logger()
        logger.error(exception, exc_info=True)