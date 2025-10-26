from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Signal

class SettingsWidget(QWidget):
    theme_changed = Signal(str)

    # Список доступных встроенных стилей PySide6
    AVAILABLE_THEMES = ['Fusion', 'Windows', 'WindowsVista', 'Macintosh']

    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Настройки приложения"))
        layout.addWidget(QLabel("Тема интерфейса:"))

        self.theme_box = QComboBox()
        # добавляем только стили, которые поддерживаются на текущей системе
        import PySide6.QtWidgets
        supported_styles = [s for s in PySide6.QtWidgets.QStyleFactory.keys() if s in PySide6.QtWidgets.QStyleFactory.keys()]
        self.theme_box.addItems(supported_styles)

        current_theme = self.settings.get("theme")
        if current_theme in supported_styles:
            self.theme_box.setCurrentText(current_theme)

        self.theme_box.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.theme_box)
        layout.addStretch()

    def on_theme_changed(self, theme):
        """Сохраняем выбранный стиль и вызываем сигнал для динамического применения"""
        self.settings.set("theme", theme)
        self.theme_changed.emit(theme)
