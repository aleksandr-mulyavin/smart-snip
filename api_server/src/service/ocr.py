from PIL import Image, UnidentifiedImageError
import base64
from io import BytesIO
import pytesseract

import service

logger = service.get_logger(__name__)


def image_to_string(image: str) -> str:
    """Recognizes text from image.

    Args:
        image (str): image in base64 format

    Returns:
        str: text from image
    """
    result = ''
    try:
        result = pytesseract.image_to_string(
            image=Image.open(BytesIO(base64.b64decode(image))),
            timeout=5
        )
    except UnidentifiedImageError as image_error:
        logger.error(str(image_error))
    except RuntimeError as timeout_error:
        logger.error(str(timeout_error))
    return result
