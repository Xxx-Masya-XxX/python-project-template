from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QWidgetItem, QPushButton, QHBoxLayout, QFileDialog
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
import os
from src.ui.widgets.plugin_widget import PluginWidget


class PluginsWidget(QWidget):
    def __init__(self, plugin_manager=None, log_callback=None):
        super().__init__()
        self.plugin_manager = plugin_manager
        self.log_callback = log_callback
        self._last_context_provider = None

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("🔌 Доступные плагины:"))

        # ...existing code...
        # Панель кнопок (перезагрузка, открыть папку)
        btn_layout = QHBoxLayout()
        self.reload_btn = QPushButton("⟳ Перезагрузить плагины")
        self.open_folder_btn = QPushButton("📁 Открыть папку плагинов")
        btn_layout.addWidget(self.reload_btn)
        btn_layout.addWidget(self.open_folder_btn)
        layout.addLayout(btn_layout)

        # Прокручиваемая область
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.inner = QWidget()
        self.inner_layout = QVBoxLayout(self.inner)
        self.scroll.setWidget(self.inner)

        layout.addWidget(self.scroll)

        # Сигналы
        self.reload_btn.clicked.connect(self._on_reload_clicked)
        self.open_folder_btn.clicked.connect(self._on_open_folder_clicked)

    def load_plugins(self, plugins, context_provider):
        """Отобразить загруженные плагины."""
        # сохраняем provider для возможности перезагрузки из виджета
        self._last_context_provider = context_provider

        # Очистка
        while self.inner_layout.count():
            item = self.inner_layout.takeAt(0)
            if isinstance(item, QWidgetItem):
                item.widget().deleteLater()

        for plugin in plugins:
            w = PluginWidget(plugin['info'], lambda info=plugin['info']: self._run_plugin(info, context_provider))
            self.inner_layout.addWidget(w)

    def _run_plugin(self, plugin_info, context_provider):
        """Запуск плагина через context."""
        context = context_provider()
        module = next(p['module'] for p in self.plugin_manager.plugins if p['info'] == plugin_info)
        try:
            result = module.run_plugin(context)
            if self.log_callback:
                self.log_callback("SUCCESS", f"{plugin_info['name']} завершил работу: {result.get('message', '')}")
        except Exception as e:
            if self.log_callback:
                self.log_callback("ERROR", f"Ошибка при запуске {plugin_info['name']}: {e}")

    def _on_reload_clicked(self):
        """Попытаться перезагрузить плагины через plugin_manager и обновить виджеты."""
        if not self.plugin_manager:
            if self.log_callback:
                self.log_callback("ERROR", "Plugin manager не задан")
            return

        # попытки вызвать различные имена методов перезагрузки
        try:
            if hasattr(self.plugin_manager, 'reload_plugins'):
                self.plugin_manager.reload_plugins()
            elif hasattr(self.plugin_manager, 'reload'):
                self.plugin_manager.reload()
            elif hasattr(self.plugin_manager, 'load_plugins'):
                self.plugin_manager.load_plugins()
            else:
                if self.log_callback:
                    self.log_callback("ERROR", "Plugin manager не содержит метод перезагрузки")
                return
        except Exception as e:
            if self.log_callback:
                self.log_callback("ERROR", f"Ошибка при перезагрузке плагинов: {e}")
            return

        # получить обновлённый список плагинов
        plugins = getattr(self.plugin_manager, 'plugins', None)
        if plugins is None and hasattr(self.plugin_manager, 'get_plugins'):
            try:
                plugins = self.plugin_manager.get_plugins()
            except Exception:
                plugins = None

        if plugins is None:
            if self.log_callback:
                self.log_callback("WARN", "Не удалось получить список плагинов после перезагрузки")
            return

        # если есть сохранённый context_provider — использовать его для обновления UI
        if self._last_context_provider:
            self.load_plugins(plugins, self._last_context_provider)
        else:
            # иначе просто обновим виджеты без контекста (подстройте при необходимости)
            self.load_plugins(plugins, lambda: {})

        if self.log_callback:
            self.log_callback("INFO", "Плагины перезагружены")

    def _on_open_folder_clicked(self):
        """Открыть папку с плагинами в проводнике (Windows) или через QDesktopServices."""
        folder = None
        if self.plugin_manager:
            for attr in ('plugins_dir', 'plugins_path', 'plugins_folder', 'folder', 'path'):
                folder = getattr(self.plugin_manager, attr, None)
                if folder:
                    break

        # если путь не найден — предложить выбрать вручную
        if not folder or not os.path.exists(folder):
            dlg = QFileDialog(self)
            chosen = dlg.getExistingDirectory(self, "Выберите папку плагинов", os.getcwd())
            if not chosen:
                return
            folder = chosen

        try:
            # Windows-специфично
            if os.name == 'nt':
                os.startfile(folder)
            else:
                # fallback
                QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
            if self.log_callback:
                self.log_callback("INFO", f"Открыта папка плагинов: {folder}")
        except Exception as e:
            if self.log_callback:
                self.log_callback("ERROR", f"Не удалось открыть папку плагинов: {e}")