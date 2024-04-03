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
        super().__init__(parent)
        self.setup_snipping_widget()

    def setup_snipping_widget(self):
        """
        Настройка экрана для области выделения
        """
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Параметры для области выделения
        self._outsideSquareColor = "red"
        self._squareThickness = 2
        self._start_point = QtCore.QPointF()
        self._end_point = QtCore.QPointF()

        # Выделенное изображение
        self._image = None

    def start_snipping(self):
        """
        Захват области экрана
        """
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
        self._start_point = QtCore.QPointF()
        self._end_point = QtCore.QPointF()

    def paintEvent(self, event):
        """
        Обработка события отрисовки виджета
        :param event: Данные события
        """
        trans_color = QtGui.QColor(22, 100, 233)
        selected_rect = QtCore.QRectF(self._start_point, self._end_point).normalized()
        painter = QtGui.QPainter(self)
        trans_color.setAlphaF(0.2)
        painter.setBrush(trans_color)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(selected_rect)
        removing_path = outer - inner
        painter.drawPath(removing_path)
        painter.setPen(
            QtGui.QPen(
                QtGui.QColor(self._outsideSquareColor),
                self._squareThickness)
        )
        trans_color.setAlphaF(0)
        painter.setBrush(trans_color)
        painter.drawRect(selected_rect)

    def get_selected_image(self) -> Image or None:
        """
        Получение выделенного изображения
        :return: Выделенное изображение
        """
        return self._image