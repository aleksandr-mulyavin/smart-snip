from PyQt5 import QtCore, QtGui, QtWidgets

from PIL import ImageGrab
from PIL.Image import Image


class SnippingWidget(QtWidgets.QMainWindow):
    """
    Виджет выделения области экрана
    """
    # Определение сигналов Qt (событий)
    on_snipping_start = QtCore.pyqtSignal()
    on_snipping_finish = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """
        Конструктор класса
        """
        super(SnippingWidget, self).__init__(parent)

        # Настройка экрана для области выделения
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Параметры для области выделения
        self._outsideSquareColor = "red"
        self._squareThickness = 2
        self._start_point = QtCore.QPoint()
        self._end_point = QtCore.QPoint()

        # Выделенное изображение
        self._image = None

    def start_snipping(self):
        self.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.on_snipping_start.emit()

    def mousePressEvent(self, event):
        """
        Обработка события начала выделения
        :param event: Данные события
        """
        self._image = None
        self._start_point = event.pos()
        self._end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        """
        Обработка события процесса выделения
        :param event: Данные события
        """
        self._end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        """
        Обработка события окончания выделения
        :param event: Данные события
        """
        # Получение изображения из области выделения
        rect = QtCore.QRect(self._start_point, self._end_point).normalized()
        self._image = ImageGrab.grab(bbox=rect.getCoords())
        QtWidgets.QApplication.restoreOverrideCursor()

        # Скрытие области выделения
        self.on_snipping_finish.emit()
        self.hide()

        # Обнуление позиций
        self._start_point = QtCore.QPoint()
        self._end_point = QtCore.QPoint()

    def paintEvent(self, event):
        """
        Обработка события отрисовки виджета
        :param event: Данные события
        """
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self._start_point, self._end_point).normalized()
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
            QtGui.QPen(
                QtGui.QColor(self._outsideSquareColor),
                self._squareThickness)
        )
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)

    def get_selected_image(self) -> Image | None:
        """
        Получение выделенного изображения
        :return: Выделенное изображение
        """
        return self._image
