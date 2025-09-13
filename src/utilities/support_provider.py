import requests

from PyQt6.QtWidgets import QWidget, QApplication

from src.utilities.error_handler import ErrorHandler


class SupportProvider:

    @staticmethod
    def centre_on_screen(widget: QWidget) -> None:
        frame_geometry = widget.frameGeometry()
        if widget.screen():
            screen = widget.screen().availableGeometry()
        else:
            screen = QApplication.primaryScreen().availableGeometry()
        frame_geometry.moveCenter(screen.center())
        widget.move(frame_geometry.topLeft())

    @staticmethod
    def check_internet_connection() -> bool:
        try:
            request = requests.head("https://github.com/Jin-Mach/MoodApp", timeout=3)
            return request.ok
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.write_show_exception(e, False)
        return False