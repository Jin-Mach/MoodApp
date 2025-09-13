from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget

from src.utilities.config_provider import config_setup


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindow")
        self.setCentralWidget(self.create_gui())
        self.load_setup()

    def create_gui(self) -> QWidget:
        main_widget = QWidget()
        main_layout =QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_text_label = QLabel()
        self.app_text_label.setObjectName("appTextLabel")
        self.app_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mood_buttons_layout = QHBoxLayout()
        self.happy_mood_button = QPushButton()
        self.happy_mood_button.setObjectName("happyMoodButton")
        self.neutral_mood_button = QPushButton()
        self.neutral_mood_button.setObjectName("neutralMoodButton")
        self.sad_mood_button = QPushButton()
        self.sad_mood_button.setObjectName("sadMoodButton")
        mood_buttons_layout.addWidget(self.happy_mood_button)
        mood_buttons_layout.addWidget(self.neutral_mood_button)
        mood_buttons_layout.addWidget(self.sad_mood_button)
        main_layout.addWidget(self.app_text_label)
        main_layout.addLayout(mood_buttons_layout)
        main_widget.setLayout(main_layout)
        return main_widget

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            if config:
                self.setWindowTitle(config.get("mainWindowTitle", ""))
                self.setFixedWidth(config.get("mainWindowWidth", 300))
                self.setFixedHeight(config.get("mainWindowHeight", 200))
                self.app_text_label.setText(config.get(self.app_text_label.objectName(), "Mood App"))
        except Exception as e:
            print(e)