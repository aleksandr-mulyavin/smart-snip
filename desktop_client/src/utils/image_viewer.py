import logging

from PIL.Image import Image
from PyQt5 import QtGui

from threading import Thread


LOGGER = logging.getLogger(__name__)


def __show_image(image: Image) -> None:
    """
    Функция открытия стандартного просмотра изображения
    :param image: Объект изображения
    """
    image.show()


def open_stand_image_viewer(image: Image, in_new_thread: bool = True) -> None:
    """
    Функция открытия стандартного просмотра изображения
    с возможностью запуска в отдельном потоке
    :param image: Объект изображения
    :param in_new_thread: Открыть в новом потоке
    """
    if image is None:
        raise RuntimeError('Изображение не существует')

    if in_new_thread:
        thread = Thread(target=__show_image, args=(image,))
        thread.start()
    else:
        __show_image(image)


def conv_to_pixmap(image: Image) -> QtGui.QPixmap | None:
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
