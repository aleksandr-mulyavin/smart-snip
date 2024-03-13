from pydantic import BaseModel


class ImageToTextRequest(BaseModel):
    image: str
    lang: str = ''


class TranslateImageTextRequest(BaseModel):
    image: str
    to_lang: str = ''


class TranslateImageTextResponse(BaseModel):
    image: str


class Error(BaseModel):
    error: str
