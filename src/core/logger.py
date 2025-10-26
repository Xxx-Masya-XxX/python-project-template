import logging
import os
from datetime import datetime


class GuiLogHandler(logging.Handler):
    """Обработчик логов для GUI (LoggerWidget)."""
    def __init__(self, widget=None):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        if self.widget:
            level = record.levelname
            self.widget.append_log(level, msg)


class AppLogger:
    """Глобальный логгер приложения."""
    def __init__(self, logs_dir="data/logs"):
        os.makedirs(logs_dir, exist_ok=True)

        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
        log_path = os.path.join(logs_dir, log_filename)

        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S")

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.gui_handler = GuiLogHandler()
        self.gui_handler.setFormatter(formatter)
        self.logger.addHandler(self.gui_handler)

        self.info("Сессия логирования начата")

    def attach_widget(self, widget):
        """Подключить LoggerWidget к логгеру."""
        self.gui_handler.widget = widget
        self.info("Виджет логов подключен")

    # --- стандартные методы ---
    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)
    def warning(self, msg): self.logger.warning(msg)
    def debug(self, msg): self.logger.debug(msg)

    # --- callback для плагинов ---
    def get_callback(self):
        """Возвращает функцию log(level, message) для использования в context."""
        def log_callback(level, message):
            level = level.upper()
            if level == "INFO":
                self.logger.info(message)
            elif level == "ERROR":
                self.logger.error(message)
            elif level in ("WARN", "WARNING"):
                self.logger.warning(message)
            elif level == "DEBUG":
                self.logger.debug(message)
            elif level == "SUCCESS":
                self.logger.info("✅ " + message)
            else:
                self.logger.info(message)
        return log_callback
