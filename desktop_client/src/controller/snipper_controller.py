from PyQt5 import QtCore, QtGui, QtWidgets

from utils.image_viewer import open_stand_image_viewer, Image
from utils.config_reader import Config, ConfigReader
from utils.api_caller import call_image_to_text, call_image_to_data
from api_models import OCRData

from ui.snipping_widget import SnippingWidget


class SnipperController(QtCore.QObject):
    """
    Контроллер ножниц
    """
    # Определение сигналов Qt (событий)
    on_snipping_start = QtCore.pyqtSignal()
    on_snipping_finish = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """
        Конструктор класса
        """
        super(SnipperController, self).__init__(parent)
        self._config_reader = ConfigReader()

        # Инициализация виджета выделения (ножниц) и перехват событий
        self._snipper = SnippingWidget()
        self._snipper.on_snipping_finish.connect(self._on_snipping_finish)
        # self.on_snipping_start = self._snipper.on_snipping_start
        # self.on_snipping_finish = self._snipper.on_snipping_finish
        self._image: Image
        self._ocr_data: list[OCRData] = []

    def start_snipping(self):
        """
        Запуск виджета ножниц
        """
        self._snipper.start_snipping()
        self.on_snipping_start.emit()

    def open_stand_image_viewer(self):
        if not self.is_image_selected():
            return
        open_stand_image_viewer(self.get_selected_image(), True)

    def parse_image_to_text(self) -> str:
        if not self.is_image_selected():
            return ''
        text: str = call_image_to_text(
            self._config_reader.url,
            self._config_reader.api_key,
            self.get_selected_image())
        return text

    def parse_image_to_data(self) -> list[OCRData]:
        if not self.is_image_selected():
            return ''
        self._ocr_data: list[OCRData] = call_image_to_data(
            self._config_reader.url,
            self._config_reader.api_key,
            self.get_selected_image()).image_data
        return self._ocr_data

    def get_selected_image(self) -> Image | None:
        return self._snipper.get_selected_image()

    def is_image_selected(self) -> bool:
        """
        Проверка наличия выделенного изображения
        :return:
        """
        if self._snipper.get_selected_image():
            return True
        return False

    def _on_snipping_finish(self):
        self.on_snipping_finish.emit()
        self._image = self._snipper.get_selected_image()

