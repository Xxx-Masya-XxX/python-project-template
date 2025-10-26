import importlib.util
import os
import traceback


class PluginManager:
    def __init__(self, logger, plugins_dir="plugins"):
        self.logger = logger
        self.plugins_dir = plugins_dir
        self.plugins = []  # список словарей с {'module', 'info'}

    def load_plugins(self):
        """Загрузка всех плагинов из папки plugins/"""
        self.logger.info("Загрузка плагинов...")
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
            return

        for filename in os.listdir(self.plugins_dir):
            if not filename.endswith(".py"):
                continue

            plugin_path = os.path.join(self.plugins_dir, filename)
            plugin_name = os.path.splitext(filename)[0]

            try:
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "get_plugin_info") and hasattr(module, "run_plugin"):
                    info = module.get_plugin_info()
                    self.plugins.append({"module": module, "info": info})
                    self.logger.info(f"Плагин загружен: {info['name']} ({info['version']})")
                else:
                    self.logger.warning(f"Пропущен {filename}: отсутствуют обязательные функции")

            except Exception as e:
                self.logger.error(f"Ошибка загрузки плагина {filename}: {e}")
                traceback.print_exc()

    def get_plugins(self):
        """Возвращает список информации о загруженных плагинах"""
        return self.plugins
