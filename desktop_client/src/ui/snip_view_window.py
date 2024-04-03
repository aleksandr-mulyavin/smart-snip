import os
import logging
import pathlib
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

from api_models import OCRData
from controller.snipper_controller import SnipperController
from utils.image_viewer import conv_to_pixmap
from utils.resource import ResourceFinder
from .snip_image_viewer import SnipImageViewer
from .color_select_widget import ColorSelectComboBoxWidget

MAX_WIDTH: int = 800
MAX_HEIGHT: int = 600
MIN_WIDTH: int = 800
MIN_HEIGHT: int = 600

LOGGER = logging.getLogger(__name__)


class SnipViewWindow(QtWidgets.QMainWindow):
    """
    Окно просмотра изображения и операций над ним
    """

    def __init__(self, controller: SnipperController, parent=None):
        """
        Конструктор объекта
        :param controller: Контроллер операций сканирования и распознавания
        :param parent: Родительский виджет
        """
        super(SnipViewWindow, self).__init__(parent)

        # Запись входных параметров в атрибуты класса
        self._controller = controller
        """Контроллер операций сканирования и распознавания"""

        # Конвертация изображения в QPixmap для Qt
        self._pixmap = QtGui.QPixmap()
        """Объект изображения"""

        # Если изображение отсканировано с экрана,
        # то его необходимо конвертировать в QPixmap
        if self._controller.is_image_selected():
            self._pixmap = conv_to_pixmap(
                self._controller.get_selected_image())
        if self._pixmap is None:
            self._pixmap = QtGui.QPixmap()

        # Инициализация списка распознанных блоков
        self._ocr_data: list[OCRData] = []
        """Список распознанных блоков"""

        # Инициализация объекта поиска ресурсов
        self._resource_finder = ResourceFinder()
        """Объект поиска ресурсов"""

        # Конфигурация окна виджета
        self._icon = QtGui.QIcon(str(
            self._resource_finder.find_resource_file(
                file_name='icon.png').absolute()))
        """Иконка окна"""
        self.setWindowIcon(self._icon)
        self.setWindowTitle('Просмотр распознанного текста')
        self.setMinimumSize(MIN_WIDTH,
                            MIN_HEIGHT)
        self._central_widget = QtWidgets.QWidget()
        """Центральный виджет окна"""
        self.setCentralWidget(self._central_widget)

        try:
            # Создание действий тулбара
            self._action_paint_grp = QtWidgets.QActionGroup(self)
            """Группа действий переключателя рисования"""

            self._action_new_snip = QtWidgets.QAction(
                QtGui.QIcon(),
                f"Новая{os.linesep}вырезка")
            """Действие для нового снимка экрана"""
            self._action_new_snip.triggered.connect(self._handle_new_snip)

            self._action_scan_text = QtWidgets.QAction(
                QtGui.QIcon(),
                f"Сканирование{os.linesep}текста")
            """Действие для сканирование текста на изображении"""
            self._action_scan_text.triggered.connect(self._handle_scan_text)

            self._action_color_sel = ColorSelectComboBoxWidget(
                withDefault=True)
            """Виджет выбора цвета выделения"""

            self._action_drag_hand = QtWidgets.QAction(
                QtGui.QIcon(),
                "Перемещать")
            """Действие для включения режима перемещения"""
            self._action_drag_hand.triggered.connect(self._handle_drag_hand)
            self._action_drag_hand.setCheckable(True)
            self._action_drag_hand.setChecked(True)
            self._action_paint_grp.addAction(self._action_drag_hand)

            self._action_paint_box = QtWidgets.QAction(
                QtGui.QIcon(),
                "Обвести")
            """Действие для режима обведения на изображении"""
            self._action_paint_box.triggered.connect(self._handle_paint_box)
            self._action_paint_box.setCheckable(True)
            self._action_paint_grp.addAction(self._action_paint_box)

            self._action_save_to_disk = QtWidgets.QAction(
                QtGui.QIcon(),
                f"Сохранить{os.linesep}изображение")
            """Действие сохранения изображения на диск"""
            self._action_save_to_disk.triggered.connect(
                self._handle_save_to_disk)

            self._action_save_as_to_disk = QtWidgets.QAction(
                QtGui.QIcon(),
                f"Сохранить{os.linesep}изображение{os.linesep}как...")
            """Действие сохранения изображения с указанием имени"""
            self._action_save_as_to_disk.triggered.connect(
                self._handle_save_as_to_disk)

            self._action_copy_to_clipboard = QtWidgets.QAction(
                QtGui.QIcon(),
                f"Скопировать{os.linesep}в буфер")
            """Действие копирования изображения в буфер обмена"""
            self._action_copy_to_clipboard.triggered.connect(
                self._handle_copy_to_clipboard)

            # Конфигурация тулбара
            self._main_toolbar = self.addToolBar("Главное меню")
            """Главный тулбар (меню)"""
            self._main_toolbar.addAction(self._action_new_snip)
            self._main_toolbar.addAction(self._action_scan_text)
            self._main_toolbar.addSeparator()
            self._main_toolbar.addWidget(self._action_color_sel)
            self._main_toolbar.addAction(self._action_drag_hand)
            self._main_toolbar.addAction(self._action_paint_box)
            self._main_toolbar.addSeparator()
            self._main_toolbar.addAction(self._action_save_to_disk)
            self._main_toolbar.addAction(self._action_save_as_to_disk)
            self._main_toolbar.addAction(self._action_copy_to_clipboard)
        except Exception as e:
            LOGGER.exception(e)

        # Формирование центрального лайоута виджета
        self._layout_lvl0 = QtWidgets.QHBoxLayout()
        """Центральный лайоут окна"""
        self._central_widget.setLayout(self._layout_lvl0)
        self._layout_lvl0.setContentsMargins(0, 0, 0, 0)

        # Создание контейнера для изобрадения
        self._image_viewer = SnipImageViewer(self)
        """Контейнер для просмотра изображения"""
        self._image_viewer.set_photo(self._pixmap)
        self._layout_lvl0.addWidget(self._image_viewer)

        # Создание поля просмотра текста
        self._text_viewer_docker = QtWidgets.QDockWidget()
        """Док виджет для просмотра сканированного текста"""
        self._layout_lvl0.addWidget(self._text_viewer_docker)
        self._text_viewer_docker.setMaximumWidth(
            int(self.geometry().width() / 3))
        self._text_viewer_docker.hide()

        self._text_viewer = QtWidgets.QTextBrowser()
        """Виджет для просмотра сканированного текста"""
        self._text_viewer_docker.setWidget(self._text_viewer)
        self._text_viewer.hide()

        self._status_bar = self.statusBar()
        """Статус бар"""
        self._status_bar.show()

    # @staticmethod
    # def _text_to_browser_processing(text: str) -> str:
    #     local_text = text.replace("\\n", "<br>")
    #     return local_text

    def _handle_new_snip(self) -> None:
        """
        Обработка кнопки создания нового снимка экрана
        """
        # Скрытие экрана (чтобы не мерцало и не мешало)
        self.hide()

        # Пересоздание контроллера для нового снимка
        self._controller = SnipperController()
        self._controller.start_snipping()
        self._controller.on_snipping_finish.connect(
            self._handle_snipping_finish)

    def _handle_snipping_finish(self):
        """
        Обработчик события окончания выделения
        """
        if not self._controller.get_selected_image():
            return
        try:
            # Конвертация изображения в QPixmap для Qt
            self._pixmap = QtGui.QPixmap()
            if self._controller.is_image_selected():
                self._pixmap = conv_to_pixmap(
                    self._controller.get_selected_image())
            if self._pixmap is None:
                self._pixmap = QtGui.QPixmap()
            self._image_viewer.set_photo(self._pixmap)
            self.show()
        except Exception as e:
            LOGGER.exception(e)

    def _handle_scan_text(self) -> None:
        """
        Обработка кнопки сканирования текста на изображении
        """
        try:
            # Передача изображения и получение текста из API
            text: str = self._controller.parse_image_to_text()
            self._text_viewer.setText(text)
            # Показ виджета для показа текста
            self._text_viewer.show()
            self._text_viewer_docker.show()
        except Exception as e:
            LOGGER.exception(e)

    def _handle_drag_hand(self) -> None:
        """
        Обработка кнопки включение режима перетаскивания изображения
        """
        self._image_viewer.enable_drag()

    def _handle_paint_box(self) -> None:
        """
        Обработка кнопки включения режима обведения на изображении
        :return:
        """
        try:
            if self._action_color_sel.get_current_color() is None:
                self._status_bar.showMessage("Укажите цвет", 5000)
                return
            self._image_viewer.enable_draw(
                self._image_viewer.PAINT_BOX,
                self._action_color_sel.get_current_color())
        except Exception as e:
            LOGGER.exception(e)

    def _handle_save_to_disk(self) -> None:
        """
        Обработка кнопки сохранения изображения на диск
        """
        if not self._image_viewer.get_photo():
            return
        try:
            snipped_path = self.__get_and_create_save_path()
            # Генерация имени файла и сохранение
            image_path = snipped_path.joinpath(
                f"snip_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.png")
            file = QtCore.QFile(str(image_path))
            file.open(QtCore.QFile.WriteOnly)
            self._image_viewer.get_photo().save(file, 'PNG')
        except Exception as e:
            LOGGER.exception(e)

    def _handle_save_as_to_disk(self) -> None:
        """
        Обработка кнопки сохранения изображения на диск с выбором имени
        """
        if not self._image_viewer.get_photo():
            return
        try:
            snipped_path = self.__get_and_create_save_path()
            # Открытие окна ввода имени файла
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            file_name = QtWidgets.QFileDialog.getSaveFileName(
                self,
                caption="Сохранение изображения",
                directory=str(snipped_path),
                filter="PNG(*.png)",
                options=options)
            # Если имя файла введено, то сохраним
            if file_name:
                file = QtCore.QFile(f'{file_name[0]}.png')
                file.open(QtCore.QFile.WriteOnly)
                self._image_viewer.get_photo().save(file, 'PNG')
        except Exception as e:
            LOGGER.exception(e)

    def _handle_copy_to_clipboard(self) -> None:
        """
        Обработка кнопки копирования изображения в буфер обмена
        """
        try:
            pixmap = self._image_viewer.get_photo()
            if pixmap is None:
                return
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(pixmap)
        except Exception as e:
            LOGGER.exception(e)

    @staticmethod
    def __get_and_create_save_path() -> pathlib.Path:
        """
        Получение пути сохранения и создания папки
        """
        documents_path = pathlib.Path(os.path.expanduser('~\\Documents'))
        snipped_path = documents_path.joinpath("Snipped Image")
        if not snipped_path.exists():
            snipped_path.mkdir(parents=True, exist_ok=True)
        return snipped_path
