import sys

from PyQt6.QtWidgets import QApplication, QDialog

from src.ui.main_window import MainWindow
from src.utilities.app_init import app_init
from src.utilities.dialogs_provider import DialogsProvider


def create_app():
    application = QApplication(sys.argv)
    if not app_init():
        dialog = DialogsProvider.show_init_dialog()
        if dialog.exec() == QDialog.DialogCode.Rejected:
            sys.exit(1)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())