import unittest

from ..src.utils.config_reader import ConfigReader


class ConfigReaderTest(unittest.TestCase):
    """
    Тесты для модуля чтения конфигурации
    """
    CORRECT_CONFIG_FILE_NAME: str = "config_correct.yaml"
    INVALID_CONFIG_FILE_NAME: str = "config_invalid.yaml"
    NOT_FOUND_CONFIG_FILE_NAME: str = "config_not_found.yaml"

    CORRECT_URL = 'https://test.ru/'
    CORRECT_API_KEY = '1234567890'
    CORRECT_SNIP_HOTKEY = "Ctrl+Shift+A"

    def test_correct_config(self):
        """
        Тест чтения корректной конфигурации
        """
        try:
            config_reader = ConfigReader(self.CORRECT_CONFIG_FILE_NAME)
            assert config_reader is not None
            assert config_reader.url == self.CORRECT_URL
            assert config_reader.api_key == self.CORRECT_API_KEY
            assert config_reader.snip_hotkey == self.CORRECT_SNIP_HOTKEY
        except FileNotFoundError as file_not_found_error:
            self.failureException(file_not_found_error)

    def test_invalid_config(self):
        """
        Тест чтения некорректной конфигурации
        """
        try:
            ConfigReader(self.INVALID_CONFIG_FILE_NAME)
        except Exception as e:
            self.failureException(e)

    def test_not_found_config(self):
        """
        Тест чтения некорректной конфигурации
        """
        try:
            ConfigReader(self.NOT_FOUND_CONFIG_FILE_NAME)
        except FileNotFoundError as file_not_found_error:
            self.failureException(file_not_found_error)
