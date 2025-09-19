from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QDialogButtonBox, QLabel

from src.utilities.config_provider import config_setup
from src.utilities.error_handler import ErrorHandler


# noinspection PyUnresolvedReferences
class AboutDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("aboutDialog")
        self.setFixedSize(200, 150)
        self.error_handler = ErrorHandler(self.parent())
        self.setLayout(self.create_gui())
        self.load_setup()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.about_text_label = QLabel()
        self.about_text_label.setObjectName("aboutTextLabel")
        self.about_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.about_text_label.setWordWrap(True)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.close)
        main_layout.addWidget(self.about_text_label)
        main_layout.addWidget(button_box)
        return main_layout

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            if config:
                self.setWindowTitle(config.get(f"{self.objectName()}Title", "About"))
                self.about_text_label.setText(config.get(f"{self.about_text_label.objectName()}Text", "Mood App\nVersion 1.0\nAuthor: Jin-Mach"))
                self.close_button.setText(config.get(f"{self.close_button.objectName()}Text", "Close"))
            else:
                self.setWindowTitle("About")
                self.about_text_label.setText("Mood App\nVersion 1.0\nAuthor: Jin-Mach")
                self.close_button.setText("Close")
                raise ValueError("Failed to load UI config")
        except Exception as e:
            self.error_handler.write_show_exception(e)