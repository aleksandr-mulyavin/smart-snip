import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PIL.Image import Image

from ..controller import SnipperController
from .snip_image_viewer import SnipImageViewer
from ..api_models import OCRData

MAX_WIDTH: int = 800
MAX_HEIGHT: int = 600
MIN_WIDTH: int = 800
MIN_HEIGHT: int = 600

LOGGER = logging.getLogger(__name__)


class SnipViewWindow(QtWidgets.QMainWindow):
    def __init__(self, controller: SnipperController, parent=None):
        super(SnipViewWindow, self).__init__(parent)

        # Запись входных параметров в атрибуты класса
        self._controller = controller

        # Конвертация изображения в QPixmap для Qt
        self._pixmap = QtGui.QPixmap()
        if self._controller.is_image_selected():
            self._pixmap = self.__conv_to_pixmap(
                self._controller.get_selected_image())

        # Конфигурация окна виджета
        self.__icon = QtGui.QIcon("../../icon.png")
        self.setWindowIcon(self.__icon)
        self.setWindowTitle('Просмотр распознанного текста')
        # self.setMaximumSize(MAX_WIDTH,
        #                     MAX_HEIGHT)
        self.setMinimumSize(MIN_WIDTH,
                            MIN_HEIGHT)
        self.__central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.__central_widget)

        # Создание действий
        self.__action_new_snip = QtWidgets.QAction(QtGui.QIcon(), "Новая вырезка")
        self.__action_new_snip.triggered.connect(self.__on_new_snip)
        self.__action_scan_text = QtWidgets.QAction(QtGui.QIcon(), "Сканирование текста")
        self.__action_scan_text.triggered.connect(self.__on_scan_text)
        self.__action_lasso = QtWidgets.QAction(QtGui.QIcon(), "Лассо")
        self.__action_lasso.triggered.connect(self.__on_lasso)

        # Конфигурация тулбара
        self.__main_toolbar = self.addToolBar("Главное меню")
        self.__main_toolbar.addAction(self.__action_new_snip)
        self.__main_toolbar.addAction(self.__action_scan_text)
        self.__main_toolbar.addAction(self.__action_lasso)

        # Формирование центрального лайоута виджета
        self.__layout_lvl0 = QtWidgets.QHBoxLayout()
        self.__central_widget.setLayout(self.__layout_lvl0)
        self.__layout_lvl0.setContentsMargins(1, 1, 1, 1)

        # Создание контейнера для изобрадения
        self._image_viewer = SnipImageViewer(self)
        self._image_viewer.set_photo(self._pixmap)
        # self.__graphics_scene = QtWidgets.QGraphicsScene()
        # self.__graphics_view = QtWidgets.QGraphicsView()
        # self.__graphics_view.setScene(self.__graphics_scene)
        # self.__layout_lvl0.addWidget(self.__graphics_view)
        self.__layout_lvl0.addWidget(self._image_viewer)

        # Отрисовка изображения в контейнере
        # self.__graphics_scene.addPixmap(self._pixmap)
        # # self.__graphics_view.fitInView(QtWidgets.QGraphicsPixmapItem(self.__pixmap),
        # #                                QtCore.Qt.KeepAspectRatio)
        # self.__graphics_scene.update()

        # Создание поля просмотра текста
        self.__text_viewer = QtWidgets.QTextBrowser()
        # self.__text_viewer.setText(self.__text_to_browser_processing(self._text))
        self.__text_viewer_docker = QtWidgets.QDockWidget()
        self.__text_viewer_docker.setWidget(self.__text_viewer)

        self.__lasso_viewer = QtWidgets.QGraphicsView()

        self.__stack = QtWidgets.QTabWidget()
        self.__stack.tabBarAutoHide()
        self.__stack.addTab(self.__text_viewer, '1')
        self.__stack.addTab(self.__lasso_viewer, '2')
        self.__stack.hide()
        self.__layout_lvl0.addWidget(self.__stack)

    def keyPressEvent(self, event):
        event = QtGui.QKeyEvent(event)
        print(event.key(), event.text())

    def mousePressEvent(self, event):
        event = QtGui.QMouseEvent(event)
        print(event.globalPos(), event.type(), event.button())

    def mouseReleaseEvent(self, event):
        print(event)

    def wheelEvent(self, event):
        modifiers = QtGui.QGuiApplication.keyboardModifiers()
        event = QtGui.QWheelEvent(event)
        print(event.globalPosition(), event.angleDelta(),
              True if (modifiers == QtCore.Qt.ControlModifier) else False)

    def __on_new_snip(self):
        self.hide()
        # self._controller.on_snipping_finish.disconnect()
        # self._controller.on_snipping_start.disconnect()
        self._controller = SnipperController()
        self._controller.start_snipping()
        self._controller.on_snipping_finish.connect(self._handle_snipping_finish)

    def __on_scan_text(self):
        try:
            ocr_data: list[OCRData] = self._controller.parse_image_to_data()
            for ocr in ocr_data:
                if ocr.text == '' or ocr.text.replace(' ', '') == '':
                    continue
                print(f'OCR: {ocr}')
                self._image_viewer.add_text_label(
                    line=ocr.line_num,
                    left=ocr.left,
                    top=ocr.top,
                    width=ocr.width,
                    height=ocr.height,
                    text=ocr.text)
        except Exception as e:
            print(e)

    def __on_lasso(self):
        pass

    @staticmethod
    def __conv_to_pixmap(image: Image) -> QtGui.QPixmap:
        try:
            image_local = image.convert("RGBA")
            image_data = image_local.tobytes("raw", "RGBA")
            q_image = QtGui.QImage(image_data,
                                   image_local.size[0],
                                   image_local.size[1],
                                   QtGui.QImage.Format_ARGB32)
            print(image.size[0], image.size[1])
            print(image_local.size[0], image_local.size[1])
            return QtGui.QPixmap.fromImage(q_image)
        except Exception as e:
            logging.exception(e)
            return QtGui.QPixmap()

    @staticmethod
    def __text_to_browser_processing(text: str) -> str:
        local_text = text.replace("\\n", "<br>")
        return local_text

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
                self._pixmap = self.__conv_to_pixmap(
                    self._controller.get_selected_image())
            self._image_viewer.set_photo(self._pixmap)
            self.show()
        except Exception as e:
            logging.exception(e)