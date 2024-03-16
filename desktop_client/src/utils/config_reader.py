import os
import yaml

from pydantic import BaseModel


class ServerConfig(BaseModel):
    """
    Объект блока конфигурации сервера
    """
    url: str
    api_key: str


class Config(BaseModel):
    """
    Объект файл конфигурации
    """
    server: ServerConfig


class ConfigReader(object):
    """
    Класс чтения файла конфигурации
    """
    URL_ENV: str = 'URL_ENV'
    API_KEY_ENV: str = 'API_KEY_ENV'
    CONFIG_PATH: str = 'CONFIG_PATH'

    # Интсанция класса для шаблона - Одиночка
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Метод создания инстанции класса или возврата существующей
        инстанции (часть шаблона - Одиночка)
        """
        if not isinstance(cls.__instance, cls):
            cls.__instance = object.__new__(cls)
            return cls.__instance
        return cls.__instance

    def __init__(self):
        """
        Конструктор класса
        """

        # Получение параметров из окружения (если задано)
        self.url: str = os.getenv(self.URL_ENV)
        self.api_key: str = os.getenv(self.API_KEY_ENV)

        # Если в окружении не задано, то чтение параметров из файла
        if self.url is None or self.api_key is None:
            config = self.read_config_file(os.getenv(self.CONFIG_PATH))
            if config is None or config.server.url is None or config.server.api_key is None \
                    or config.server.url == "" or config.server.api_key == "":
                raise RuntimeError('Настройки не заданы')
            self.url = config.server.url
            self.api_key = config.server.api_key

    @staticmethod
    def read_config_file(config_path: str) -> Config | None:
        """
        Чтение параметров из файла
        :param config_path: Путь к файлу с параметрами (без имени файла)
        :return: Инстанция объекта файла конфигурации
        """
        filename: str = ""
        if config_path is not None and config_path != "":
            filename = config_path + '\\config.yaml'
        if config_path is None or config_path == "":
            filename = f'{os.path.dirname(__file__)}\\..\\..\\config.yaml'

        config_file: dict
        # try:
        with open(filename, 'r') as f:
            config_file = yaml.safe_load(f)
            print(config_file)
        # except FileNotFoundError:
        #     print(f'Файл {filename} не найден')
        #     return None

        return Config(**config_file)
