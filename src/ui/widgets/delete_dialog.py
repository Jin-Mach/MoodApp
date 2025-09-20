from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox

from src.utilities.config_provider import config_setup
from src.utilities.error_handler import ErrorHandler


# noinspection PyTypeChecker
class DeleteDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("deleteDialog")
        self.error_handler = ErrorHandler(self.parent())
        self.setLayout(self.create_gui())
        self.load_setup()
        self.create_connection()
        self.adjustSize()
        self.setFixedSize(self.size())

    def create_gui(self) -> QLayout:
        main_layout= QVBoxLayout()
        self.delete_label = QLabel()
        self.delete_label.setObjectName("deleteLabel")
        self.delete_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        self.delete_label.setFont(font)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close)
        self.delete_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.delete_button.setObjectName("deleteButton")
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        main_layout.addWidget(self.delete_label)
        main_layout.addWidget(button_box)
        return main_layout

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            if config:
                self.delete_label.setText(config.get(f"{self.delete_label.objectName()}Text", "Are you sure you want to delete all saved mood history?"))
                self.delete_button.setText(config.get(f"{self.delete_button.objectName()}", "Delete"))
                self.close_button.setText(config.get(f"{self.close_button.objectName()}Text", "Close"))
            else:
                self.delete_label.setText("Are you sure you want to delete all saved mood history?")
                self.delete_button.setText("Delete")
                self.close_button.setText("Close")
                raise ValueError("Failed to load UI config")
        except Exception as e:
            self.error_handler.write_show_exception(e)

    def create_connection(self) -> None:
        self.delete_button.clicked.connect(self.accept)
        self.close_button.clicked.connect(self.close)