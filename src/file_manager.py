import json
import os


class FileManager:
    """Класс для работы с файлами."""

    @staticmethod
    def save_to_file(data, filename: str = "vacancies.json") -> None:
        """Сохраняет данные в файл в формате JSON."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка при записи в файл {filename}: {e}")

    @staticmethod
    def load_from_file(filename: str = "vacancies.json") -> dict:
        """Загружает данные из файла в формате JSON."""
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден.")
            return {}
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
