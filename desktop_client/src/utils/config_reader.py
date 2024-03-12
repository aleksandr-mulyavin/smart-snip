import os
import yaml

from pydantic import BaseModel


class Config(BaseModel):
    class ServerConfig(BaseModel):
        url: str
        api_key: str

    server: ServerConfig


class ConfigReader(object):
    URL_ENV: str = 'URL_ENV'
    API_KEY_ENV: str = 'API_KEY_ENV'

    def __init__(self):
        self.__url: str = os.getenv(self.URL_ENV)
        self.__api_key: str = os.getenv(self.API_KEY_ENV)
        if self.__url is None or self.__api_key is None:
            config = self.read_config_file()
            if config.url is None or config.api_key is None \
                    or config.url == "" or config.api_key == "":
                raise RuntimeError('Настройки не заданы')
            self.__url = config.url
            self.__api_key = config.api_key

    def save(self):
        pass

    @staticmethod
    def read_config_file() -> Config:

        config_file: dict
        with open(f'{os.path.dirname(__file__)}/../config.yaml', 'r') as f:
            config_file = yaml.safe_load(f)

        return Config(**config_file)
