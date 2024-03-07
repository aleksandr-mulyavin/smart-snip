from typing import List

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

from .snipping_widget import SnippingWidget
from desktop_client.src.controller import open_stand_image_viewer
from desktop_client.src.utils import QtKeyBinder


class ScannerApp(QApplication):
    """
    Основнове приложение умных ножниц
    """
    def __init__(self, argv: List[str]) -> None:
        super(ScannerApp, self).__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        self.__config_app()

        self.__snipper = SnippingWidget()
        self.__snipper.closed.connect(self.__on_closed)
        self.__snipper.before_closed.connect(self.__on_before_closed)

    def __config_app(self):
        self.sample_key_binder = QtKeyBinder(win_id=None)
        self.sample_key_binder.register_hotkey("Ctrl+Shift+A", self.__activateSnipping)

        self.icon = QIcon("../../icon.png")

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.context_menu = QMenu()
        self.context_menu_option1 = QAction("Сканировать область")
        self.context_menu_option1.triggered.connect(self.__activateSnipping)
        self.context_menu.addAction(self.context_menu_option1)
        self.context_menu_quit_action = QAction("Выход")
        self.context_menu_quit_action.triggered.connect(self.quit)
        self.context_menu.addAction(self.context_menu_quit_action)

        self.tray.setContextMenu(self.context_menu)

        self.img_menu = QMenu()
        self.img_menu_option0 = QAction("Показать")
        self.img_menu_option0.triggered.connect(self.__on_view_img)
        self.img_menu.addAction(self.img_menu_option0)
        self.img_menu_option1 = QAction("Распознать")
        self.img_menu.addAction(self.img_menu_option1)
        self.img_menu_option2 = QAction("Распознать и перевести")
        self.img_menu.addAction(self.img_menu_option2)
        self.img_menu_option3 = QAction("Найти...")
        self.img_menu.addAction(self.img_menu_option3)
        self.img_menu_option4 = QAction("Описать изображение")
        self.img_menu.addAction(self.img_menu_option4)

    def __activateSnipping(self):
        self.__snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def __on_closed(self):
        print("ccc")

    def __on_before_closed(self):
        img = self.__snipper.get_image()
        if img:
            print("aaa")
            # self.img_menu.popup()
            self.img_menu.exec_(QtGui.QCursor.pos())
            print("bbb")

    def __on_view_img(self):
        open_stand_image_viewer(self.__snipper.get_image())
