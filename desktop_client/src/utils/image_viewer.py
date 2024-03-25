from PIL.Image import Image

from threading import Thread


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
