from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QMenuBar, QMessageBox, QDialog
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication
from src.ui.widgets.main_widget import MainWidget
from src.ui.widgets.logger_widget import LoggerWidget
from src.ui.widgets.plugins_widget import PluginsWidget
from src.core.plugins import PluginManager
from src.core.settings_manager import SettingsManager
from src.ui.settings_widget import SettingsWidget


class MainWindow(QMainWindow):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.setWindowTitle("My App — Plugin Framework")
        self.resize(1300, 800)

        # === Настройки ===
        self.settings_manager = SettingsManager()

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.main_widget = MainWidget()
        self.logger_widget = LoggerWidget()
        self.plugins_widget = PluginsWidget()

        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(self.plugins_widget)
        right_splitter.addWidget(self.logger_widget)

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.main_widget)
        main_splitter.addWidget(right_splitter)
        main_splitter.setStretchFactor(0, 3)
        main_splitter.setStretchFactor(1, 1)

        layout.addWidget(main_splitter)
        self._create_menu()

        # === Менеджер плагинов ===
        self.plugin_manager = PluginManager(logger)
        QTimer.singleShot(200, self.load_plugins)  # загрузить после старта GUI

    def _create_menu(self):
        menu_bar = self.menuBar()

        # --- Вид ---
        view_menu = menu_bar.addMenu("Вид")
        self.toggle_logs_action = QAction("Показать логи", self, checkable=True, checked=True)
        self.toggle_plugins_action = QAction("Показать плагины", self, checkable=True, checked=True)
        view_menu.addAction(self.toggle_logs_action)
        view_menu.addAction(self.toggle_plugins_action)
        self.toggle_logs_action.toggled.connect(self.logger_widget.setVisible)
        self.toggle_plugins_action.toggled.connect(self.plugins_widget.setVisible)

        # --- Настройки ---
        settings_menu = menu_bar.addMenu("Настройки")
        self.open_settings_action = QAction("Открыть настройки", self)
        settings_menu.addAction(self.open_settings_action)
        self.open_settings_action.triggered.connect(self.open_settings_dialog)

    def open_settings_dialog(self):
        """Открывает окно с настройками"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Настройки")
        dialog.resize(400, 200)
        layout = QVBoxLayout(dialog)

        settings_widget = SettingsWidget(self.settings_manager)
        layout.addWidget(settings_widget)

        # при смене темы динамически меняем стиль приложения
        settings_widget.theme_changed.connect(lambda theme: self.apply_theme(theme))

        dialog.exec()

    def apply_theme(self, theme):
        """Применяет тему интерфейса через встроенные стили Qt"""
        app = QApplication.instance()
        if theme:
            app.setStyle(theme)


    def load_plugins(self):
        self.plugin_manager.load_plugins()
        self.plugins_widget.plugin_manager = self.plugin_manager
        self.plugins_widget.log_callback = self.logger.get_callback()

        # контекст создаётся динамически при запуске плагина
        def context_provider():
            return {
                "source_folder": "E:/Temp/Input",
                "target_folder": "E:/Temp/Output",
                "move_files": False,
                "log_callback": self.logger.get_callback(),
                "main_window": self
            }

        self.plugins_widget.load_plugins(self.plugin_manager.get_plugins(), context_provider)
        self.logger.info("Плагины загружены и отображены.")
