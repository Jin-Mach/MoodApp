import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utilities.app_init import app_init


def create_app():
    application = QApplication(sys.argv)
    if not app_init():
        print("init error")
        sys.exit(1)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())