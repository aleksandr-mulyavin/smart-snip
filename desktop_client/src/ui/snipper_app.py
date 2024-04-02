import logging
import os
from typing import List

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from utils.config_reader import ConfigReader
from .snip_view_window import SnipViewWindow
from .modal_translate import translatess
from controller.snipper_controller import SnipperController
from utils.sys_event_key import QtKeyBinder
from utils.resource import ResourceFinder
from utils.image_viewer import conv_to_pixmap
from utils.api_caller import call_image_to_text
from utils.image_search import open_search_in_browser

LOGGER = logging.getLogger("SnipperApp")

class SnipperApp(QtWidgets.QApplication):
    """
    Класс основного приложения Умных ножниц
    """

    def __init__(self, argv: List[str]) -> None:
        """
        Конструктор класса
        """
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        self._resource_finder = ResourceFinder()
        self._config_reader = ConfigReader()

        # Настройка приложения
        self._config_app()

        # Инициализация контроллера ножниц
        self._snipper_controller = SnipperController()
        self._snipper_controller.on_snipping_finish.connect(self._handle_snipping_finish)

    def _config_app(self) -> None:
        """
        Метод конфигурации приложения
        """
        # Привязка hotkey для выделения экрана
        self._sample_key_binder = QtKeyBinder(win_id=None)
        self._sample_key_binder.register_hotkey(self._config_reader.snip_hotkey,
                                                self._handle_activate_snipping)

        # Привязка иконки в системном трее
        self._tray = QtWidgets.QSystemTrayIcon()
        self._icon = QtGui.QIcon(str(self._resource_finder.find_resource_file(file_name='icon.png').absolute()))
        self._tray.setIcon(self._icon)
        self._tray.setVisible(True)

        # Настройка основного меню программы в системном трее
        self._tray_menu = QtWidgets.QMenu()
        self._tray_menu_snip_action = QtWidgets.QAction("Выделить область")
        self._tray_menu_snip_action.triggered.connect(self._handle_activate_snipping)
        self._tray_menu.addAction(self._tray_menu_snip_action)
        self._tray_menu_translatess = QtWidgets.QAction("Переводчик")
        self._tray_menu_translatess.triggered.connect(self._translate)
        self._tray_menu.addAction(self._tray_menu_translatess)
        self._tray_menu_quit_action = QtWidgets.QAction("Выход")
        self._tray_menu_quit_action.triggered.connect(self.quit)
        self._tray_menu.addAction(self._tray_menu_quit_action)
        self._tray.setContextMenu(self._tray_menu)

        # Настройка контекстного меню выделенного изображения
        self._img_menu = QtWidgets.QMenu()
        self._img_menu_stand_view_action = QtWidgets.QAction("Показать в просмотрщике")
        self._img_menu_stand_view_action.triggered.connect(self._handle_stand_view)
        self._img_menu.addAction(self._img_menu_stand_view_action)
        self._img_menu_snip_view_action = QtWidgets.QAction("Открыть выделенную область")
        self._img_menu_snip_view_action.triggered.connect(self._handle_snip_view)
        self._img_menu.addAction(self._img_menu_snip_view_action)
        self._img_menu.addSeparator()
        self._img_menu_recognize_and_copy = QtWidgets.QAction("Распознать и скопировать в буфер")
        self._img_menu_recognize_and_copy.triggered.connect(self._handle_recognize_and_copy)
        self._img_menu.addAction(self._img_menu_recognize_and_copy)
        self._img_menu_snip_and_copy = QtWidgets.QAction("Скопировать в буфер")
        self._img_menu_snip_and_copy.triggered.connect(self._handle_snip_and_copy)
        self._img_menu.addAction(self._img_menu_snip_and_copy)
        self._img_menu.addSeparator()
        self._img_menu_web_search_action = QtWidgets.QAction("Найти...")
        self._img_menu.addAction(self._img_menu_web_search_action)
        self._img_menu_web_search_action.triggered.connect(self._handle_web_search)

    def _handle_activate_snipping(self):
        """
        Активация процесса выделения области
        """
        self._snipper_controller.start_snipping()

    def _translate(self):
        """
        Обработчик события - Перевести
        """
        self.new_window = translatess()
        self.new_window.show()

    def _handle_snipping_finish(self):
        """
        Обработчик события окончания выделения
        """
        if not self._snipper_controller.get_selected_image():
            return
        try:
            self._img_menu.exec_(QtGui.QCursor.pos())
        except Exception as e:
            logging.exception("An error occurred when handling snipping finish event", exc_info=True)

    def _handle_stand_view(self):
        """
        Обработчик события - Показать в просмотрщике
        """
        if not self._snipper_controller.is_image_selected():
            return
        self._snipper_controller.open_stand_image_viewer()

    def _handle_snip_view(self):
        """
        Обработчик события - Открыть выделенную область
        """
        self._snip_viewer = SnipViewWindow(self._snipper_controller)
        self._snip_viewer.show()

    def _handle_recognize_and_copy(self):
        """
        Обработчик события - Распознать и скопировать в буфер
        """
        if not self._snipper_controller.is_image_selected():
            return
        text = call_image_to_text(
            url=self._config_reader.url,
            token=self._config_reader.api_key,
            image=self._snipper_controller.get_selected_image())
        if text is not None:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    def _handle_snip_and_copy(self):
        """
        Обработчик события - Скопировать в буфер
        """
        if not self._snipper_controller.is_image_selected():
            return
        clipboard = QApplication.clipboard()
        pixmap = conv_to_pixmap(self._snipper_controller.get_selected_image()) or QtGui.QPixmap()
        clipboard.setPixmap(pixmap)

    def _handle_web_search(self):
        """
        Обработчик события - Поиск в Интернете
        """
        if not self._snipper_controller.is_image_selected():
            return
        open_search_in_browser(
            self._snipper_controller.get_selected_image())
