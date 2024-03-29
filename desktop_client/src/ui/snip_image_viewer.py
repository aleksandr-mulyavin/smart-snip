import logging

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import QRectF, QPoint, QRect
from PyQt5.QtGui import QColor, QPen

LOGGER = logging.getLogger(__name__)


class SnipImageViewer(QtWidgets.QGraphicsView):
    """

    """
    on_photo_clicked = QtCore.pyqtSignal(QtCore.QPoint)

    PAINT_BOX: str = 'BOX'
    PAINT_FREE: str = 'FREE'

    def __init__(self, parent=None):
        super(SnipImageViewer, self).__init__(parent)

        # Связанные объекты
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)

        # Атрибуты статуса изображения
        self._zoom_factor: float = .0
        self._is_empty: bool = True

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.viewport().installEventFilter(self)
        self._fit_in_view()
        self._first_show = True

        self._text_list: list[QtWidgets.QLineEdit] = []
        self._text_proxy_list: list[QtWidgets.QGraphicsProxyWidget] = []
        self._paint_type = None
        self._paint_color = None
        self._paint_start_point = QtCore.QPoint()

        self.pen = QPen()
        self.start = QPoint()
        self.end = QPoint()
        self.setMouseTracking(True)
        self.mouse_pressed = False
        self.rect, self.line = None, None

    def set_photo(self, pixmap: QtGui.QPixmap = None) -> None:
        self._zoom_factor = .0
        if pixmap and not pixmap.isNull():
            self._is_empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self.fitInView(QtWidgets.QGraphicsPixmapItem(pixmap),
                           QtCore.Qt.KeepAspectRatio)
            self._scene.update()
        else:
            self._is_empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self._fit_in_view()

    def get_photo(self) -> QtGui.QPixmap | None:
        try:
            print(f'To: {self.mapToScene(self._photo.pixmap().rect())}')
            print(f'From: {self.mapFromScene(self.scene().sceneRect())}')
            return self.grab(QRect(self.mapFromScene(self.scene().sceneRect().topLeft()),
                                   self.mapFromScene(self.scene().sceneRect().bottomRight())))
        except Exception as e:
            LOGGER.exception(e)

    def _fit_in_view(self, scale: bool = True) -> None:
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            print(f'PixmapRect: {rect.width()} / {rect.height()}')
            self.setSceneRect(rect)

            if self.has_photo():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                print(f'Factor: {factor}')
                print(f'ViewRect: {viewrect.width()} / {viewrect.height()}')
                print(f'SceneRect: {scenerect.width()} / {scenerect.height()}')
                self.scale(factor, factor)
            self._zoom_factor = 0

    def has_photo(self):
        return not self._is_empty

    def wheelEvent(self, event):
        if self.has_photo():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom_factor += 1
            else:
                factor = 0.8
                self._zoom_factor -= 1

            if self._zoom_factor > 0:
                self.scale(factor, factor)
            elif self._zoom_factor <= 0:
                self._fit_in_view()
            else:
                self._zoom_factor = 0

    def showEvent(self, event):
        super().showEvent(event)
        if self._first_show:
            print(f'First Show: {self._first_show}')
            self._first_show = False
            self._fit_in_view()

    def toggle_drag_mode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        print(f'mousePressEvent {event}')
        try:
            if self._photo.isUnderMouse():
                _event = QtGui.QMouseEvent(event)
                print(f'mouseMoveEvent {_event.x(), _event.y(), _event.globalX(), _event.globalY()}')
                print(f'mapToScene {self.mapToScene(event.pos())}')
                print(f'mapToScene {self.mapFromGlobal(event.globalPos())}')
                self.on_photo_clicked.emit(self.mapToScene(event.pos()).toPoint())
                if self._paint_type:
                    self._paint_start_point = self.mapToScene(event.pos())
                    if event.button() == QtCore.Qt.LeftButton:
                        self.mouse_pressed = True
                        self.start = self.mapToScene(event.pos())
        except Exception as e:
            LOGGER.exception(e)
        super(SnipImageViewer, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._photo.isUnderMouse():
            try:
                if event.buttons() & QtCore.Qt.LeftButton & self.mouse_pressed:
                    self.end = self.mapToScene(event.pos())
                    self.draw_shape()
            except Exception as e:
                LOGGER.exception(e)
        super(SnipImageViewer, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        print(f'mouseReleaseEvent {event}')
        try:
            if self._paint_type == self.PAINT_BOX:
                paint_end_point = self.mapToScene(event.pos())
                # self._scene.addRect(QRectF([self._paint_start_point, paint_end_point]),
                #                     QPen())
                if event.button() == QtCore.Qt.LeftButton and self.mouse_pressed:
                    self.mouse_pressed = False
                    self.draw_shape()
                    self.start, self.end = QPoint(), QPoint()
                    self.rect, self.line = None, None
        except Exception as e:
            print(e)
        super(SnipImageViewer, self).mouseReleaseEvent(event)

    def add_text_label(self, line: int, left: int, top: int, width: int, height: int, text: str) -> None:
        # text_obj = self._scene.addText(text)
        # text_obj.setPos(left, top)
        # text_obj.setDefaultTextColor(QtGui.QColor(255, 0, 0))
        # text_obj.setFlag(QtWidgets.QGraphicsTextItem.ItemIsSelectable)
        # text_rect = text_obj.boundingRect()
        # text_obj.setTransform(QtGui.QTransform.fromScale(width / text_rect.width(),
        #                                                  height / text_rect.height()))

        line_edit = QtWidgets.QLineEdit()
        line_edit.setText(text)
        line_edit.setReadOnly(True)
        line_edit.setEnabled(False)
        line_edit.setStyleSheet('border-style: solid;'
                                + 'border-width: 0px;border-color: red;color: red;'
                                + 'background-color: rgba(0, 0, 100, 80);')
        line_edit.move(left, top)
        line_edit.resize(width - 2, height - 2)
        font = line_edit.font()
        font.setPixelSize(height)
        line_edit.setFont(font)
        # line_edit.setAlignment(QtCore.Qt.AlignCenter)
        # line_edit.setWindowFlags(QtCore.Qt.TextSelectableByMouse)
        line_edit.setTextMargins(0, 0, 0, 0)
        # self._text_list.append(line_edit)
        proxy = self._scene.addWidget(line_edit)
        self._text_proxy_list.append(proxy)
        print(len(self._text_proxy_list))

    def del_all_text_labels(self):
        # for text in self._text_list:
        #     self._text_list.remove(text)
        #     self._scene.removeItem(text.graphicsProxyWidget())
        print(len(self._text_proxy_list))
        for proxy in self._text_proxy_list:
            self._scene.removeItem(proxy)
            self.viewport().update()
            self.update()
        self._text_proxy_list.clear()

    def enable_drag(self):
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self._paint_type = None
        self._paint_color = None

    def enable_draw(self, paint_type, color: QColor):
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self._paint_type = paint_type
        self._paint_color = color
        self.pen.setColor(color)

    def draw_shape(self):
        if self.start.isNull() or self.end.isNull():
            return
        if self.start.x() == self.end.x() and self.start.y() == self.end.y():
            return
        elif abs(self.end.x() - self.start.x()) < 20 or abs(self.end.y() - self.start.y()) < 20:
            if self.rect != None:
                self.scene().removeItem(self.rect)
                self.rect = None
            if abs(self.end.y() - self.start.y()) < 20:
                if self.line != None:
                    self.line.setLine(self.start.x(), self.start.y(), self.end.x(), self.start.y())
                else:
                    self.line = self.scene().addLine(self.start.x(), self.start.y(), self.end.x(), self.start.y(),
                                                     self.pen)
            else:
                if self.line != None:
                    self.line.setLine(self.start.x(), self.start.y(), self.start.x(), self.end.y())
                else:
                    self.line = self.scene().addLine(self.start.x(), self.start.y(), self.start.x(), self.end.y(),
                                                     self.pen)
        else:
            if self.line != None:
                self.scene().removeItem(self.line)
                self.line = None

            width = abs(self.start.x() - self.end.x())
            height = abs(self.start.y() - self.end.y())
            if self.rect == None:
                self.rect = self.scene().addRect(min(self.start.x(), self.end.x()), min(self.start.y(), self.end.y()),
                                                 width, height, self.pen)
            else:
                self.rect.setRect(min(self.start.x(), self.end.x()), min(self.start.y(), self.end.y()), width, height)
