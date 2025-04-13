import os
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # Определяем путь к файлу конфигурации
    config_file_path = os.path.join(os.path.dirname(__file__), filename)

    # Создаем парсер
    parser = ConfigParser()

    # Читаем файл конфигурации
    parser.read(config_file_path)

    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, config_file_path))

    return db
