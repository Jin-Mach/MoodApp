import pathlib

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, \
    QDialogButtonBox, QAbstractItemView, QLabel

from src.core.mood_manager import MoodManager
from src.utilities.config_provider import config_setup
from src.utilities.error_handler import ErrorHandler


# noinspection PyUnresolvedReferences
class HistoryDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("historyDialog")
        self.setFixedSize(600, 400)
        self.error_handler = ErrorHandler(self.parent())
        self.setLayout(self.create_gui())
        self.load_setup()
        self.load_data()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.history_table = QTableWidget()
        self.history_table.setObjectName("historyTable")
        self.history_table.setColumnCount(3)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.history_table.setSortingEnabled(True)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.close)
        main_layout.addWidget(self.history_table)
        main_layout.addWidget(button_box)
        return main_layout

    def load_setup(self) -> None:
        try:
            config = config_setup(self.objectName())
            if config:
                self.setWindowTitle(config.get(f"{self.objectName()}Title", "History"))
                self.history_table.setHorizontalHeaderLabels(config.get(f"{self.history_table.objectName()}Tables", ["Date", "Mood", "Note"]))
            else:
                self.history_table.setHorizontalHeaderLabels(["Date", "Mood", "Note"])
                self.setWindowTitle("History")
                raise ValueError("Failed to load UI config")
        except Exception as e:
            self.error_handler.write_show_exception(e)

    def load_data(self) -> None:
        try:
            formated_data = MoodManager.format_data()
            if formated_data:
                self.history_table.setRowCount(len(formated_data))
                icons_path = pathlib.Path(__file__).parents[3].joinpath("icons")
                icon_map = {"1": icons_path.joinpath("smileMoodButton_icon.png"),
                            "0": icons_path.joinpath("neutralMoodButton_icon.png"),
                            "-1": icons_path.joinpath("sadMoodButton_icon.png")}
                for index, (date, mood, note) in enumerate(formated_data):
                    self.history_table.setItem(index, 0, QTableWidgetItem(date))
                    pixmap = QPixmap(str(icon_map.get(str(mood), mood)))
                    pixmap = pixmap.scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    label = QLabel()
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.history_table.setCellWidget(index, 1, label)
                    self.history_table.setItem(index, 2, QTableWidgetItem(note))
        except Exception as e:
            self.error_handler.write_show_exception(e)