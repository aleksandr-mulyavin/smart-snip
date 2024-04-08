import PIL.Image

from . import (get_module_from_file, get_func_from_module,
               get_class_from_module)

from PIL.Image import Image
from PyQt5.QtGui import QPixmap

image_viewer_py = get_module_from_file('image_viewer.py')
conv_to_pixmap_func = get_func_from_module('conv_to_pixmap', image_viewer_py)

resource_py = get_module_from_file('resource.py')
resource_finder_class = get_class_from_module('ResourceFinder', resource_py)


def test_conv_pixmap():
    path_png = resource_finder_class().find_resource_file(
        'snip_29_03_2024_21_05_13.png')
    image: Image = PIL.Image.open(path_png)
    pixmap: QPixmap = conv_to_pixmap_func(image)
    assert pixmap is not None
    assert isinstance(pixmap, QPixmap)
    assert pixmap.width() == image.width
    assert pixmap.height() == image.height
