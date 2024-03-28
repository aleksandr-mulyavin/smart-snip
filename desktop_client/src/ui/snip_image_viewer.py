from PyQt5 import QtCore, QtGui, QtWidgets


class SnipImageViewer(QtWidgets.QGraphicsView):
    """

    """
    on_photo_clicked = QtCore.pyqtSignal(QtCore.QPoint)

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
        if self._photo.isUnderMouse():
            self.on_photo_clicked.emit(self.mapToScene(event.pos()).toPoint())
        super(SnipImageViewer, self).mousePressEvent(event)

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
        self._scene.addWidget(line_edit)
