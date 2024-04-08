import PIL

from PIL.Image import Image
from PyQt5.QtGui import QPixmap

from ..src.utils.resource import ResourceFinder
from ..src.utils.image_viewer import conv_to_pixmap


def test_conv_pixmap():
    path_png = ResourceFinder().find_resource_file(
        'snip_29_03_2024_21_05_13.png')
    image: Image = PIL.Image.open(path_png)
    pixmap: QPixmap = conv_to_pixmap(image)
    assert pixmap is not None
    assert isinstance(pixmap, QPixmap)
    assert pixmap.width() == image.width
    assert pixmap.height() == image.height
