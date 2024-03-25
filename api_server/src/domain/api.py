from pydantic import BaseModel
from .ocr import OCRData


class ImageToTextRequest(BaseModel):
    image: str
    lang: str = ''


class ImageToDataResponse(BaseModel):
    image_data: list[OCRData]


class TranslateImageTextRequest(BaseModel):
    image: str
    to_lang: str = ''


class TranslateImageTextResponse(BaseModel):
    image: str


class Error(BaseModel):
    error: str
