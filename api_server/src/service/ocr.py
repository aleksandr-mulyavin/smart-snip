from PIL import Image, UnidentifiedImageError
import base64
from io import BytesIO
import pytesseract

from . import logging

logger = logging.get_logger(__name__)


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
        image = Image.open(BytesIO(base64.b64decode(image_base64)))
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


def get_languages():
    return pytesseract.get_languages()
