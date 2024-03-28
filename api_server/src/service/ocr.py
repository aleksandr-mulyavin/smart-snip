import sys
from PIL import (
    Image,
    UnidentifiedImageError
)
import base64
from io import BytesIO
import pytesseract

from .logging import get_logger
from ..domain.ocr import OCRData
from .image import ImageHandler
from .translating import Translator

logger = get_logger(__name__)


def image_from_base64(image_base64: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(image_base64)))


def image_to_string(
    image_base64: str,
    lang: str = '',
) -> str:
    """Recognizes text from image.

    Args:
        image_base64 (str): image in base64 format
        lang (str): language of the text

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

    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': str(exc_value)
        }
        logger.error(traceback_details)

    return result


def image_to_data(
    image_base64: str,
    lang: str = '',
) -> list[OCRData]:
    """Recognizes text from image.

    Args:
        image_base64 (str): image in base64 format
        lang (str): language of the text

    Returns:
        list[OCRData]: data from pytesseract
    """
    result = []
    try:

        image = image_from_base64(image_base64)
        str_data = pytesseract.image_to_data(
            image=image,
            lang='eng+rus' if lang == '' else lang,
            timeout=5,
        )

        data = [line for line in str_data.split('\n')]

        result = [OCRData.from_str(line) for line in data[1:]]
        while None in result:
            result.remove(None)

    except Exception as e:
        logger.error(str(e))

        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': str(exc_value)
        }
        logger.error(traceback_details)

    return result


def translate_image_text(
    image_base64: str,
    from_lang: str = 'en',
    to_lang: str = 'ru',
) -> str:
    result = ''

    image = image_from_base64(image_base64)

    image_handler = ImageHandler(
        image=image,
        translator=Translator(from_lang=from_lang, to_lang=to_lang)
    )

    try:

        lang = 'eng+rus' if from_lang == '' or from_lang == 'en' else from_lang
        str_data = pytesseract.image_to_data(
            image=image,
            lang=lang,
        )

        data = [line for line in str_data.split('\n')]

        image_data = [OCRData.from_str(line) for line in data[1:]]

        image_handler.translate_text(data=image_data)
        # image.save('result.png')

        buffered = BytesIO()
        image.save(buffered, format=image.format)

        result = base64.b64encode(buffered.getvalue())

    except Exception as e:
        logger.error(str(e))

        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': str(exc_value)
        }
        logger.error(traceback_details)

    return result


def get_languages():
    return pytesseract.get_languages()
