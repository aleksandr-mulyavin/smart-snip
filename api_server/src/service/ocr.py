from PIL import (
    Image,
    ImageDraw,
    ImageFont,
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
    to_lang: str = '',
) -> str:

    image = image_from_base64(image_base64)

    eraser = ImageHandler(image=image)

    result = pytesseract.image_to_data(image=image)
    data = [[row for row in line.split('\t')] for line in result.split('\n')]

    font = ImageFont.truetype('arial.ttf', 30)

    eraser.erase_text(data=data[1:])

    draw = ImageDraw.Draw(image)
    for row in data[1:]:
        if len(row) == 12 and row[10] != '-1':
            text = row[11]

            if text.strip() != '':
                x1 = int(row[6])
                y1 = int(row[7])
                width = int(row[8])
                height = int(row[9])
                if width > 10 and height > 10:
                    draw.text(
                        xy=(x1, y1),
                        text=text,
                        font=font,
                        fill=(0, 0, 0)
                    )

    image.save('result.png')
    buffered = BytesIO()
    image.save(buffered, format=image.format)
    return base64.b64encode(buffered.getvalue())


def get_languages():
    return pytesseract.get_languages()
