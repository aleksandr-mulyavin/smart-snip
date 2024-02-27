import sys
from typing import Callable, List, Optional

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

from pyqtkeybind import keybinder
from PIL import ImageGrab
from PIL.Image import Image

class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    before_closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 2

        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

        self.__image = None

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        r = QtCore.QRect(self.start_point, self.end_point).normalized()
        self.__image = ImageGrab.grab(bbox=r.getCoords())
        self.before_closed.emit()
        self.hide()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit()
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def paintEvent(self, event):
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(
            QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness)
        )
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)

    def get_image(self) -> Image:
        return self.__image

class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class EventDispatcher:
    """Install a native event filter to receive events from the OS"""
    def __init__(self, keybinder) -> None:
        self.win_event_filter = WinEventFilter(keybinder)
        self.event_dispatcher: QAbstractEventDispatcher = QAbstractEventDispatcher.instance()
        self.event_dispatcher.installNativeEventFilter(self.win_event_filter)


class QtKeyBinder:
    def __init__(self, win_id: Optional[int]) -> None:
        keybinder.init()
        self.win_id = win_id

        self.event_dispatcher = EventDispatcher(keybinder=keybinder)

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        keybinder.register_hotkey(self.win_id, hotkey, callback)

    def unregister_hotkey(self, hotkey: str) -> None:
        keybinder.unregister_hotkey(self.win_id, hotkey)


class ScannerApp(QApplication):
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
        self.__snipper.get_image().show()


if __name__ == "__main__":
    app = ScannerApp(sys.argv)
    app.exec_()
