from pydantic import BaseModel
from .ocr import OCRData


class ImageToTextRequest(BaseModel):
    """Query class of the method for recognizing text in an image.
    """
    image: str
    lang: str = ''


class ImageToDataResponse(BaseModel):
    """Response class of the method for recognizing text in an image.
    """
    image_data: list[OCRData]


class TranslateImageTextRequest(BaseModel):
    """Query class of the method for translating text in an image.
    """
    image: str
    to_lang: str = ''


class TranslateImageTextResponse(BaseModel):
    """Response class of the method for translating text in an image.
    """
    image: str


class Error(BaseModel):
    """Class with error description.
    """
    error: str
