from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

class LoggerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.label = QLabel("Логи:")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.text_edit.clear)

        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.clear_button)

    def append_log(self, level: str, msg: str):
        color_map = {
            "INFO": "#d0d0d0",
            "WARNING": "#f0ad4e",
            "ERROR": "#d9534f",
            "SUCCESS": "#5cb85c"
        }

        color = color_map.get(level.upper(), "#ffffff")
        self.text_edit.append(f'<span style="color:{color}">[{level}] {msg}</span>')
        self.text_edit.moveCursor(QTextCursor.End)
