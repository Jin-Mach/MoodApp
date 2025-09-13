from PyQt6.QtWidgets import QWidget, QApplication


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