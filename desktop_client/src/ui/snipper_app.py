import logging
import os
from typing import List

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

from utils.config_reader import ConfigReader
from .snip_view_window import SnipViewWindow
from controller.snipper_controller import SnipperController
from utils.sys_event_key import QtKeyBinder
from utils.resource import ResourceFinder
# from utils.image_viewer import conv_to_pixmap
# from utils.api_caller import call_image_to_text

LOGGER = logging.getLogger(__name__)


class SnipperApp(QtWidgets.QApplication):
    """
    Класс основного приложения Умных ножниц
    """

    def __init__(self, argv: List[str]) -> None:
        """
        Конструктор класса
        """
        super(SnipperApp, self).__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        self._resource_finder = ResourceFinder()
        self._config_reader = ConfigReader()

        # Настройка приложения
        self._config_app()

        # Инициализация контроллера ножниц
        self._snipper_controller = SnipperController()
        self._snipper_controller.on_snipping_finish.connect(self._handle_snipping_finish)

        # Инициализация виджета выделения (ножниц) и перехват событий
        # self._snipper = SnippingWidget()
        # self._snipper.on_snipping_finish.connect(self._handle_snipping_finish)

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
        self._icon = QtGui.QIcon(str(self._resource_finder.find_resource_file(
            file_name='icon.png').absolute()))
        self._tray.setIcon(self._icon)
        self._tray.setVisible(True)

        # Настройка основного меню программы в системном трее
        self._tray_menu = QtWidgets.QMenu()
        self._tray_menu_snip_action = QtWidgets.QAction("Выделить область")
        self._tray_menu_snip_action.triggered.connect(self._handle_activate_snipping)
        self._tray_menu.addAction(self._tray_menu_snip_action)
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
        self._img_menu_web_search_action = QtWidgets.QAction("Найти...")
        self._img_menu.addAction(self._img_menu_web_search_action)

    def _handle_activate_snipping(self):
        self._snipper_controller.start_snipping()
        # self._snipper.showFullScreen()
        # QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def _handle_snipping_finish(self):
        """
        Обработчик события окончания выделения
        """
        if not self._snipper_controller.get_selected_image():
            return
        try:
            self._img_menu.exec_(QtGui.QCursor.pos())
        except Exception as e:
            logging.exception(e)

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
