from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLayout, QTextEdit, QDialogButtonBox

from src.utilities.config_provider import config_setup
from src.utilities.error_handler import ErrorHandler


# noinspection PyUnresolvedReferences
class ManualDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualDialog")
        self.setFixedSize(400, 300)
        self.error_handler = ErrorHandler(self.parent())
        self.setLayout(self.create_gui())
        self.load_setup()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_edit = QTextEdit()
        self.manual_edit.setObjectName("manualEdit")
        self.manual_edit.setReadOnly(True)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.close)
        main_layout.addWidget(self.manual_edit)
        main_layout.addWidget(button_box)
        return main_layout

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            manual_text = ("<p align=\"center\">MoodApp</p><p>1. Select your current mood from the main screen.</p><p>"
                           "2. Optionally, write a short note about your day.</p>")
            if config:
                self.setWindowTitle(config.get(f"{self.objectName()}Title", "Manual"))
                self.manual_edit.setHtml(config.get(f"{self.manual_edit.objectName()}Text", manual_text))
                self.close_button.setText(config.get(f"{self.close_button.objectName()}Text", "Close"))
            else:
                self.close_button.setText("Close")
                self.setWindowTitle("Manual")
                self.manual_edit.setHtml(manual_text)
                raise ValueError("Failed to load UI config")
        except Exception as e:
            self.error_handler.write_show_exception(e)