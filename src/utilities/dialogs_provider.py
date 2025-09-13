from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox


# noinspection PyUnresolvedReferences
class DialogsProvider:

    @staticmethod
    def show_init_dialog() -> QDialog:
        dialog = QDialog()
        dialog.setModal(True)
        dialog.setWindowTitle("Init error")
        main_layout = QVBoxLayout()
        text_label = QLabel()
        font = QFont()
        font.setBold(True)
        text_label.setText("Application initialization failed.\nThe application will now close.")
        text_label.setFont(font)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(dialog.reject)
        main_layout.addWidget(text_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        dialog.setFixedSize(dialog.sizeHint())
        return dialog