import PIL.Image

from pathlib import Path

from . import get_module_from_file, get_func_from_module

from PIL.Image import Image
from PyQt5.QtGui import QPixmap

resource_py = get_module_from_file('image_viewer.py')
conv_to_pixmap_func = get_func_from_module('conv_to_pixmap', resource_py)


def _test_conv_pixmap():
    path = Path(__file__).parent.joinpath(
        'resources/snip_29_03_2024_21_05_13.png')
    image: Image = PIL.Image.open(path)
    pixmap: QPixmap = conv_to_pixmap_func(image)
    assert pixmap is not None
    assert isinstance(pixmap, QPixmap)
    assert pixmap.width() == image.width
    assert pixmap.height() == image.height
