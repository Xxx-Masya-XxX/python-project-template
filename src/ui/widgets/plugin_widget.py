from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt


class PluginWidget(QWidget):
    """
    Виджет одного плагина (отображает информацию и кнопку "Запустить")
    """
    def __init__(self, plugin_info: dict, run_callback):
        super().__init__()

        self.plugin_info = plugin_info
        self.run_callback = run_callback

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Название плагина
        name_label = QLabel(f"{plugin_info.get('icon', '🔌')} <b>{plugin_info.get('name', 'Без названия')}</b>")
        layout.addWidget(name_label)

        # Автор и версия
        meta = QLabel(f"<i>{plugin_info.get('author', 'Автор неизвестен')}</i> — версия {plugin_info.get('version', 'N/A')}")
        meta.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(meta)

        # Описание
        desc = QLabel(plugin_info.get('description', ''))
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 12px;")
        layout.addWidget(desc)

        # Кнопка запуска
        btn_layout = QHBoxLayout()
        run_btn = QPushButton("▶ Запустить")
        run_btn.clicked.connect(self._on_run_clicked)
        btn_layout.addStretch()
        btn_layout.addWidget(run_btn)
        layout.addLayout(btn_layout)

        # Оформление карточки
        self.setStyleSheet("""
            PluginWidget {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                background: #fafafa;
            }
            QPushButton {
                padding: 4px 8px;
            }
        """)

    def _on_run_clicked(self):
        """Вызов внешнего callback при нажатии на кнопку."""
        if callable(self.run_callback):
            self.run_callback()
