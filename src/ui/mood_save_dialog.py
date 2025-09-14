from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QDialogButtonBox, QLabel

from src.utilities.config_provider import config_setup
from src.utilities.error_handler import ErrorHandler


# noinspection PyUnresolvedReferences
class MoodSaveDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("moodSavedDialog")
        self.error_handler = ErrorHandler(self.parent())
        self.setLayout(self.create_gui())
        self.load_setup()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.mood_text_label = QLabel()
        self.mood_text_label.setObjectName("moodTextLabel")
        font = QFont()
        font.setBold(True)
        self.mood_text_label.setFont(font)
        self.mood_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.motivation_text_label = QLabel()
        self.motivation_text_label.setObjectName("motivationTextLabel")
        self.motivation_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.mood_text_label)
        main_layout.addWidget(self.motivation_text_label)
        main_layout.addWidget(button_box)
        return main_layout

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            if config:
                self.setWindowTitle(config.get("moodSavedDialogTitle", "Mood saved"))
            else:
                self.setWindowTitle("MoodSaved")
        except Exception as e:
            self.error_handler.write_show_exception(e)

    def set_text(self, mood: int) -> None:
        try:
            config = config_setup(self.objectName())
            if config:
                mood_map = config.get("mood_map", {})
                if mood_map:
                    mood_state = mood_map.get(str(mood), "")
                    self.mood_text_label.setText(mood_state[0])
                    self.motivation_text_label.setText(mood_state[1])
                else:
                    self.mood_text_label.setText("Mood Saved")
            else:
                self.mood_text_label.setText("Mood Saved")
        except Exception as e:
            self.error_handler.write_show_exception(e)