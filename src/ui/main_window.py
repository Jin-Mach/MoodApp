from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget, QCheckBox, QLineEdit

from src.core.mood_manager import MoodManager
from src.ui.mood_save_dialog import MoodSaveDialog
from src.utilities.config_provider import config_setup
from src.utilities.error_handler import ErrorHandler
from src.utilities.icons_provider import IconsProvider
from src.utilities.support_provider import SupportProvider


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindow")
        self.error_handler = ErrorHandler(self)
        self.setCentralWidget(self.create_gui())
        self.buttons = self.findChildren(QPushButton)
        self.load_setup()
        IconsProvider.set_icons(self.buttons, QSize(70, 70))
        self.create_connection()

    def create_gui(self) -> QWidget:
        main_widget = QWidget()
        main_layout =QVBoxLayout()
        self.app_text_label = QLabel()
        self.app_text_label.setObjectName("appTextLabel")
        self.app_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mood_buttons_layout = QHBoxLayout()
        self.smile_mood_button = QPushButton()
        self.smile_mood_button.setObjectName("smileMoodButton")
        self.neutral_mood_button = QPushButton()
        self.neutral_mood_button.setObjectName("neutralMoodButton")
        self.sad_mood_button = QPushButton()
        self.sad_mood_button.setObjectName("sadMoodButton")
        check_button_layout = QHBoxLayout()
        self.notes_checkbox = QCheckBox()
        self.notes_checkbox.setObjectName("notesCheckbox")
        self.notes_checkbox.checkStateChanged.connect(self.show_notes)
        self.notes_edit = QLineEdit()
        self.notes_edit.setObjectName("notesEdit")
        mood_buttons_layout.addWidget(self.smile_mood_button)
        mood_buttons_layout.addWidget(self.neutral_mood_button)
        mood_buttons_layout.addWidget(self.sad_mood_button)
        check_button_layout.addWidget(self.notes_checkbox)
        check_button_layout.addStretch()
        main_layout.addWidget(self.app_text_label)
        main_layout.addLayout(mood_buttons_layout)
        main_layout.addLayout(check_button_layout)
        main_layout.addWidget(self.notes_edit)
        main_widget.setLayout(main_layout)
        return main_widget

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            if config:
                self.setWindowTitle(config.get("mainWindowTitle", "Mood App"))
                self.setFixedWidth(config.get("mainWindowWidth", 300))
                self.setFixedHeight(config.get("mainWindowHeight", 250))
                self.app_text_label.setText(config.get(self.app_text_label.objectName(), "Mood App"))
                self.notes_checkbox.setText(config.get(f"{self.notes_checkbox.objectName()}Text", "Add note?"))
                self.notes_checkbox.setChecked(config.get(f"{self.notes_checkbox.objectName()}State", True))
                self.smile_mood_button.setToolTip(config.get(f"{self.smile_mood_button.objectName()}Tooltip", "Record happy mood"))
                self.neutral_mood_button.setToolTip(config.get(f"{self.neutral_mood_button.objectName()}Tooltip", "Record neutral mood"))
                self.sad_mood_button.setToolTip(config.get(f"{self.sad_mood_button.objectName()}Tooltip", "Record sad mood"))
                self.notes_edit.setMaxLength(config.get(f"{self.notes_edit.objectName()}MaxLength", 50))
                self.notes_edit.setPlaceholderText(config.get(f"{self.notes_edit.objectName()}PlaceholderText", "max 50 letter..."))
                for button in self.buttons:
                    button.setToolTipDuration(3000)
            else:
                self.setWindowTitle("Mood App")
                self.setFixedWidth(300)
                self.setFixedHeight(250)
                self.app_text_label.setText("Your mood tracker application\n(select mood)")
                self.notes_checkbox.setText("Add note?")
                self.notes_checkbox.setChecked(True)
                self.smile_mood_button.setToolTip("Record happy mood")
                self.neutral_mood_button.setToolTip("Record neutral mood")
                self.sad_mood_button.setToolTip("Record sad mood")
                self.notes_edit.setMaxLength(50)
                self.notes_edit.setPlaceholderText("max 50 letter...")
                for button in self.buttons:
                    button.setToolTipDuration(3000)
                raise ValueError("Failed to load UI config")
        except Exception as e:
            self.error_handler.write_show_exception(e)

    def create_connection(self) -> None:
        self.smile_mood_button.clicked.connect(lambda: self.save_mood(1))
        self.neutral_mood_button.clicked.connect(lambda: self.save_mood(0))
        self.sad_mood_button.clicked.connect(lambda: self.save_mood(-1))
        self.notes_checkbox.checkStateChanged.connect(self.show_notes)

    def show_notes(self) -> None:
        self.notes_edit.setReadOnly(not self.notes_checkbox.isChecked())

    def save_mood(self, mood: int) -> None:
        MoodManager.save_current_mood(mood, self.notes_edit.text().strip())
        self.notes_edit.clear()
        mood_save_dialog = MoodSaveDialog(self)
        mood_save_dialog.set_text(mood)
        mood_save_dialog.exec()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        SupportProvider.centre_on_screen(self)