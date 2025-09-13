import pathlib

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton

from src.utilities.error_handler import ErrorHandler


class IconsProvider:

    @staticmethod
    def set_icons(widgets: list[QPushButton], size: QSize) -> None:
        try:
            icons_path = pathlib.Path(__file__).parents[2].joinpath("icons")
            for widget in widgets:
                icon_path = icons_path.joinpath(f"{widget.objectName()}_icon.png")
                if icon_path.exists():
                    widget.setIcon(QIcon(str(icon_path)))
                    widget.setIconSize(size)
                else:
                    widget.setFixedSize(size)
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.write_show_exception(e, cancel_visible=True)