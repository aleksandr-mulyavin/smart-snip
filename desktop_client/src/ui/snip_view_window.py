import logging
import os
import pathlib
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QStyle

from controller.snipper_controller import SnipperController
from utils.resource import ResourceFinder
from .snip_image_viewer import SnipImageViewer
from .color_select_widget import ColorSelectComboBoxWidget
from api_models import OCRData
from utils.image_viewer import conv_to_pixmap

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
            self._pixmap = conv_to_pixmap(
                self._controller.get_selected_image())
        self._ocr_data: list[OCRData] = []

        self._resource_finder = ResourceFinder()

        # Конфигурация окна виджета
        self.__icon = QtGui.QIcon(str(self._resource_finder.find_resource_file(
            file_name='icon.png').absolute()))
        self.setWindowIcon(self.__icon)
        self.setWindowTitle('Просмотр распознанного текста')
        # self.setMaximumSize(MAX_WIDTH,
        #                     MAX_HEIGHT)
        self.setMinimumSize(MIN_WIDTH,
                            MIN_HEIGHT)
        self.__central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.__central_widget)

        try:
            # Создание действий
            self._action_paint_grp = QtWidgets.QActionGroup(self)

            self.__action_new_snip = QtWidgets.QAction(QtGui.QIcon(), f"Новая{os.linesep}вырезка")
            self.__action_new_snip.triggered.connect(self.__on_new_snip)
            self.__action_scan_text = QtWidgets.QAction(QtGui.QIcon(), f"Сканирование{os.linesep}текста")
            self.__action_scan_text.triggered.connect(self.__on_scan_text)
            self._action_view_scan_text = QtWidgets.QCheckBox(f"Отображать{os.linesep}текст")
            self._action_view_scan_text.setChecked(False)
            self._action_view_scan_text.clicked.connect(self._handle_view_scan_text)

            self.__action_color_sel = ColorSelectComboBoxWidget(with_default=True)
            self.__action_drag_hand = QtWidgets.QAction(QtGui.QIcon(), f"Перемещать")
            self.__action_drag_hand.triggered.connect(self._handle_drag_hand)
            self.__action_drag_hand.setCheckable(True)
            self.__action_drag_hand.setChecked(True)
            self._action_paint_grp.addAction(self.__action_drag_hand)
            self.__action_paint_box = QtWidgets.QAction(QtGui.QIcon(), f"Обвести")
            self.__action_paint_box.triggered.connect(self._handle_paint_box)
            self.__action_paint_box.setCheckable(True)
            self._action_paint_grp.addAction(self.__action_paint_box)
            self.__action_paint_free = QtWidgets.QAction(QtGui.QIcon(), f"Рисовать")
            self.__action_paint_free.setCheckable(True)
            self.__action_paint_free.triggered.connect(self._handle_paint_free)
            # self._action_paint_grp.addAction(self.__action_paint_free)

            self.__action_save_to_disk = QtWidgets.QAction(QtGui.QIcon(), f"Сохранить{os.linesep}изображение")
            self.__action_save_to_disk.triggered.connect(self._handle_save_to_disk)
            self.__action_save_as_to_disk = QtWidgets.QAction(QtGui.QIcon(),
                                                              f"Сохранить{os.linesep}изображение{os.linesep}как...")
            self.__action_save_as_to_disk.triggered.connect(self._handle_save_as_to_disk)
            self.__action_copy_to_clipboard = QtWidgets.QAction(QtGui.QIcon(), f"Скопировать{os.linesep}в буфер")
            self.__action_copy_to_clipboard.triggered.connect(self._handle_copy_to_clipboard)

            # Конфигурация тулбара
            self.__main_toolbar = self.addToolBar("Главное меню")
            self.__main_toolbar.addAction(self.__action_new_snip)
            self.__main_toolbar.addAction(self.__action_scan_text)
            self.__main_toolbar.addWidget(self._action_view_scan_text)
            self.__main_toolbar.addSeparator()
            self.__main_toolbar.addWidget(self.__action_color_sel)
            self.__main_toolbar.addAction(self.__action_drag_hand)
            self.__main_toolbar.addAction(self.__action_paint_box)
            self.__main_toolbar.addAction(self.__action_paint_free)
            self.__main_toolbar.addSeparator()
            self.__main_toolbar.addAction(self.__action_save_to_disk)
            self.__main_toolbar.addAction(self.__action_save_as_to_disk)
            self.__main_toolbar.addAction(self.__action_copy_to_clipboard)
        except Exception as e:
            LOGGER.exception(e)

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
        self.__text_viewer_docker = QtWidgets.QDockWidget()
        self.__layout_lvl0.addWidget(self.__text_viewer_docker)
        self.__text_viewer_docker.setMaximumWidth(int(self.geometry().width() / 3))
        self.__text_viewer_docker.hide()

        self.__text_viewer = QtWidgets.QTextBrowser()
        self.__text_viewer_docker.setWidget(self.__text_viewer)
        self.__text_viewer.hide()

        self._status_bar = self.statusBar()
        self._status_bar.show()

    def __on_new_snip(self):
        self._ocr_data = []
        self.hide()
        # self._controller.on_snipping_finish.disconnect()
        # self._controller.on_snipping_start.disconnect()
        self._controller = SnipperController()
        self._controller.start_snipping()
        self._controller.on_snipping_finish.connect(self._handle_snipping_finish)

    def __on_scan_text(self):
        try:
            text: str = self._controller.parse_image_to_text()
            self.__text_viewer.setText(text)
            self.__text_viewer.show()
            self.__text_viewer_docker.show()

            if self._action_view_scan_text.isChecked():
                self._ocr_data: list[OCRData] = self._controller.parse_image_to_data()
                for ocr in self._ocr_data:
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
                self._pixmap = conv_to_pixmap(
                    self._controller.get_selected_image())
            self._image_viewer.set_photo(self._pixmap)
            self.show()
        except Exception as e:
            logging.exception(e)

    def _handle_save_to_disk(self):
        if not self._image_viewer.get_photo():
            return
        try:
            documents_path = pathlib.Path(os.path.expanduser('~\\Documents'))
            snipped_path = documents_path.joinpath("Snipped Image")
            if not snipped_path.exists():
                snipped_path.mkdir(parents=True, exist_ok=True)
            image_path = snipped_path.joinpath(f"snip_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.png")
            file = QtCore.QFile(str(image_path))
            file.open(QtCore.QFile.WriteOnly)
            self._image_viewer.get_photo().save(file, 'PNG')
        except Exception as e:
            LOGGER.exception(e)

    def _handle_save_as_to_disk(self):
        if not self._image_viewer.get_photo():
            return
        try:
            documents_path = pathlib.Path(os.path.expanduser('~\\Documents'))
            snipped_path = documents_path.joinpath("Snipped Image")
            if not snipped_path.exists():
                snipped_path.mkdir(parents=True, exist_ok=True)
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            file_name = QtWidgets.QFileDialog.getSaveFileName(
                self,
                caption="Сохранение изображения",
                directory=str(snipped_path),
                filter="PNG(*.png)",
                options=options)
            print(file_name)
            if file_name:
                file = QtCore.QFile(f'{file_name[0]}.png')
                file.open(QtCore.QFile.WriteOnly)
                self._image_viewer.get_photo().save(file, 'PNG')
        except Exception as e:
            LOGGER.exception(e)

    def _handle_copy_to_clipboard(self):
        try:
            pixmap = self._image_viewer.get_photo()
            if pixmap is None:
                return
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(pixmap)
        except Exception as e:
            LOGGER.exception(e)

    def _handle_drag_hand(self):
        self._image_viewer.enable_drag()

    def _handle_paint_box(self):
        try:
            if self.__action_color_sel.get_сurrent_сolor() is None:
                self._status_bar.showMessage(f"Укажите цвет", 5000)
                return
            self._image_viewer.enable_draw(self._image_viewer.PAINT_BOX,
                                           self.__action_color_sel.get_сurrent_сolor())
        except Exception as e:
            LOGGER.exception(e)

    def _handle_paint_free(self):
        if self.__action_color_sel.get_сurrent_сolor() is None:
            self._status_bar.showMessage(f"Укажите цвет", 5000)
            return
        self._image_viewer.enable_draw(self._image_viewer.PAINT_FREE,
                                       self.__action_color_sel.get_сurrent_сolor())

    def _handle_view_scan_text(self):
        if self._action_view_scan_text.isChecked():
            self._ocr_data: list[OCRData] = self._controller.parse_image_to_data()
            for ocr in self._ocr_data:
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
            return
        self._image_viewer.del_all_text_labels()
