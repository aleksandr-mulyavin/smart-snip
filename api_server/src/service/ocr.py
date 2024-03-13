from PIL import (
    Image,
    UnidentifiedImageError
)
import base64
from io import BytesIO
import pytesseract

from . import logging
from .image import ImageHandler

logger = logging.get_logger(__name__)


def image_from_base64(image_base64: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(image_base64)))


def image_to_string(
    image_base64: str,
    lang: str = '',
) -> str:
    """Recognizes text from image.

    Args:
        image_base64 (str): image in base64 format

    Returns:
        str: text from image
    """
    result = ''
    try:
        image = image_from_base64(image_base64)
        result = pytesseract.image_to_string(
            image=image,
            lang='eng+rus' if lang == '' else lang,
            timeout=5,
        )
    except UnidentifiedImageError as image_error:
        logger.error(str(image_error))
    except RuntimeError as timeout_error:
        logger.error(str(timeout_error))
    return result


def translate_image_text(
    image_base64: str,
    from_lang: str = '',
    to_lang: str = '',
) -> str:

    image = image_from_base64(image_base64)

    image_handler = ImageHandler(image=image)

    result = pytesseract.image_to_data(
        image=image,
        lang='eng+rus' if from_lang == '' else from_lang,
    )
    data = [[row for row in line.split('\t')] for line in result.split('\n')]

    image_handler.erase_text(data=data[1:])

    image_handler.draw_text(data=data[1:])

    image.save('result.png')
    buffered = BytesIO()
    image.save(buffered, format=image.format)
    return base64.b64encode(buffered.getvalue())


def get_languages():
    return pytesseract.get_languages()
