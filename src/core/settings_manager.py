import json
import os

class SettingsManager:
    DEFAULTS = {
        "theme": "light"
    }

    def __init__(self, path="config/settings.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.data = self.load()

    def load(self):
        """Загружает настройки из файла"""
        if not os.path.exists(self.path):
            self.save(self.DEFAULTS)
            return dict(self.DEFAULTS)

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return dict(self.DEFAULTS)

    def save(self, data=None):
        """Сохраняет настройки"""
        if data is not None:
            self.data.update(data)

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get(self, key):
        return self.data.get(key, self.DEFAULTS.get(key))

    def set(self, key, value):
        self.data[key] = value
        self.save()
