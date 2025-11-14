from PySide6.QtWidgets import QApplication
import sys

from src.core.logger import AppLogger
from src.core.settings_manager import SettingsManager
from src.ui.main_window import MainWindow
from src.ui.settings_widget import SettingsWidget

def apply_theme(app, theme):
    """Применяет тему оформления"""
    if theme == "dark":
        app.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #3c3c3c;
                border: 1px solid #555;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4b4b4b;
            }
            QLineEdit, QTreeWidget, QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #666;
            }
        """)
    else:
        app.setStyleSheet("")  # Используем стандартную светлую тему


def main():
    app = QApplication(sys.argv)

    # === Настройки ===
    settings = SettingsManager()
    if settings.get("theme"):
        app.setStyle(settings.get("theme"))


    # === Логгер ===
    logger = AppLogger()

    # === Главное окно ===
    window = MainWindow(logger)

    # === Виджет настроек (пока можно показать отдельно или встроить в меню) ===
    settings_widget = SettingsWidget(settings)
    settings_widget.theme_changed.connect(lambda t: apply_theme(app, t))

    # Подключаем логгер
    logger.attach_widget(window.logger_widget)

    window.show()
    logger.info("Приложение запущено")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
