import yaml

from pydantic import BaseModel
from .resource import ResourceFinder


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
    snip_hotkey: str


class ConfigReader(object):
    """
    Класс чтения файла конфигурации
    """
    URL_ENV: str = 'URL_ENV'
    API_KEY_ENV: str = 'API_KEY_ENV'
    CONFIG_PATH: str = 'CONFIG_PATH'
    DEFAULT_CONFIG_NAME: str = 'config.yaml'

    # Интсанция класса для шаблона - Одиночка
    __instances = dict()

    def __new__(cls, *args, **kwargs):
        """
        Метод создания инстанции класса или возврата существующей
        инстанции (часть шаблона - Одиночка)
        """
        config_file_name = ''
        if args:
            config_file_name = args[0]
        if not config_file_name and kwargs:
            config_file_name = kwargs['config_file_name']
        if not config_file_name:
            config_file_name = cls.DEFAULT_CONFIG_NAME
        if (cls.__instances.get(config_file_name) is None
                or not isinstance(cls.__instances.get(config_file_name), cls)):
            cls.__instances[config_file_name] = (super(ConfigReader, cls)
                                                 .__new__(cls))
        elif cls.__init__.__name__ == '__init__':
            cls.__init__ = lambda *args, **kwargs: None
        return cls.__instances.get(config_file_name)

    def __init__(self, config_file_name: str = DEFAULT_CONFIG_NAME):
        """
        Конструктор класса
        """
        self._config_file_name = config_file_name
        self._config = self.read_config_file(self._config_file_name)
        if self._config is None \
                or self._config.server.url is None \
                or self._config.server.api_key is None \
                or self._config.server.url == "" \
                or self._config.server.api_key == "":
            raise RuntimeError('Настройки не заданы')

        self.url = self._config.server.url
        self.api_key = self._config.server.api_key
        self.snip_hotkey = self._config.snip_hotkey
        if self.snip_hotkey is None or self.snip_hotkey == '':
            self.snip_hotkey = 'Ctrl+Shift+A'

    @staticmethod
    def read_config_file(file_name: str) -> Config | None:
        """
        Чтение параметров из файла
        :return: Инстанция объекта файла конфигурации
        """
        resource_finder = ResourceFinder()
        file_path = resource_finder.find_resource_file(file_name)
        if not file_path:
            raise FileNotFoundError()
        filename: str = str(file_path.absolute())

        with open(filename, 'r') as f:
            config_file = yaml.safe_load(f)
            print(config_file)

        return Config(**config_file)
